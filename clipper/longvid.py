"""Long video (Make Shorts box > Make: Long video / Both): one 16:9 video of the best moments of a stream or of the
owner's own video, about as long as they asked for (8 / 10 / 15 / 20 minutes).

It finds moments the same way Shorts are found (chat, loudness, what's said), but longer (20-75 s), closer together
and more of them, then takes the best until the length is reached and puts them back in stream order. The result is
a compilation (compilations/<id>/, same store as the Compilations tab), so the owner trims, reorders, removes and
exports it there - one MP4 or a Premiere project.
"""
import copy
import shutil
import sys
from pathlib import Path

from . import compile as comp
from . import download
from .audio import loudness_per_sec
from .chat import load_chat
from .pipeline import check_video, fetch_source, progress, source_name
from .score import Detector
from .transcribe import transcribe_range
from .util import DATA, hms, save_json

MERGE_GAP = 8.0       # two picked moments closer than this become one
PAD_STEP = 5.0
MIN_LEN = 20.0        # no moment shorter than this        # widen moments this much per side per round when there aren't enough good ones


def _mmss(t):
    t = int(round(t))
    return f"{t // 60}:{t % 60:02d}"


def _total(ms):
    return sum(m["end"] - m["start"] for m in ms)


def _merge(ms):
    ms = sorted(ms, key=lambda m: m["start"])
    out = []
    for m in ms:
        if out and m["start"] - out[-1]["end"] <= MERGE_GAP:
            prev = out[-1]
            prev["end"] = max(prev["end"], m["end"])
            prev["score"] = max(prev["score"], m["score"])
            prev["text"] = (prev.get("text", "") + " " + m.get("text", "")).strip()
        else:
            out.append(dict(m))
    return out


def pick(cands, target, lo, hi):
    """The best moments until about `target` seconds, in stream order. Widens them if there aren't enough."""
    chosen = []
    for c in sorted(cands, key=lambda c: -c["score"]):
        if _total(chosen) >= target:
            break
        if any(c["start"] < m["end"] and m["start"] < c["end"] for m in chosen):
            continue
        a, b = max(lo, c["start"]), min(hi, c["end"])
        if b - a < MIN_LEN:                                   # near the start/end of the video: grow the other way
            a, b = (a, min(hi, a + MIN_LEN)) if a <= lo + 1 else (max(lo, b - MIN_LEN), b)
        chosen.append({"start": a, "end": b, "score": c["score"], "text": c.get("text", "")})
        chosen = _merge(chosen)
    rounds = 0
    while chosen and _total(chosen) < target and rounds < 12:      # widen each moment a little, both sides
        rounds += 1
        for m in chosen:
            m["start"] = max(lo, m["start"] - PAD_STEP)
            m["end"] = min(hi, m["end"] + PAD_STEP)
        chosen = _merge(chosen)
    return sorted(chosen, key=lambda m: m["start"])


def make(source, cfg, minutes=8, start=None, end=None):
    target = max(60, int(float(minutes) * 60))
    name = source_name(source)
    print(f"\n== Long video ({minutes} min) from {name}")
    src = fetch_source(source, cfg, start, end, None, None)
    video, offset, t0, t1, dl = src["video"], src["offset"], src["t0"], src["t1"], src["dl"]
    cache = src["cache"] or (DATA / "longvid_transcripts.json")
    duration, sw, sh = check_video(video, source)
    n = int(duration)
    lo, hi = float(t0 or 0), float(min(duration, t1 or duration))
    print(f"  video {sw}x{sh}, {hms(duration)} long; looking at {hms(lo)} - {hms(hi)}")

    if hi - lo <= target * 1.1:
        print(f"  the part to use is only {_mmss(hi - lo)}, so the long video is all of it")
        chosen = [{"start": lo, "end": hi, "score": 0, "text": ""}]
    else:
        progress(35, "Reading chat")
        chat = load_chat(src["chat_file"], offset=offset, duration=duration) if src["chat_file"] else []
        print(f"  chat messages: {len(chat)}" + ("" if chat else " (none - using audio + speech only)"))
        progress(40, "Listening for loud moments")
        loud = loudness_per_sec(video)
        c2 = copy.deepcopy(cfg)
        c2["detect"].update(clip_len_sec=45, min_len_sec=20, max_len_sec=75, tail_sec=5, spacing_sec=50,
                            candidates=max(20, min(80, int(target / 30 * 2.2))))
        det = Detector(c2)
        cands = det.candidates(n, chat, loud, t0, t1, min_score=0.0)
        print(f"  {len(cands)} candidate moments; transcribing them...")
        for i, c in enumerate(cands, 1):
            progress(45 + 30 * i / max(1, len(cands)), f"Checking moment {i} of {len(cands)}")
            a, b = max(0.0, c["start"] - 12), min(duration, c["end"] + 8)
            tr = transcribe_range(video, a, b - a, c2, cache)
            det.refine(c, tr)
        chosen = pick(cands, target, lo, hi)
        if not chosen:
            sys.exit("\n[!] Couldn't find any moments in that video.\n")
    total = _total(chosen)
    print(f"  picked {len(chosen)} moments, {_mmss(total)} in all (asked for {_mmss(target)})")

    title = name if not download.is_url(source) else (_stream_title(dl) or "Stream")
    c = comp.new(f"{title[:40]} - long video", goal=target)
    folder = comp._path(c["id"]).parent
    moments = []
    try:
        for i, m in enumerate(chosen, 1):
            progress(76 + 23 * i / len(chosen), f"Copying moment {i} of {len(chosen)} into the long video")
            mid, fname, poster, ca, fdur = comp.copy_range(cfg, folder, video, m["start"], m["end"])
            said = " ".join(m.get("text", "").split())
            moments.append({
                "mid": mid, "file": fname, "poster": poster,
                "title": (said[:70].strip() or f"Moment at {hms(offset + m['start'])}"),
                "query": "long video", "kind": "auto",
                "stream": source if download.is_url(source) else name, "stream_date": c["created"][:10],
                "stream_t": round(offset + m["start"], 2),
                "a": round(m["start"] - ca, 2), "b": round(min(fdur, m["end"] - ca), 2), "dur": round(fdur, 2),
                "added": c["created"]})
    except BaseException:
        shutil.rmtree(folder, ignore_errors=True)          # no half-made long video left behind
        raise
    c = comp.get(c["id"])
    c.update(moments=moments, made_from=source if download.is_url(source) else name, auto=True,
             source_file=str(Path(video).resolve()), source_offset=offset, source_w=sw, source_h=sh,
             source_link=source if download.is_url(source) else "")
    save_json(comp._path(c["id"]), c)
    save_json(DATA / "last_longvid.json", {"id": c["id"]})
    short = ""
    if total < target * 0.9:
        short = (" - the video is only that long" if hi - lo <= target * 1.1
                 else " - shorter than asked: there weren't enough good moments")
    progress(100, f"Long video ready: {len(moments)} moments, {_mmss(total)}{short}")
    return c["id"]


def _stream_title(dl):
    try:
        return (Path(dl) / "title.txt").read_text(encoding="utf-8").strip() if dl else ""
    except OSError:
        return ""
