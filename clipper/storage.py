"""Storage: what's using space in the Peanut Clipper folder, and the auto-delete rules.

Rules (Settings -> Auto-delete):
- Downloaded streams (and the app's copy of videos uploaded on Make Shorts): deleted once every Short from them is done, or after keep_source_days - including downloads
  no Short was ever made from (failed/cancelled runs, unused live recordings, video pieces for sound-only searches).
- The app's copy of Shorts exported to Premiere: deleted after delete_exported_days (right away if "Delete once
  they're on YouTube" is on, as before).
- Keyword searches: removed after search_keep_days, unless a Short made from them is still in Review / Approved.
- Shorts still in Review or Approved are never deleted automatically.
"""
import datetime as dt
import os
import re
import shutil
import time
from pathlib import Path

from .util import ROOT, load_json, save_json

PENDING = ("pending", "approved")


def _size(p):
    p = Path(p)
    if p.is_file():
        return p.stat().st_size
    total = 0
    for root, _, files in os.walk(p):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total


def _newest(p):
    """Last time anything in the folder changed (seconds since epoch)."""
    newest = Path(p).stat().st_mtime
    for root, _, files in os.walk(p):
        for f in files:
            try:
                newest = max(newest, os.path.getmtime(os.path.join(root, f)))
            except OSError:
                pass
    return newest


def _days(ts):
    return (time.time() - ts) / 86400


def _date(ts):
    return dt.datetime.fromtimestamp(ts).strftime("%b %d").replace(" 0", " ")


def _inside(p, base):
    try:
        return Path(base).resolve() in Path(p).resolve().parents
    except OSError:
        return False


def _jobs(cfg):
    """Every Make Shorts run / keyword search: (folder, clips.json data, is_search)."""
    out = []
    for f in sorted(Path(cfg["paths"]["output_dir"]).glob("*/clips.json")):
        d = load_json(f)
        if d:
            out.append((f.parent, d, (f.parent / "search.json").exists()))
    return out


def _live_folder():
    try:
        from . import live
        st = live.state()
        return st.get("job_dir") if st.get("alive") else None
    except Exception:  # noqa: BLE001
        return None


def _downloads(cfg):
    """Each folder in work/_downloads with what it is, who uses it, and how old it is."""
    base = Path(cfg["paths"]["work_dir"]) / "_downloads"
    if not base.is_dir():
        return []
    users = {}
    for folder, d, is_search in _jobs(cfg):
        sd = d.get("source_dir")
        if sd:
            users.setdefault(str(Path(sd).resolve()), []).append((folder, d, is_search))
    for f in Path(cfg["paths"]["output_dir"]).glob("*/search.json"):
        s = load_json(f) or {}
        if s.get("source_dir"):
            users.setdefault(str(Path(s["source_dir"]).resolve()), [])
    live_dir = _live_folder()
    out = []
    for p in sorted(base.iterdir()):
        if not p.is_dir():
            continue
        key = str(p.resolve())
        try:
            title = (p / "title.txt").read_text(encoding="utf-8").strip()
        except OSError:
            title = ""
        piece = bool(re.search(r"_\d+-(\d+|end)$", p.name))     # cache_key with a range
        live_rec = (p / "recorded_live").exists()
        jobs = users.get(key, [])
        waiting = sum(1 for _, d, _ in jobs for c in d["clips"] if c["status"] in PENDING)
        made = sum(len(d["clips"]) for _, d, _ in jobs)
        if piece:
            what, note = f"Part of a stream: \"{title}\"" if title else "Part of a stream", ""
        elif (p / "uploaded").exists():
            what, note = f"Your video: \"{title}\"" if title else "Your uploaded video", "the app's copy, your original is untouched"
        elif live_rec:
            what, note = f"Live recording: \"{title}\"" if title else "Live recording", ""
        else:
            what, note = f"Stream: \"{title}\"" if title else f"Stream {p.name}", ""
        if waiting:
            note = (note + ", " if note else "") + f"{waiting} Short{'s' if waiting != 1 else ''} still in Review or Approved"
        elif not jobs and not piece:
            note = (note + ", " if note else "") + ("never used" if live_rec else "no Shorts made from it")
        elif jobs and not waiting:
            note = (note + ", " if note else "") + "everything from it is done"
        newest = _newest(p)
        out.append({"kind": "download", "path": str(p), "name": what, "note": note, "date": _date(newest),
                    "age_days": round(_days(newest), 1), "size": _size(p), "jobs": [str(j[0]) for j in jobs],
                    "all_done": bool(jobs) and not waiting and made > 0, "busy": key == str(Path(live_dir).resolve()) if live_dir else False})
    return out


def scan(cfg):
    """Sizes per area + the biggest items, for Settings -> Storage."""
    work, out_dir = Path(cfg["paths"]["work_dir"]), Path(cfg["paths"]["output_dir"])
    st = cfg["settings"]
    exports = Path(st.get("export_folder") or (ROOT / "exports"))
    comps = ROOT / "compilations"
    downloads = _downloads(cfg)
    items = list(downloads)
    for folder, d, is_search in _jobs(cfg):
        waiting = sum(1 for c in d["clips"] if c["status"] in PENDING)
        newest = _newest(folder)
        label = ("Keyword search" if is_search else "App Shorts from a run") + f" ({d.get('stream_title') or folder.name})"
        items.append({"kind": "job", "path": str(folder), "name": label,
                      "note": f"{waiting} Short{'s' if waiting != 1 else ''} still in Review or Approved" if waiting else "everything in it is done",
                      "date": _date(newest), "age_days": round(_days(newest), 1), "size": _size(folder), "waiting": waiting})
    dl_total = sum(i["size"] for i in downloads)
    other_work = max(0, _size(work) - dl_total) if work.is_dir() else 0
    areas = [{"key": "downloads", "name": "Downloaded streams", "size": dl_total + other_work, "path": str(work / "_downloads")},
             {"key": "shorts", "name": "App Shorts and searches", "size": _size(out_dir) if out_dir.is_dir() else 0, "path": str(out_dir)},
             {"key": "exports", "name": "Exports", "size": _size(exports) if exports.is_dir() else 0, "path": str(exports)},
             {"key": "compilations", "name": "Compilations", "size": _size(comps) if comps.is_dir() else 0, "path": str(comps)}]
    du = shutil.disk_usage(ROOT)
    items.sort(key=lambda i: i["size"], reverse=True)
    return {"root": str(ROOT), "areas": areas, "total": sum(a["size"] for a in areas), "free": du.free,
            "drive": str(Path(ROOT).anchor), "items": items[:25], "plan": plan(cfg)}


# ------------------------------------------------------------------ auto-delete
def plan(cfg):
    """Everything the auto-delete rules would remove right now: [{path, name, size, why}]."""
    st = cfg["settings"]
    todo = []
    if st.get("delete_source", True):
        days = float(st.get("keep_source_days", 3))
        for d in _downloads(cfg):
            if d["busy"] or d["age_days"] < 0.05:          # recording right now / being written
                continue
            if d["all_done"] or d["age_days"] >= days:
                why = "everything from it is done" if d["all_done"] else f"older than {days:g} days"
                todo.append({"kind": "download", "path": d["path"], "name": d["name"], "size": d["size"], "why": why})
    if st.get("delete_exported", True):
        days = float(st.get("delete_exported_days", 3))
        for folder, data, _ in _jobs(cfg):
            for c in data["clips"]:
                if c["status"] == "exported" and not c.get("deleted") and c.get("file"):
                    f = folder / c["file"]
                    if f.exists() and _days(f.stat().st_mtime) >= days:
                        todo.append({"kind": "exported", "path": str(f), "job": str(folder), "id": c["id"],
                                     "name": f"App copy of \"{c['title']}\"", "size": _size(f),
                                     "why": f"exported to Premiere over {days:g} days ago"})
    if st.get("delete_searches", True):
        days = float(st.get("search_keep_days", 14))
        for folder, data, is_search in _jobs(cfg):
            if is_search and not any(c["status"] in PENDING for c in data["clips"]) and _days(_newest(folder)) >= days:
                todo.append({"kind": "search", "path": str(folder), "name": f"Keyword search ({data.get('stream_title') or folder.name})",
                             "size": _size(folder), "why": f"older than {days:g} days"})
    return todo


def _mark_source_gone(cfg, src):
    for folder, data, _ in _jobs(cfg):
        if data.get("source_dir") and str(Path(data["source_dir"]).resolve()) == str(Path(src).resolve()):
            data["source_deleted"] = True
            save_json(folder / "clips.json", data)


def delete_item(cfg, item):
    """Delete one download / job folder / exported app copy - only ever inside the app's own folders."""
    from .library import delete_files, prune
    from .util import safe_unlink
    p = Path(item["path"])
    work, out_dir = Path(cfg["paths"]["work_dir"]), Path(cfg["paths"]["output_dir"])
    kind = item.get("kind")
    if kind == "download" and _inside(p, work / "_downloads") and p.is_dir():
        if _live_folder() and str(p.resolve()) == str(Path(_live_folder()).resolve()):
            raise SystemExit("[!] That one is being recorded right now.")
        shutil.rmtree(p, ignore_errors=True)
        _mark_source_gone(cfg, p)
        return True
    if kind in ("job", "search") and _inside(p, out_dir) and p.is_dir():
        shutil.rmtree(p, ignore_errors=True)
        return True
    if kind == "exported" and _inside(p, out_dir):
        job = Path(item["job"])
        data = load_json(job / "clips.json")
        for c in (data or {}).get("clips", []):
            if c["id"] == item["id"]:
                delete_files(job, c)
        if data:
            save_json(job / "clips.json", data)
            prune(job)
        else:
            safe_unlink(p)
        return True
    return False


def auto_clean(cfg, quiet=True):
    """Apply the rules (app start, after Reject/upload/export, nightly). Returns (count, bytes freed)."""
    n = freed = 0
    for item in plan(cfg):
        try:
            if delete_item(cfg, item):
                n += 1
                freed += item["size"]
                if not quiet:
                    print(f"  deleted: {item['name']} ({item['why']})")
        except (OSError, SystemExit):
            pass
    from .library import prune
    for folder, _, is_search in _jobs(cfg):      # job folders that are completely done
        if not is_search:
            prune(folder)
    return n, freed
