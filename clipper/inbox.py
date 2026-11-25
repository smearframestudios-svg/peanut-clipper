"""Auto-clip folder (Make Shorts > From your own video): every video put in the owner's inbox folder is made
into Shorts on its own - while the app is open (app.inbox_watcher starts `python -m clipper inbox --one` when
nothing else is running) and in the nightly auto run (auto.run_auto calls run_all).

Each video is copied into work/_downloads/upload-<name>-u<time>/ exactly like an uploaded video, so re-cuts and
Storage clean-up work the same. Afterwards the original is moved to <inbox>\\Done, deleted, or left where it is
(setting watch_after: move / delete / keep). What happened to each file is kept in data/inbox.json, so a file is
never clipped twice and a failed one isn't retried until it changes.
"""
import datetime as dt
import hashlib
import os
import shutil
import sys
import time
from pathlib import Path

from .util import DATA, load_json, save_json, slug

VIDEO_TYPES = (".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi", ".ts", ".flv", ".wmv", ".mts")
SETTLE_SEC = 30          # a file that changed in the last 30 s is probably still being copied in
STATE = DATA / "inbox.json"
CLAIMS = DATA / "inbox_claims"


def default_folder():
    return str(Path.home() / "Videos" / "Peanut Clipper inbox")


def folder(cfg):
    return Path(cfg["settings"].get("watch_folder") or default_folder())


def new_upload_folder(cfg, name):
    """work/_downloads/upload-<name>-u<time>/ with title.txt + the `uploaded` marker (shared with uploads)."""
    base = Path(cfg["paths"]["work_dir"]) / "_downloads"
    base.mkdir(parents=True, exist_ok=True)
    f = base / f"upload-{slug(Path(name).stem, 30)}-u{dt.datetime.now():%Y%m%d%H%M%S%f}"
    f.mkdir(parents=True, exist_ok=True)
    (f / "title.txt").write_text(Path(name).stem, encoding="utf-8")
    (f / "uploaded").write_text(name, encoding="utf-8")
    return f


def _key(p, stat=None):
    stat = stat or p.stat()
    return f"{p.name}|{stat.st_size}|{int(stat.st_mtime)}"


def _state():
    s = load_json(STATE, {}) or {}
    s.setdefault("files", {})
    return s


def _set(key, **kw):
    s = _state()
    s["files"].setdefault(key, {}).update(kw)
    if kw.get("status") in ("done", "failed"):
        s["last"] = key
    files = s["files"]
    if len(files) > 500:            # keep the list from growing forever
        for k in sorted(files, key=lambda k: files[k].get("at", ""))[:len(files) - 500]:
            files.pop(k, None)
    save_json(STATE, s)


def videos(cfg):
    """Video files sitting in the inbox (top level only - Done stays out), oldest first."""
    f = folder(cfg)
    if not f.is_dir():
        return []
    out = []
    for p in f.iterdir():
        try:
            if p.is_file() and p.suffix.lower() in VIDEO_TYPES and not p.name.startswith((".", "~")):
                out.append((p, p.stat()))
        except OSError:
            pass
    return sorted(out, key=lambda x: x[1].st_mtime)


def ready(cfg):
    """Videos that are finished copying in and haven't been clipped (or failed) yet."""
    files = _state()["files"]
    now = time.time()
    out = []
    for p, st in videos(cfg):
        k = _key(p, st)
        if k in files and files[k].get("status") in ("done", "failed", "making"):
            continue
        if now - st.st_mtime < SETTLE_SEC or st.st_size == 0:
            continue
        if _claimed(k):
            continue
        out.append(p)
    return out


def _claim_file(k):
    return CLAIMS / (hashlib.sha1(k.encode()).hexdigest()[:16] + ".claim")


def _claimed(k):
    c = _claim_file(k)
    try:
        return time.time() - c.stat().st_mtime < 12 * 3600       # older = left over from a crash
    except OSError:
        return False


def _claim(k):
    """True if this process may clip the file (the app and the scheduled auto run never take the same one)."""
    CLAIMS.mkdir(parents=True, exist_ok=True)
    c = _claim_file(k)
    if c.exists() and not _claimed(k):
        c.unlink(missing_ok=True)
    try:
        fd = os.open(c, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    os.write(fd, f"{os.getpid()} {k}".encode())
    os.close(fd)
    return True


def _progress(pct, label):
    print(f"@@ {int(pct)} {label}", flush=True)


def _copy(src, dst, name):
    total = max(1, src.stat().st_size)
    done, last = 0, 0.0
    with open(src, "rb") as a, open(dst, "wb") as b:
        while True:
            chunk = a.read(8 << 20)
            if not chunk:
                break
            b.write(chunk)
            done += len(chunk)
            if time.time() - last > 1:
                last = time.time()
                _progress(1 + done / total * 3, f"Copying {name} from your folder ({done * 100 // total}%)")


def _finish_original(cfg, p):
    """Move / delete / keep the owner's file once its Shorts are made. Returns a short note."""
    how = cfg["settings"].get("watch_after", "move")
    try:
        if how == "delete":
            p.unlink()
            return "deleted from the folder"
        if how == "move":
            done = p.parent / "Done"
            done.mkdir(exist_ok=True)
            dst, n = done / p.name, 2
            while dst.exists():
                dst, n = done / f"{p.stem} ({n}){p.suffix}", n + 1
            shutil.move(str(p), str(dst))
            return "moved to Done"
    except OSError as e:
        return f"couldn't {'delete' if how == 'delete' else 'move'} it ({e.strerror or e}) - it's still in the folder"
    return "left in the folder"


def process(cfg, p):
    """Clip one inbox video. Returns the number of Shorts made (None = failed or skipped)."""
    from . import pipeline
    try:
        st = p.stat()
    except OSError:
        return None
    k = _key(p, st)
    if not _claim(k):
        return None
    name = p.name
    copy_dir = None
    try:
        time.sleep(2)
        st2 = p.stat()
        if (st2.st_size, int(st2.st_mtime)) != (st.st_size, int(st.st_mtime)):
            print(f"  {name} is still being copied in - trying again later")
            return None
        if shutil.disk_usage(Path(cfg["paths"]["work_dir"]).parent if not Path(cfg["paths"]["work_dir"]).exists()
                             else cfg["paths"]["work_dir"]).free < st.st_size + (2 << 30):
            _set(k, name=name, status="failed", at=_now(), why="not enough free disk space")
            sys.exit(f"\n[!] Not enough free disk space to copy {name}. Free some space (Settings > Storage).\n")
        _set(k, name=name, status="making", at=_now())
        print(f"\n== Auto-clip folder: {name}")
        copy_dir = new_upload_folder(cfg, name)
        src = copy_dir / ("source" + p.suffix.lower())
        _copy(p, src, name)
        layout = cfg["settings"].get("watch_layout") or None
        out = pipeline.process_vod(str(src), cfg, layout=layout)
        data = load_json(Path(out) / "clips.json") if out and (Path(out) / "clips.json").exists() else None
        n = len(data["clips"]) if data else 0
        note = _finish_original(cfg, p)
        _set(k, name=name, status="done", at=_now(), shorts=n, job=Path(out).name if data else "", note=note)
        print(f"  {name}: {n} Short{'s' if n != 1 else ''}, original {note}")
        _progress(100, f"Done - {n} Shorts from {name} ready to review")
        return n
    except SystemExit as e:
        why = str(e).strip().replace("[!]", "").strip().splitlines()[0] if str(e).strip() else "stopped"
        _set(k, name=name, status="failed", at=_now(), why=why[:200])
        _drop_copy(copy_dir)
        raise
    except Exception as e:  # noqa: BLE001
        _set(k, name=name, status="failed", at=_now(), why=str(e)[:200])
        _drop_copy(copy_dir)
        raise
    finally:
        _claim_file(k).unlink(missing_ok=True)


def _drop_copy(copy_dir):
    """A failed run's copy is useless (the original is still in the inbox)."""
    if copy_dir and Path(copy_dir).is_dir():
        shutil.rmtree(copy_dir, ignore_errors=True)


def _now():
    return dt.datetime.now().isoformat(timespec="seconds")


def run_one(cfg):
    """`python -m clipper inbox --one`: the oldest waiting video (what the app starts while it's open)."""
    r = ready(cfg)
    if not r:
        print("Nothing waiting in the auto-clip folder.")
        return None
    return process(cfg, r[0])


def run_all(cfg, log=print):
    """Every waiting video (nightly auto run / `python -m clipper inbox`). A failure doesn't stop the rest."""
    made = 0
    for p in ready(cfg):
        try:
            n = process(cfg, p)
            if n is not None:
                made += 1
                log(f"auto-clip folder: {p.name} -> {n} Shorts")
        except SystemExit as e:
            log(f"auto-clip folder: {p.name} skipped: {str(e).strip()[:160]}")
        except Exception as e:  # noqa: BLE001
            log(f"auto-clip folder: {p.name} failed: {e}")
    return made


def status(cfg):
    """For the page: the folder, what's waiting, how many done, the last result."""
    st = cfg["settings"]
    s = _state()
    files = s["files"]
    waiting, making = [], None
    for p, stt in videos(cfg):
        k = _key(p, stt)
        info = files.get(k, {})
        if info.get("status") == "making" or _claimed(k):
            making = p.name
        elif info.get("status") not in ("done", "failed"):
            waiting.append(p.name)
    failed = [dict(v, key=k) for k, v in files.items() if v.get("status") == "failed"
              and (folder(cfg) / v.get("name", "")).exists()]
    last = files.get(s.get("last") or "")
    return {"enabled": bool(st.get("watch_enabled")), "folder": str(folder(cfg)), "exists": folder(cfg).is_dir(),
            "after": st.get("watch_after", "move"), "layout": st.get("watch_layout") or "",
            "waiting": waiting, "making": making, "failed": failed[-5:],
            "done": sum(1 for v in files.values() if v.get("status") == "done"), "last": last}


def retry(key):
    """Forget a failed file so it gets another try."""
    s = _state()
    if s["files"].get(key, {}).get("status") == "failed":
        s["files"].pop(key, None)
        save_json(STATE, s)
