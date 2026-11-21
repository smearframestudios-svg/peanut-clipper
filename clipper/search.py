"""Keyword search: transcribe the whole stream once, then find every time a word or phrase is
said (or typed in chat), and turn any match into a Short or a Premiere export."""
import datetime as dt
import hashlib
import re
from pathlib import Path

from . import download
from .chat import load_chat
from .pipeline import progress
from .transcribe import transcribe_range
from .util import hms, load_json, media_duration, probe, save_json, slug

CHUNK = 600          # transcribe in 10-minute pieces (cached, so re-searching is instant)
LEAD, TAIL = 10, 8   # default seconds before / after a match when making a Short


# ------------------------------------------------------------------ text matching
def _norm(w):
    return re.sub(r"[^a-z0-9]+", "", w.lower().replace("'", ""))


def _stem(w):
    for suf in ("ings", "ing", "ers", "er", "ies", "es", "ed", "s"):
        if len(w) > len(suf) + 2 and w.endswith(suf):
            w = w[: -len(suf)]
            break
    return w[:-1] if len(w) > 3 and w.endswith("e") else w


def parse_queries(text):
    qs = []
    for part in re.split(r"[,\n;]+", text or ""):
        toks = [_norm(t) for t in part.split()]
        toks = [t for t in toks if t]
        if toks:
            qs.append({"label": " ".join(part.split()).strip().strip('"'), "toks": toks})
    return qs


def find_in_words(words, queries, similar=True):
    """Every place a query phrase is spoken. Returns [(query_label, i_first, i_last)]."""
    key = (lambda t: _stem(t)) if similar else (lambda t: t)
    norm = [key(_norm(w["w"])) for w in words]
    hits = []
    for q in queries:
        qt = [key(t) for t in q["toks"]]
        n = len(qt)
        for i in range(len(norm) - n + 1):
            if norm[i] == qt[0] and norm[i:i + n] == qt:
                hits.append((q["label"], i, i + n - 1))
    return hits


def context(words, i0, i1, before=10, after=10):
    a, b = max(0, i0 - before), min(len(words), i1 + after + 1)
    parts = []
    for i in range(a, b):
        w = words[i]["w"].strip()
        parts.append(f"[[{w}]]" if i0 <= i <= i1 else w)
    text = " ".join(parts)
    return ("..." if a > 0 else "") + text + ("..." if b < len(words) else "")


# ------------------------------------------------------------------ full transcript
def full_transcript(video, cfg, cache_path, label="Listening to the stream"):
    dur = media_duration(video)
    words, segs = [], []
    n = max(1, int((dur + CHUNK - 1) // CHUNK))
    for k in range(n):
        a = k * CHUNK
        d = min(CHUNK, dur - a)
        if d <= 0.5:
            break
        progress(35 + 55 * k / n, f"{label} ({hms(a)} of {hms(dur)})")
        tr = transcribe_range(video, float(a), float(d), cfg, cache_path)
        words += tr["words"]
        segs += tr["segments"]
    return {"words": words, "segments": segs, "duration": dur}


def _local_cache_dir(cfg, path):
    h = hashlib.sha1(str(Path(path).resolve()).encode()).hexdigest()[:12]
    d = cfg["paths"]["work_dir"] / "_local" / h
    d.mkdir(parents=True, exist_ok=True)
    return d


# ------------------------------------------------------------------ matching
def find_matches(tr, chat, queries, cfg, similar=True):
    words = tr["words"]
    out = []
    last = {}
    for label, i0, i1 in find_in_words(words, queries, similar):
        t = words[i0]["s"]
        if t - last.get(label, -999) < 8:      # same phrase repeated right away = one match
            continue
        last[label] = t
        out.append({"t": round(t, 2), "t_end": round(words[i1]["e"], 2), "query": label, "kind": "speech",
                    "text": context(words, i0, i1)})
    if chat:
        delay = cfg["detect"]["chat_delay_sec"]
        for q in queries:
            rx = re.compile(r"(?<!\w)" + r"\W*".join(re.escape(t) for t in q["toks"]), re.I)
            times = [(t, m) for t, m in chat if rx.search(m)]
            groups = []
            for t, m in times:
                if groups and t - groups[-1]["last"] <= 20:
                    groups[-1]["n"] += 1
                    groups[-1]["last"] = t
                else:
                    groups.append({"first": t, "last": t, "n": 1, "msg": m})
            for g in groups:
                if g["n"] < 2:
                    continue      # one random chatter isn't a moment
                t = max(0.0, g["first"] - delay)
                out.append({"t": round(t, 2), "t_end": round(t + 3, 2), "query": q["label"], "kind": "chat",
                            "count": g["n"], "text": f'{g["n"]} chat messages, e.g. "{g["msg"][:120]}"'})
    out.sort(key=lambda m: m["t"])
    # one result per moment: merge speech hits within 12s of each other (different words, same moment)
    merged = []
    for m in out:
        prev = merged[-1] if merged else None
        if prev and m["kind"] == prev["kind"] == "speech" and m["t"] - prev["t"] <= 12:
            if m["query"] not in prev["queries"]:
                prev["queries"].append(m["query"])
            prev["t_end"] = max(prev["t_end"], m["t_end"])
            prev["text"] = _merge_marks(prev["text"], m["text"])
            continue
        m["queries"] = [m["query"]]
        merged.append(m)
    return merged


def _merge_marks(a, b):
    """Keep the highlights from both context snippets (they overlap a lot)."""
    marked = set(re.findall(r"\[\[(.+?)\]\]", b))
    for w in marked:
        a = re.sub(r"(?<!\[)\b" + re.escape(w) + r"\b(?!\]\])", f"[[{w}]]", a, count=1)
    return a


# ------------------------------------------------------------------ the search command
def run_search(cfg, source, words_text, start=None, end=None, use_chat=True, similar=True, layout=None,
               audio_only=False):
    from .util import apply_layout
    layout = apply_layout(cfg, layout)
    queries = parse_queries(words_text)
    if not queries:
        raise SystemExit("[!] Type at least one word or phrase to search for.")
    sid = f"{dt.datetime.now():%Y%m%d-%H%M%S}-search-{slug(queries[0]['label'], 24)}"
    out = cfg["paths"]["output_dir"] / sid
    out.mkdir(parents=True, exist_ok=True)
    progress(2, "Getting the stream")
    offset, dl, chat_file = 0.0, None, None
    if download.is_url(source):
        dl = cfg["paths"]["work_dir"] / "_downloads" / download.cache_key(source, start, end)
        dl.mkdir(parents=True, exist_ok=True)
        if audio_only:                     # just the sound; video pieces come later, only for matches you use
            video = download.download_audio(source, dl, start, end)
            audio_only = video.name.startswith("audio.")
        else:
            video = download.download_video(source, dl, cfg, start, end)
        if use_chat:
            progress(32, "Getting chat")
            chat_file = download.download_chat(source, dl, start, end)
        offset = start or 0.0
        cache = dl / "transcripts.json"
    else:
        video = Path(source)
        cache = _local_cache_dir(cfg, video) / "transcripts.json"
        audio_only = False
    dur = media_duration(video)
    chat = load_chat(chat_file, offset=offset, duration=dur) if chat_file else []
    tr = full_transcript(video, cfg, cache)
    if not tr["words"]:
        print("[!] No speech could be read from this stream (is the speech model installed?)")
    progress(92, "Searching")
    matches = find_matches(tr, chat, queries, cfg, similar)
    for i, m in enumerate(matches):
        m["i"] = i
    data = {"sid": sid, "source": source, "url": source if download.is_url(source) else "",
            "source_file": str(Path(video).resolve()), "source_dir": str(dl) if dl else None,
            "transcript_cache": str(cache), "offset": offset, "duration": dur,
            "words": words_text, "queries": [q["label"] for q in queries], "matches": matches, "layout": layout,
            "created": dt.datetime.now().isoformat(timespec="seconds"), "audio_only": bool(audio_only)}
    save_json(out / "search.json", data)
    save_json(out / "clips.json", {"job": sid, "source": source, "clips": [], "source_dir": data["source_dir"],
                                   "created": data["created"], **download.stream_extras(dl)})
    progress(100, f"Found {len(matches)} match{'es' if len(matches) != 1 else ''}")
    print(f"  {len(matches)} matches for: {', '.join(data['queries'])}")
    return sid


# ------------------------------------------------------------------ cutting a match
def snap(segments, start, end, max_len=180):
    """Start at the beginning of the sentence we land in, end at the end of the sentence."""
    for s in segments:
        if s["s"] <= start < s["e"] and start - s["s"] <= 6:
            start = s["s"]
            break
    for s in segments:
        if s["s"] < end <= s["e"] and s["e"] - end <= 6:
            end = s["e"] + 0.4
            break
    if end - start > max_len:
        start = end - max_len
    return max(0.0, start), end


def _segments_from_cache(cache_path):
    segs, words = [], []
    for v in (load_json(cache_path, {}) or {}).values():
        segs += v.get("segments", [])
        words += v.get("words", [])
    segs.sort(key=lambda s: s["s"])
    words.sort(key=lambda w: w["s"])
    return segs, words


PART_PAD = 120     # a sound-only search downloads this much video either side of a match you use


def match_video(cfg, data, a, b):
    """(video file, shift) for seconds a-b of a search (file time = search time - shift).
    Sound-only searches download just that piece, unless the whole video is already on the PC."""
    if not data.get("audio_only"):
        return Path(data["source_file"]), 0.0
    if data.get("source_dir"):
        full = download.full_video(data["source_dir"])
        if full:
            return download.fix_sync(full, cfg), 0.0
    if not data.get("url"):
        raise SystemExit("[!] This search has no stream link to get the video from.")
    dur = float(data.get("duration") or 0) or b + PART_PAD
    pa, pb = max(0.0, a - PART_PAD), min(dur, b + PART_PAD)
    off = float(data.get("offset") or 0)
    progress(8, "Getting this part of the video")
    part = download.download_part(data["url"], cfg, off + pa, off + pb, cfg["paths"]["work_dir"])
    return part, pa


def clip_from_match(cfg, sid, idx, export=False, lead=LEAD, tail=TAIL, layout=None):
    from .library import export_raw
    from .render import render_short
    from .titles import make_description, make_title
    from .util import apply_layout
    out = cfg["paths"]["output_dir"] / sid
    data = load_json(out / "search.json")
    apply_layout(cfg, layout or data.get("layout"))
    m = next((x for x in data["matches"] if x["i"] == int(idx)), None)
    if not m:
        raise SystemExit("[!] That match wasn't found.")
    if data.get("audio_only"):
        dur = float(data.get("duration") or 0) or media_duration(data["source_file"])
        segs, words = _segments_from_cache(data["transcript_cache"])
        start, end = snap(segs, max(0.0, m["t"] - lead), min(dur, m["t_end"] + tail))
        src, shift = match_video(cfg, data, start, end)
    else:
        src = Path(data["source_file"])
        if not src.exists():
            raise SystemExit("[!] The stream for this search was already deleted. Search again to re-download it.")
        from .download import fix_sync
        fixed = fix_sync(src, cfg)
        if str(fixed) != str(src):
            data["source_file"] = str(fixed)
            save_json(out / "search.json", data)
        src, shift = fixed, 0.0
        dur = probe(src)[0]
        segs, words = _segments_from_cache(data["transcript_cache"])
        start, end = snap(segs, max(0.0, m["t"] - lead), min(dur, m["t_end"] + tail))
    _, sw, sh = probe(src)
    text = " ".join(w["w"] for w in words if start <= w["s"] < end)
    title = make_title(text, [], "", cfg)
    clips_path = out / "clips.json"
    cd = load_json(clips_path)
    cid = f"{len(cd['clips']) + 1:02d}"
    url = data["url"]
    if url and "youtube" in url:
        url = f"{url}{'&' if '?' in url else '?'}t={int(data['offset'] + start)}s"
    clip = {"id": cid, "file": "", "poster": "", "start": data["offset"] + start, "end": data["offset"] + end,
            "src_start": round(start - shift, 2), "src_end": round(end - shift, 2), "source_file": str(src),
            "length": round(end - start, 1), "score": 0, "reasons": [f"says '{m['query']}'" if m["kind"] == "speech"
                                                                    else f"chat says '{m['query']}'"],
            "transcript": text, "title": title, "description": make_description(title, cfg, url),
            "status": "pending", "from_search": m["i"], "layout": cfg["layout"].get("id")}
    if export:
        clip["status"] = "approved"
        cd["clips"].append(clip)
        save_json(clips_path, cd)
        progress(20, "Exporting for Premiere")
        export_raw(cfg, sid, cid)
    else:
        progress(20, "Making the Short")
        w = [dict(x, s=x["s"] - shift, e=x["e"] - shift) for x in words] if cfg["captions"]["enabled"] else []
        mp4, jpg = render_short(src, start - shift, end - shift, out / f"clip_{cid}.mp4", w, cfg, sw, sh)
        clip.update(file=mp4.name, poster=jpg.name)
        cd["clips"].append(clip)
        save_json(clips_path, cd)
    save_json(cfg["paths"]["work_dir"] / "last_made.json", {"job": sid, "id": cid, "export": export})
    progress(100, "Exported for Premiere" if export else "Short ready - opening the editor")
    return sid, cid


# ------------------------------------------------------------------ saved keywords on every stream
def add_keyword_clips(cfg, out, video, cache, chat, offset, src_url, existing):
    """Called at the end of a normal run: adds Shorts for your saved keywords."""
    from .render import render_short
    from .titles import make_description, make_title
    st = cfg["settings"]
    queries = parse_queries(", ".join(st.get("saved_keywords", [])))
    if not queries:
        return []
    tr = full_transcript(video, cfg, cache, "Searching for your saved words")
    matches = find_matches(tr, chat, queries, cfg)
    matches.sort(key=lambda m: (m["kind"] != "speech", -m.get("count", 0)))
    dur, sw, sh = probe(video)
    taken = [(c["src_start"], c["src_end"]) for c in existing]
    added = []
    for m in matches:
        if len(added) >= int(st.get("saved_keywords_max", 5)):
            break
        start, end = snap(tr["segments"], max(0.0, m["t"] - LEAD), min(dur, m["t_end"] + TAIL))
        if any(not (end < a - 5 or start > b + 5) for a, b in taken):
            continue
        taken.append((start, end))
        cid = f"{len(existing) + len(added) + 1:02d}"
        text = " ".join(w["w"] for w in tr["words"] if start <= w["s"] < end)
        title = make_title(text, [], "", cfg)
        progress(95, f"Making keyword Short {len(added) + 1}")
        w = tr["words"] if cfg["captions"]["enabled"] else []
        mp4, jpg = render_short(video, start, end, out / f"clip_{cid}.mp4", w, cfg, sw, sh)
        url = src_url
        if src_url and "youtube" in src_url:
            url = f"{src_url}{'&' if '?' in src_url else '?'}t={int(offset + start)}s"
        added.append({"id": cid, "file": mp4.name, "poster": jpg.name, "start": offset + start, "end": offset + end,
                      "src_start": round(start, 2), "src_end": round(end, 2),
                      "source_file": str(Path(video).resolve()), "length": round(end - start, 1), "score": 0,
                      "reasons": [f"saved word: '{m['query']}'"], "transcript": text, "title": title,
                      "description": make_description(title, cfg, url), "status": "pending",
                      "layout": cfg["layout"].get("id")})
    return added


def syncfix_search(cfg, sid):
    from .download import fix_sync
    out = cfg["paths"]["output_dir"] / sid
    data = load_json(out / "search.json")
    fixed = fix_sync(Path(data["source_file"]), cfg)
    if str(fixed) != data["source_file"]:
        data["source_file"] = str(fixed)
        save_json(out / "search.json", data)
    progress(100, "Stream converted")
