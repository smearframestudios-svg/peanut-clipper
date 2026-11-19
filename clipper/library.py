"""The finished Shorts on disk: list, decide, trim, export, and clean up (auto-delete)."""
import datetime as dt
import re
import shutil
import subprocess
from pathlib import Path

from .util import ROOT, load_json, probe, save_json

DONE = ("rejected", "uploaded", "exported")


def _jobs(cfg):
    return sorted(Path(cfg["paths"]["output_dir"]).glob("*/clips.json"))


def clips(cfg, status="pending"):
    out = []
    for f in _jobs(cfg):
        data = load_json(f)
        for c in data["clips"]:
            if c["status"] == status:
                out.append(dict(c, job=f.parent.name))
    return out


def counts(cfg):
    n = {"pending": 0, "approved": 0, "uploaded": 0, "exported": 0}
    for f in _jobs(cfg):
        for c in load_json(f)["clips"]:
            if c["status"] in n:
                n[c["status"]] += 1
    return n


def delete_files(job_dir, clip):
    for name in (clip.get("file"), clip.get("poster"), Path(clip.get("file", "x")).with_suffix(".ass").name):
        if name:
            (Path(job_dir) / name).unlink(missing_ok=True)
    clip["deleted"] = True


def prune(job_dir):
    """Remove a job folder once nothing in it is waiting for review or upload."""
    f = Path(job_dir) / "clips.json"
    data = load_json(f)
    if data and all(c["status"] in DONE and c.get("deleted") for c in data["clips"]):
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
        all_done = all(c["status"] in DONE for c in data["clips"])
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
        if status == "rejected" and cfg["settings"]["delete_rejected"]:
            delete_files(job_dir, c)
    save_json(f, data)
    cleanup_sources(cfg)
    prune(job_dir)


def after_upload(cfg, json_path, data, clip):
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


def source_info(cfg, job, cid):
    f, data, c = _find(cfg, job, cid)
    src = Path(c.get("source_file", ""))
    if not c.get("source_file") or not src.exists():
        return {"available": False}
    dur, w, h = probe(src)
    return {"available": True, "duration": dur, "start": c["src_start"], "end": c["src_end"],
            "file": c["file"], "poster": c["poster"], "title": c["title"]}


def rerender(cfg, job, cid, start, end):
    from .render import render_short
    from .transcribe import transcribe_range
    f, data, c = _find(cfg, job, cid)
    src = Path(c.get("source_file", ""))
    if not src.exists():
        raise SystemExit("[!] The full stream for this Short was already deleted, so it can't be re-cut.")
    dur, sw, sh = probe(src)
    start, end = max(0.0, float(start)), min(dur, float(end))
    if end - start < 3:
        raise SystemExit("[!] That's too short - make it at least 3 seconds.")
    print("@@ 10 Re-cutting the Short", flush=True)
    words = []
    if cfg["captions"]["enabled"]:
        cache = Path(data.get("source_dir") or f.parent) / "transcripts.json"
        words = transcribe_range(src, start, end - start, cfg, cache)["words"]
    ver = int(c.get("version", 1)) + 1
    name = f"clip_{cid}_v{ver}.mp4"
    print("@@ 40 Rendering", flush=True)
    mp4, jpg = render_short(src, start, end, f.parent / name, words, cfg, sw, sh)
    delete_files(f.parent, dict(c))
    shift = start - c["src_start"]
    c.update(file=mp4.name, poster=jpg.name, version=ver, src_start=round(start, 2), src_end=round(end, 2),
             start=round(c["start"] + shift, 2), end=round(c["start"] + shift + (end - start), 2),
             length=round(end - start, 1))
    c.pop("deleted", None)
    save_json(f, data)
    print("@@ 100 Short updated", flush=True)


def _safe(name):
    return re.sub(r'[<>:"/\\|?*]+', "", name).strip()[:80] or "clip"


def export_raw(cfg, job, cid, encoder=None):
    """Horizontal, full-quality cut (with a few seconds extra each side) for editing in Premiere."""
    st = cfg["settings"]
    f, data, c = _find(cfg, job, cid)
    src = Path(c.get("source_file", ""))
    if not src.exists():
        raise SystemExit("[!] The full stream for this Short was already deleted, so there's nothing to export.")
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
    v = (["-c:v", "h264_nvenc", "-preset", "p6", "-rc", "vbr", "-cq", "17", "-b:v", "0"] if enc == "h264_nvenc"
         else ["-c:v", "libx264", "-preset", "fast", "-crf", "16", "-threads", "4"])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-i", str(src), "-t", f"{b - a:.3f}",
                    "-map", "0:v:0", "-map", "0:a:0?"] + v + ["-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "320k",
                    "-movflags", "+faststart", str(out)], check=True)
    if st.get("export_vertical_too") and (f.parent / c["file"]).exists():
        shutil.copy2(f.parent / c["file"], out.with_name(out.stem + " (vertical).mp4"))
    print(f"  exported: {out}")
    c["status"] = "exported"
    c["exported_to"] = str(out)
    after_upload(cfg, f, data, c)
    return out
