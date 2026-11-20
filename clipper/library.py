"""The finished Shorts on disk: list, decide, trim, export, and clean up (auto-delete)."""
import json
import datetime as dt
import re
import shutil
import subprocess
from pathlib import Path

from .util import DATA, ROOT, load_json, probe, safe_unlink, save_json

DONE = ("rejected", "uploaded", "exported")


def _jobs(cfg):
    return sorted(Path(cfg["paths"]["output_dir"]).glob("*/clips.json"))


def clips(cfg, status="pending"):
    out = []
    for f in _jobs(cfg):
        data = load_json(f)
        for c in data["clips"]:
            if c["status"] == status:
                out.append(dict(c, job=f.parent.name, **stream_info(data, c)))
    return out


# ------------------------------------------------------------------ where a Short came from in the stream
def _video_id(url):
    import re
    m = re.search(r"(?:v=|youtu\.be/|/live/|/shorts/)([\w-]{11})", url or "")
    return m.group(1) if m else ""


def stream_link(url, t):
    """A link that opens the stream at second t (YouTube or Twitch), or '' for local files."""
    import re
    t = max(0, int(t))
    vid = _video_id(url)
    if vid:
        return f"https://www.youtube.com/watch?v={vid}&t={t}s"
    m = re.search(r"twitch\.tv/videos/(\d+)", url or "")
    if m:
        return f"https://www.twitch.tv/videos/{m.group(1)}?t={t // 3600}h{t % 3600 // 60}m{t % 60}s"
    return ""


def stream_info(data, c):
    """Where this Short is in the original stream (seconds as on YouTube/Twitch) + a link that opens it there."""
    src = data.get("source") or ""
    is_url = src.startswith(("http://", "https://"))
    shift = float(data.get("stream_offset") or 0)
    s, e = float(c.get("start", 0)) + shift, float(c.get("end", 0)) + shift
    created = (data.get("created") or "")[:10]
    return {"stream_start": round(s, 2), "stream_end": round(e, 2), "stream_link": stream_link(src, s) if is_url else "",
            "stream_url": src if is_url else "", "stream_title": data.get("stream_title") or ("" if is_url else Path(src).name),
            "stream_date": created}


HISTORY = DATA / "history.json"
THUMBS = DATA / "history"


def history_add(job_dir, data, c):
    """Keep a permanent record of a finished Short (uploaded / exported / rejected), even after its files are deleted."""
    job_dir = Path(job_dir)
    key = f"{data.get('job') or job_dir.name}:{c['id']}"
    info = stream_info(data, c)
    thumb = ""
    p = job_dir / (c.get("poster") or "")
    if c.get("poster") and p.is_file():
        THUMBS.mkdir(parents=True, exist_ok=True)
        thumb = key.replace(":", "_") + ".jpg"
        try:
            shutil.copy2(p, THUMBS / thumb)
        except OSError:
            thumb = ""
    entry = dict(info, key=key, title=c.get("title", ""), status=c["status"],
                 when=dt.datetime.now().isoformat(timespec="seconds"), transcript=(c.get("transcript") or "")[:500],
                 youtube_id=c.get("youtube_id", ""), publish_at=c.get("publish_at", ""),
                 exported_to=c.get("exported_to", ""), length=c.get("length"), thumb=thumb,
                 source_file=c.get("source_file", ""),
                 file_shift=round(info["stream_start"] - float(c.get("src_start", c.get("start", 0))), 3))
    hist = [h for h in (load_json(HISTORY, []) or []) if h.get("key") != key]
    hist.append(entry)
    save_json(HISTORY, hist[-5000:])


def history(cfg):
    hist = load_json(HISTORY, []) or []
    for h in hist:
        h["available"] = bool(h.get("source_file")) and Path(h["source_file"]).is_file()
    return list(reversed(hist))


def history_shot(cfg, key, at):
    """Screenshot of the full stream frame at `at` (stream seconds) - while the stream is still on the PC."""
    from .render import snapshot as shot
    h = next((x for x in load_json(HISTORY, []) or [] if x.get("key") == key), None)
    if not h:
        raise SystemExit("[!] That Short isn't in the history.")
    src = Path(h.get("source_file") or "")
    if not src.is_file():
        raise SystemExit("[!] The stream was already deleted from this PC. Use \"Open stream there\" and pause it on YouTube.")
    dur, sw, sh = probe(src)
    t = min(max(0.0, at - float(h.get("file_shift") or 0)), max(0.0, dur - 0.05))
    folder = screenshot_folder(cfg)
    a = int(at)
    base = f"{_safe(h['title'])} - stream {a // 3600}h{a % 3600 // 60:02d}m{a % 60:02d}s"
    out = folder / f"{base}.png"
    n = 2
    while out.exists():
        out = folder / f"{base} ({n}).png"
        n += 1
    return shot(src, t, out, cfg, sw, sh, None, vertical=False)


def counts(cfg):
    n = {"pending": 0, "approved": 0, "uploaded": 0, "exported": 0}
    for f in _jobs(cfg):
        for c in load_json(f)["clips"]:
            if c["status"] in n:
                n[c["status"]] += 1
    return n


def delete_files(job_dir, clip):
    f = clip.get("file") or ""
    for name in (f, clip.get("poster"), Path(f).with_suffix(".ass").name if f else ""):
        if name:
            safe_unlink(Path(job_dir) / name)     # in use (preview open)? deleted later instead of failing
    clip["deleted"] = True


def prune(job_dir):
    """Remove a job folder once nothing in it is waiting for review or upload."""
    f = Path(job_dir) / "clips.json"
    data = load_json(f)
    if data and data["clips"] and not (Path(job_dir) / "search.json").exists() and \
            all(c["status"] in DONE and c.get("deleted") for c in data["clips"]):
        _delete_source(data)
        shutil.rmtree(job_dir, ignore_errors=True)


def _delete_source(data):
    sd = data.get("source_dir")
    if sd and Path(sd).exists():
        work = (ROOT / "work").resolve()
        p = Path(sd).resolve()
        if work in p.parents:           # only ever delete things the app downloaded itself
            shutil.rmtree(p, ignore_errors=True)
            print(f"  deleted downloaded source: {p.name}")
    data["source_deleted"] = True


def cleanup_sources(cfg):
    """Delete a downloaded stream once all its Shorts are decided, or after N days."""
    st = cfg["settings"]
    if not st["delete_source"]:
        return
    days = float(st.get("keep_source_days", 3))
    for f in _jobs(cfg):
        data = load_json(f)
        if data.get("source_deleted") or not data.get("source_dir"):
            continue
        all_done = bool(data["clips"]) and all(c["status"] in DONE for c in data["clips"]) \
            and not (f.parent / "search.json").exists()
        try:
            age = (dt.datetime.now() - dt.datetime.fromisoformat(data.get("created", ""))).days
        except ValueError:
            age = 0
        if all_done or age >= days:
            _delete_source(data)
            save_json(f, data)


def decide(cfg, job, cid, status, title=None):
    job_dir = Path(cfg["paths"]["output_dir"]) / job
    f = job_dir / "clips.json"
    data = load_json(f)
    for c in data["clips"]:
        if c["id"] != cid:
            continue
        c["status"] = status
        new = (title or "").strip()
        if new and new != c["title"]:
            c["description"] = c["description"].replace(c["title"], new, 1)
            c["title"] = new
        if status == "rejected":
            history_add(job_dir, data, c)
            if cfg["settings"]["delete_rejected"]:
                delete_files(job_dir, c)
    save_json(f, data)
    cleanup_sources(cfg)
    prune(job_dir)


def after_upload(cfg, json_path, data, clip):
    history_add(Path(json_path).parent, data, clip)
    if cfg["settings"]["delete_uploaded"]:
        delete_files(json_path.parent, clip)
    save_json(json_path, data)
    cleanup_sources(cfg)
    prune(json_path.parent)


def _find(cfg, job, cid):
    f = Path(cfg["paths"]["output_dir"]) / job / "clips.json"
    data = load_json(f)
    for c in data["clips"]:
        if c["id"] == cid:
            return f, data, c
    raise SystemExit(f"[!] Short {cid} not found")


def edit_win(c, start=None, end=None):
    """The converted part of the stream around this Short, if it's there (and covers start..end): (file, off, end)."""
    w = c.get("edit_win")
    if not w or not Path(w["file"]).is_file():
        return None
    if start is not None and (start < w["off"] - 0.05 or end > w["end"] + 0.05):
        return None
    return Path(w["file"]), w["off"], w["end"]


def save_markers(cfg, job, cid, markers):
    """Trim-editor markers for one Short: seconds in the stream, sorted, at most 200."""
    f, data, c = _find(cfg, job, cid)
    c["markers"] = sorted({round(float(t), 2) for t in markers if float(t) >= 0})[:200]
    save_json(f, data)


def clean_sections(sections):
    """Trim-editor sections for one Short: seconds in the stream, each with a look and a banner spot."""
    from .render import BANNERS, LOOKS
    out = []
    for sec in (sections or [])[:100]:
        a, b = round(float(sec["start"]), 2), round(float(sec["end"]), 2)
        if b - a < 0.1:
            continue
        item = {"start": a, "end": b,
                "look": sec.get("look") if sec.get("look") in LOOKS else "normal",
                "banner": sec.get("banner") if sec.get("banner") in BANNERS else "layout"}
        bx = sec.get("box")
        if isinstance(bx, dict) and item["look"] != "normal":
            w, h = (max(0.02, min(1.0, float(bx.get(q, 0.5)))) for q in ("w", "h"))
            item["box"] = {"w": w, "h": h, "x": max(0.0, min(1.0 - w, float(bx.get("x", 0)))),
                           "y": max(0.0, min(1.0 - h, float(bx.get("y", 0))))}
        out.append(item)
    return sorted(out, key=lambda x: x["start"])


def save_sections(cfg, job, cid, sections):
    f, data, c = _find(cfg, job, cid)
    c["sections"] = clean_sections(sections)
    save_json(f, data)


def source_info(cfg, job, cid):
    f, data, c = _find(cfg, job, cid)
    src = Path(c.get("source_file", ""))
    if not c.get("source_file") or not src.exists():
        return {"available": False}
    from .download import needs_sync_fix
    info = {"available": True, "layout": c.get("layout"), "framing": c.get("framing"), "markers": c.get("markers", []), "sections": c.get("sections", []), "start": c["src_start"], "end": c["src_end"],
            "file": c["file"], "poster": c["poster"], "title": c["title"], "offset": 0}
    if needs_sync_fix(src):
        win = edit_win(c)
        want = float(cfg["settings"].get("edit_window_min", 6)) * 60
        # none yet, or the owner asked for more minutes than were converted last time: convert again
        if not win or (win[2] - win[1]) < min(want, probe(src)[0]) - 30:
            return dict(info, needs_sync=True)
        # the editor works inside the converted part: times go out and come back with the offset
        return dict(info, needs_sync=False, offset=win[1], duration=win[2] - win[1])
    dur, w, h = probe(src)
    return dict(info, needs_sync=False, duration=dur)


def _synced_source(cfg, f, data, src):
    """Older partial downloads may have audio out of sync; fix once and point every Short at it."""
    from .download import fix_sync, needs_sync_fix
    if not needs_sync_fix(src):
        return src
    new = fix_sync(src, cfg)
    if str(new) != str(src):
        for c in data["clips"]:
            if c.get("source_file") == str(src):
                c["source_file"] = str(new)
        save_json(f, data)
    return new


def syncfix(cfg, job, cid):
    """Convert only the half hour around this Short so the editor opens in a minute or two."""
    from .download import edit_window, needs_sync_fix
    f, data, c = _find(cfg, job, cid)
    src = Path(c.get("source_file", ""))
    info = source_info(cfg, job, cid)
    if needs_sync_fix(src) and info.get("needs_sync"):
        out = src.parent / f"edit_{cid}.mp4"
        file, off, end = edit_window(src, c["src_start"], c["src_end"], cfg, out, cfg["settings"].get("edit_window_min", 6))
        c["edit_win"] = {"file": str(file), "off": off, "end": end}
        save_json(f, data)
    print("@@ 100 Ready - opening the editor", flush=True)


def clean_framing(fr):
    """A Short's own framing: style, Peanut height and the two boxes (0..1 of the stream frame)."""
    out = {"mode": fr.get("mode") if fr.get("mode") in ("stack", "single", "blurfit") else "stack",
           "top_height": max(300, min(1600, int(fr.get("top_height", 760))))}
    for k in ("avatar", "gameplay"):
        b = fr.get(k) or {}
        w, h = (max(0.02, min(1.0, float(b.get(q, 0.5)))) for q in ("w", "h"))
        out[k] = {"w": w, "h": h, "x": max(0.0, min(1.0 - w, float(b.get("x", 0)))), "y": max(0.0, min(1.0 - h, float(b.get("y", 0))))}
    return out


def rerender(cfg, job, cid, start, end, layout=None, framing=None, sections=None):
    from .render import render_short
    from .transcribe import transcribe_range
    from .util import apply_layout
    f, data, c = _find(cfg, job, cid)
    c["layout"] = apply_layout(cfg, layout or c.get("layout"))
    if framing == "none":
        c.pop("framing", None)                 # back to the layout's framing
    elif framing:
        c["framing"] = clean_framing(json.loads(framing) if isinstance(framing, str) else framing)
    if c.get("framing"):
        cfg["layout"].update(c["framing"])     # this Short's own boxes win over the layout's
    if sections is not None:
        c["sections"] = clean_sections(json.loads(sections) if isinstance(sections, str) else sections)
    src = Path(c.get("source_file", ""))
    if not src.exists():
        raise SystemExit("[!] The full stream for this Short was already deleted, so it can't be re-cut.")
    from .download import needs_sync_fix
    full = src
    off = 0.0
    win = edit_win(c, float(start), float(end)) if needs_sync_fix(src) else None
    if win:
        src, off = win[0], win[1]          # render from the converted part around the Short (no full conversion)
    else:
        src = full = _synced_source(cfg, f, data, src)
    dur, sw, sh = probe(src)
    start, end = max(off, float(start)), min(off + dur, float(end))
    if end - start < 3:
        raise SystemExit("[!] That's too short - make it at least 3 seconds.")
    print("@@ 10 Re-cutting the Short", flush=True)
    words = []
    if cfg["captions"]["enabled"]:
        cache = Path(data.get("source_dir") or f.parent) / "transcripts.json"
        words = transcribe_range(full, start, end - start, cfg, cache)["words"]
        if off:
            words = [dict(w, s=w["s"] - off, e=w["e"] - off) for w in words]
    ver = int(c.get("version", 1)) + 1
    name = f"clip_{cid}_v{ver}.mp4"
    print("@@ 40 Rendering", flush=True)
    secs = [dict(x, start=x["start"] - off, end=x["end"] - off) for x in c.get("sections", [])]
    mp4, jpg = render_short(src, start - off, end - off, f.parent / name, words, cfg, sw, sh, secs)
    old = dict(c)
    shift = start - c["src_start"]
    c.update(file=mp4.name, poster=jpg.name, version=ver, src_start=round(start, 2), src_end=round(end, 2),
             start=round(c["start"] + shift, 2), end=round(c["start"] + shift + (end - start), 2),
             length=round(end - start, 1))
    c.pop("deleted", None)
    save_json(f, data)
    if old.get("file") != c["file"]:
        delete_files(f.parent, old)           # the previous version, only once the new one is saved
    print("@@ 100 Short updated", flush=True)


def snapshot(cfg, job, cid, at, vertical=True, layout=None, framing=None, sections=None):
    """Screenshot of the frame at `at` (seconds in the stream) as a full-size PNG in the export folder."""
    from .download import needs_sync_fix
    from .render import snapshot as shot
    from .util import apply_layout
    st = cfg["settings"]
    f, data, c = _find(cfg, job, cid)
    apply_layout(cfg, layout or c.get("layout"))
    fr = c.get("framing") if framing is None else (None if framing == "none" else clean_framing(framing))
    if fr:
        cfg["layout"].update(fr)
    src = Path(c.get("source_file", ""))
    if not src.is_file():
        raise SystemExit("[!] The full stream for this Short was already deleted.")
    off = 0.0
    win = edit_win(c, at, at) if needs_sync_fix(src) else None
    if win:
        src, off = win[0], win[1]
    dur, sw, sh = probe(src)
    secs = clean_sections(c.get("sections", []) if sections is None else sections)
    sec = next((x for x in secs if x["start"] <= at < x["end"]), None)
    folder = screenshot_folder(cfg)
    m, s_ = divmod(max(0.0, at - c["src_start"]), 60)
    base = f"{_safe(c['title'])} - {int(m)}m{s_:04.1f}s" + (" (Short)" if vertical else " (stream)")
    out = folder / f"{base}.png"
    n = 2
    while out.exists():
        out = folder / f"{base} ({n}).png"
        n += 1
    shot(src, min(max(0.0, at - off), max(0.0, dur - 0.05)), out, cfg, sw, sh, sec, vertical)
    return out


def screenshot_folder(cfg):
    """Where screenshots go: the Screenshot folder setting, else <Export folder>\\Screenshots."""
    st = cfg["settings"]
    folder = Path(st.get("screenshot_folder") or Path(st.get("export_folder") or (ROOT / "exports")) / "Screenshots")
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _safe(name):
    return re.sub(r'[<>:"/\\|?*]+', "", name).strip()[:80] or "clip"


def export_raw(cfg, job, cid, encoder=None):
    """Horizontal, full-quality cut (with a few seconds extra each side) for editing in Premiere."""
    st = cfg["settings"]
    f, data, c = _find(cfg, job, cid)
    src = Path(c.get("source_file", ""))
    if not src.exists():
        raise SystemExit("[!] The full stream for this Short was already deleted, so there's nothing to export.")
    src = _synced_source(cfg, f, data, src)
    folder = Path(st.get("export_folder") or (ROOT / "exports"))
    folder.mkdir(parents=True, exist_ok=True)
    dur, _, _ = probe(src)
    pad = float(st.get("export_handles_sec", 3))
    a, b = max(0.0, c["src_start"] - pad), min(dur, c["src_end"] + pad)
    stamp = dt.datetime.now().strftime("%Y-%m-%d")
    out = folder / f"{stamp} - {_safe(c['title'])}.mp4"
    n = 2
    while out.exists():
        out = folder / f"{stamp} - {_safe(c['title'])} ({n}).mp4"
        n += 1
    enc = cfg.get("render_encoder")
    # Premiere-friendly: plain H.264 High profile, constant frame rate, 48 kHz stereo AAC
    v = (["-c:v", "h264_nvenc", "-preset", "p6", "-profile:v", "high", "-rc", "vbr", "-cq", "17", "-b:v", "0",
          "-bf", "2", "-b_ref_mode", "disabled"] if enc == "h264_nvenc"
         else ["-c:v", "libx264", "-preset", "fast", "-profile:v", "high", "-crf", "16", "-threads", "4"])
    v += ["-fps_mode", "cfr"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-i", str(src), "-t", f"{b - a:.3f}",
                    "-map", "0:v:0", "-map", "0:a:0?"] + v + ["-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2",
                    "-movflags", "+faststart", str(out)], check=True)
    if st.get("export_vertical_too") and (f.parent / c["file"]).exists():
        shutil.copy2(f.parent / c["file"], out.with_name(out.stem + " (vertical).mp4"))
    print(f"  exported: {out}")
    c["status"] = "exported"
    c["exported_to"] = str(out)
    after_upload(cfg, f, data, c)
    return out
