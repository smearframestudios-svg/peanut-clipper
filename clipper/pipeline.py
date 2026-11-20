import datetime as dt
import shutil
import sys
from pathlib import Path

from . import download, twitch
from .audio import loudness_per_sec
from .chat import load_chat
from .render import render_short
from .score import Detector
from .titles import make_description, make_title
from .transcribe import transcribe_range
from .util import hms, load_json, probe, save_json, slug


def progress(pct, label):
    """Read by the app to draw the progress bar."""
    print(f"@@ {int(pct)} {label}", flush=True)


def _mark_processed(cfg, key):
    from .util import DATA
    done = set(load_json(DATA / "processed.json", []) or [])
    done.add(key)
    save_json(DATA / "processed.json", sorted(done))


def _job_dirs(cfg, name):
    job = f"{dt.datetime.now():%Y%m%d-%H%M}-{slug(name)}"
    work = cfg["paths"]["work_dir"] / job
    out = cfg["paths"]["output_dir"] / job
    work.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    return job, work, out


def process_vod(source, cfg, start=None, end=None, chat_file=None, keep=None, layout=None):
    from .util import apply_layout
    apply_layout(cfg, layout)
    name = source if download.is_url(source) else Path(source).stem
    job, work, out = _job_dirs(cfg, name)
    print(f"\n== Job {job}")
    t0, t1, offset = start, end, 0.0
    cache = work / "transcripts.json"
    progress(2, "Downloading the stream")
    dl = None
    if download.is_url(source):
        # downloads are kept per link + time range, so re-running the same command skips the download
        dl = cfg["paths"]["work_dir"] / "_downloads" / download.cache_key(source, start, end)
        dl.mkdir(parents=True, exist_ok=True)
        video = download.download_video(source, dl, cfg, start, end)
        if chat_file is None:
            chat_file = download.download_chat(source, dl, start, end)
        offset = start or 0.0      # downloaded file starts at --from
        t0 = t1 = None
        cache = dl / "transcripts.json"
    else:
        video = Path(source)
    try:
        duration, sw, sh = probe(video)
    except RuntimeError:
        bad = video
        if download.is_url(source):
            for f in bad.parent.glob("source.*"):
                f.unlink()
        sys.exit("\n[!] The video came out empty, so there's nothing to clip.\n"
                 "    If you used --from / --to, the video is probably shorter than that time range.\n"
                 "    Use a full stream replay (his channel -> Live tab), or run without --from/--to.\n")
    if duration < 60:
        sys.exit(f"\n[!] That video is only {int(duration)}s long. Use a full stream replay instead.\n")
    n = int(duration)
    print(f"  video {sw}x{sh}, {hms(duration)} long")

    progress(35, "Reading chat")
    chat = load_chat(chat_file, offset=offset, duration=duration) if chat_file else []
    print(f"  chat messages: {len(chat)}" + ("" if chat else " (none - using audio + speech only)"))
    progress(40, "Listening for loud moments")
    print("  measuring loudness...")
    loud = loudness_per_sec(video)

    det = Detector(cfg)
    cands = det.candidates(n, chat, loud, t0, t1)
    print(f"  {len(cands)} candidate moments; transcribing them...")
    for i, c in enumerate(cands, 1):
        progress(45 + 30 * i / max(1, len(cands)), f"Checking moment {i} of {len(cands)}")
        a = max(0.0, c["start"] - 12)
        b = min(duration, c["end"] + 8)
        tr = transcribe_range(video, a, b - a, cfg, cache)
        det.refine(c, tr)
        c["_words"] = tr["words"]
        print(f"   {i:>2}/{len(cands)}  {hms(c['start'])}  score {c['score']:>5}  {', '.join(c['reasons'])[:70]}")

    keep = keep or int(cfg["detect"]["keep"])
    best = sorted(cands, key=lambda c: -c["score"])[:keep]
    best.sort(key=lambda c: c["start"])
    src_url = source if download.is_url(source) else ""
    result = _render_all(best, video, out, job, cfg, sw, sh, src_url, offset, source_dir=dl)
    if cfg["settings"].get("saved_keywords"):
        from .search import add_keyword_clips
        data = load_json(out / "clips.json")
        extra = add_keyword_clips(cfg, out, video, cache, chat, offset, src_url, data["clips"])
        if extra:
            data["clips"] += extra
            save_json(out / "clips.json", data)
            print(f"  + {len(extra)} Shorts from your saved words")
        best = best + extra
    if dl is not None:
        _mark_processed(cfg, download.cache_key(source))
    shutil.rmtree(work, ignore_errors=True)
    if not best:
        shutil.rmtree(out, ignore_errors=True)
    progress(100, f"Done - {len(best)} Shorts ready to review")
    return result


def _render_all(cands, video, out, job, cfg, sw, sh, src_url, offset=0.0, source_dir=None):
    clips = []
    for i, c in enumerate(cands, 1):
        title = make_title(c.get("text", ""), c.get("tags"), c.get("hint", ""), cfg)
        fname = f"clip_{i:02d}.mp4"
        progress(75 + 24 * i / max(1, len(cands)), f"Making Short {i} of {len(cands)}")
        print(f"  rendering {fname}: {title}")
        mp4, jpg = render_short(video, c["start"], c["end"], out / fname, c.get("_words", []), cfg, sw, sh)
        url = src_url
        if src_url and "youtube" in src_url:
            url = f"{src_url}{'&' if '?' in src_url else '?'}t={int(offset + c['start'])}s"
        clips.append({
            "id": f"{i:02d}", "file": mp4.name, "poster": jpg.name,
            "start": c["start"] + offset, "end": c["end"] + offset,
            "src_start": c["start"], "src_end": c["end"], "source_file": str(Path(video).resolve()),
            "length": round(c["end"] - c["start"], 1),
            "score": c["score"], "reasons": c["reasons"], "transcript": c.get("text", ""),
            "title": title, "description": make_description(title, cfg, url),
            "status": "pending", "layout": cfg["layout"].get("id"),
        })
    save_json(out / "clips.json", {"job": job, "source": src_url or str(video), "clips": clips,
                                   "source_dir": str(source_dir) if source_dir else None,
                                   "created": dt.datetime.now().isoformat(timespec="seconds"),
                                   **download.stream_extras(source_dir)})
    print(f"\n  done -> {out}  ({len(clips)} Shorts)")
    return out


def process_twitch_clips(cfg, hours=24, top=10, layout=None):
    from .util import apply_layout
    apply_layout(cfg, layout)
    seen_path = cfg["paths"]["work_dir"] / "seen_twitch_clips.json"
    seen = set(load_json(seen_path, []))
    clips = [c for c in twitch.top_clips(cfg, hours, top * 3) if c["id"] not in seen]
    # skip near-duplicates (several viewers clipping the same moment)
    picked, spots = [], []
    for c in clips:
        spot = (c.get("video_id"), c.get("vod_offset"))
        if spot[1] is not None and any(s[0] == spot[0] and s[1] is not None and abs(s[1] - spot[1]) < 40
                                       for s in spots):
            continue
        spots.append(spot)
        picked.append(c)
        if len(picked) >= top:
            break
    if not picked:
        print("No new Twitch clips.")
        return None
    job, work, out = _job_dirs(cfg, "twitch-top-clips")
    print(f"\n== Job {job}: {len(picked)} top Twitch clips")
    det = Detector(cfg)
    items = []
    sw = sh = None
    for c in picked:
        print(f"  {c['view_count']:>6} views  {c['title']}")
        path = download.download_url(c["url"], work / f"{c['id']}.mp4")
        dur, sw, sh = probe(path)
        tr = transcribe_range(path, 0, dur, cfg, work / "transcripts.json")
        cand["_dur"] = dur
        cand = {"start": 0.0, "end": min(dur, cfg["detect"]["max_len_sec"]), "score": 0, "reasons": [], "peak": 0}
        det.refine(cand, tr)
        cand.update(start=0.0, end=min(dur, cfg["detect"]["max_len_sec"]))
        cand["reasons"].insert(0, f"{c['view_count']} views on Twitch (clipped by {c.get('creator_name', '?')})")
        cand["hint"] = c["title"]
        cand["_words"] = tr["words"]
        cand["_src"] = path
        cand["_url"] = c["url"]
        items.append(cand)
        seen.add(c["id"])
    # each Twitch clip is its own source file
    results = []
    for i, cand in enumerate(items, 1):
        _, sw, sh = probe(cand["_src"])
        title = make_title(cand.get("text", ""), cand.get("tags"), cand["hint"], cfg)
        fname = f"clip_{i:02d}.mp4"
        print(f"  rendering {fname}: {title}")
        mp4, jpg = render_short(cand["_src"], cand["start"], cand["end"], out / fname, cand["_words"], cfg, sw, sh)
        results.append({"id": f"{i:02d}", "file": mp4.name, "poster": jpg.name, "start": 0, "end": cand["end"],
                        "src_start": cand["start"], "src_end": cand["end"],
                        "source_file": str(Path(cand["_src"]).resolve()),
                        "length": round(cand["end"], 1), "score": cand["score"], "reasons": cand["reasons"],
                        "transcript": cand.get("text", ""), "title": title,
                        "description": make_description(title, cfg), "status": "pending",
                        "layout": cfg["layout"].get("id"),
                        "twitch_url": cand["_url"]})
    save_json(out / "clips.json", {"job": job, "source": "twitch top clips", "clips": results,
                                   "source_dir": str(work),
                                   "created": dt.datetime.now().isoformat(timespec="seconds")})
    save_json(seen_path, sorted(seen))
    print(f"\n  done -> {out}")
    return out
