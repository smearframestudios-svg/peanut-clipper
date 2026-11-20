"""The Peanut Clipper app: a local web page (only reachable from this PC) that runs everything."""
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from . import library
from .updater import python_exe
from .util import DATA, ROOT, load_config, load_json, parse_hms, save_json, save_settings

BELOW_NORMAL = 0x00004000
NO_WINDOW = 0x08000000


# ---------------------------------------------------------------- background jobs
class Runner:
    """Runs one job at a time in a separate low-priority process and tracks its progress."""

    def __init__(self):
        self.proc = None
        self.kind = None
        self.pct = 0
        self.label = ""
        self.log = []
        self.finished_at = None
        self.ok = None
        self.lock = threading.Lock()
        self.queue = []          # quick jobs (re-cut, export, cut a match) waiting for the current job

    @property
    def running(self):
        return self.proc is not None and self.proc.poll() is None

    QUEUEABLE = ("rerender", "export", "fromsearch")

    def start(self, kind, args, label, section_len=None):
        """True = started, "queued" = waits for the current job, False = refused (something else is running)."""
        with self.lock:
            if self.running:
                if kind in self.QUEUEABLE:
                    if [kind, args] not in [[q[0], q[1]] for q in self.queue]:
                        self.queue.append((kind, args, label, section_len))
                    return "queued"
                return False
            self.kind, self.pct, self.label, self.log, self.ok = kind, 0, label, [], None
            self.finished_at = None
            self.section_len = section_len
            env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
            flags = (BELOW_NORMAL | NO_WINDOW) if os.name == "nt" else 0
            self.proc = subprocess.Popen([python_exe(), "-u", "-m", "clipper"] + args, cwd=ROOT,
                                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                         encoding="utf-8", errors="replace", env=env, creationflags=flags)
            threading.Thread(target=self._read, daemon=True).start()
            return True

    def _read(self):
        dl = re.compile(r"\[download\]\s+(\d+(?:\.\d+)?)%")
        ff = re.compile(r"time=(\d+):(\d\d):(\d\d(?:\.\d+)?)")
        for line in self.proc.stdout:
            line = line.rstrip()
            if not line:
                continue
            if line.startswith("@@ "):
                _, pct, label = line.split(" ", 2)
                self.pct, self.label = int(pct), label
                continue
            fm = ff.search(line) if self.kind in ("vod", "frame", "search") and self.section_len else None
            if fm:
                done = int(fm.group(1)) * 3600 + int(fm.group(2)) * 60 + float(fm.group(3))
                frac = min(1.0, done / self.section_len)
                self.pct = max(self.pct, int(2 + frac * 30))
                self.label = f"Downloading the stream ({frac * 100:.0f}%)"
                if self.log and "time=" in self.log[-1]:
                    self.log[-1] = line
                    continue
            m = dl.search(line)
            if m and self.kind in ("vod", "frame", "search"):
                p = float(m.group(1))
                self.pct = max(self.pct, int(2 + p * 0.3))
                self.label = f"Downloading the stream ({p:.0f}%)"
                if self.log and "[download]" in self.log[-1]:
                    self.log[-1] = line
                    continue
            self.log.append(line)
            self.log = self.log[-400:]
        code = self.proc.wait()
        self.ok = code == 0
        if not self.ok:
            err = next((ln for ln in reversed(self.log) if ln.startswith(("[!]", "ERROR")) or "Error" in ln), "")
            self.label = (err.strip() or f"Stopped (code {code})")[:300]
        elif self.kind not in ("vod", "search", "fromsearch"):
            self.pct = 100
            self.label = {"upload": "Upload finished", "frame": "Frame ready - draw the boxes below",
                          "auto": "Auto run finished", "clips": "Twitch Shorts ready to review",
                          "hwtest": "Graphics card test finished", "rerender": "Short updated",
                          "export": "Exported for Premiere", "syncfix": "Stream converted"}.get(self.kind, "Done")
        self.finished_at = time.time()
        self._next()

    def _next(self):
        """Start the next waiting job, if any (the finished job's result stays on screen briefly first)."""
        if not self.queue:
            if UPDATE.get("after_job") and not UPDATE.get("busy"):
                UPDATE["after_job"] = False
                threading.Thread(target=run_update, args=(UPDATE_SRV[0],), daemon=True).start()
            return
        time.sleep(1.5)                  # let the page see the finished job before the next one starts
        with self.lock:
            nxt = self.queue.pop(0) if self.queue else None
        if nxt:
            self.start(*nxt)

    def cancel(self):
        if self.running:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(self.proc.pid), "/T", "/F"], capture_output=True)
            else:
                self.proc.kill()
            self.label = "Cancelled"

    def state(self):
        return {"running": self.running, "kind": self.kind, "pct": self.pct, "label": self.label,
                "ok": self.ok, "log": self.log[-60:], "queued": len(self.queue)}


RUNNER = Runner()


def grab_frame(cfg, source, at):
    """Saves one frame of the stream to data/calibrate.jpg for the Layout screen."""
    from .download import download_video, is_url
    at = at or 3600
    tmp = cfg["paths"]["work_dir"] / "_frame"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    if is_url(source):
        print("@@ 10 Downloading a few seconds of the stream", flush=True)
        video = download_video(source, tmp, cfg, at, at + 8)
        t = 2
    else:
        video, t = Path(source), at
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(video), "-frames:v", "1",
                    "-q:v", "3", str(DATA / "calibrate.jpg")], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print("@@ 100 Frame ready", flush=True)


# ---------------------------------------------------------------- state for the page
def app_state():
    cfg = load_config()
    from .auto import task_exists
    hw = load_json(DATA / "hardware.json", {}) or {}
    st = dict(cfg["settings"])
    st["twitch_client_secret"] = "********" if st.get("twitch_client_secret") else ""
    return {
        "job": RUNNER.state(),
        "counts": library.counts(cfg),
        "settings": st,
        "hw": {"gpu_speech": bool(hw.get("whisper_gpu")), "gpu_video": bool(hw.get("nvenc"))},
        "youtube": {"secret": (DATA / "client_secret.json").exists(), "token": (DATA / "token.json").exists()},
        "auto": {"task": task_exists(), "last": load_json(DATA / "last_auto.json")},
        "has_frame": (DATA / "calibrate.jpg").exists(),
        "default_export": str(ROOT / "exports"),
        "update": UPDATE,
        "last_made": load_json(cfg["paths"]["work_dir"] / "last_made.json"),
        "layouts": cfg["layouts"],
    }


# ---------------------------------------------------------------- web server
def make_handler():
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, body, ctype="text/html; charset=utf-8"):
            if isinstance(body, (dict, list)):
                body, ctype = json.dumps(body), "application/json"
            if isinstance(body, str):
                body = body.encode()
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _file(self, path):
            size = path.stat().st_size
            rng = self.headers.get("Range")
            start, end = 0, size - 1
            if rng and rng.startswith("bytes="):
                a, _, b = rng[6:].partition("-")
                start, end = int(a or 0), int(b) if b else size - 1
                self.send_response(206)
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            else:
                self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(path.name)[0] or "application/octet-stream")
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(end - start + 1))
            self.end_headers()
            with open(path, "rb") as fh:
                fh.seek(start)
                left = end - start + 1
                while left > 0:
                    chunk = fh.read(min(1 << 20, left))
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        return
                    left -= len(chunk)

        def do_GET(self):
            p = unquote(urlparse(self.path).path)
            cfg = load_config()
            out_root = Path(cfg["paths"]["output_dir"]).resolve()
            if p == "/":
                from .app_page import PAGE
                return self._send(200, PAGE)
            if p == "/api/ping":
                return self._send(200, {"app": "peanut-clipper"})
            if p == "/api/state":
                return self._send(200, app_state())
            if p == "/api/clips":
                return self._send(200, library.clips(cfg, "pending"))
            if p == "/api/plan":
                from .upload import plan
                return self._send(200, plan(cfg))
            if p == "/api/searches":
                out = []
                for f in sorted(Path(cfg["paths"]["output_dir"]).glob("*/search.json"), reverse=True)[:15]:
                    d = load_json(f)
                    out.append({"sid": d["sid"], "words": d["words"], "count": len(d["matches"]),
                                "created": d["created"], "source": d["source"]})
                return self._send(200, out)
            if p == "/api/search":
                from urllib.parse import parse_qs
                sid = Path(parse_qs(urlparse(self.path).query)["sid"][0]).name
                d = load_json(Path(cfg["paths"]["output_dir"]) / sid / "search.json")
                if not d:
                    return self._send(404, {"error": "search not found"})
                cd = load_json(Path(cfg["paths"]["output_dir"]) / sid / "clips.json") or {"clips": []}
                made = {c.get("from_search"): c["status"] for c in cd["clips"] if c.get("from_search") is not None}
                for m in d["matches"]:
                    m["made"] = made.get(m["i"])
                d["source_available"] = Path(d["source_file"]).is_file()
                from .download import needs_sync_fix
                d["needs_sync"] = d["source_available"] and needs_sync_fix(d["source_file"])
                return self._send(200, d)
            if p.startswith("/search_source/"):
                sid = Path(p.split("/")[2]).name
                d = load_json(Path(cfg["paths"]["output_dir"]) / sid / "search.json")
                if d and Path(d["source_file"]).is_file():
                    return self._file(Path(d["source_file"]))
                return self._send(404, "not found")
            if p == "/api/clip_info":
                from urllib.parse import parse_qs
                q = parse_qs(urlparse(self.path).query)
                return self._send(200, library.source_info(cfg, q["job"][0], q["id"][0]))
            if p.startswith("/source/"):
                parts = p.split("/")
                try:
                    _, _, c = library._find(cfg, parts[2], parts[3])
                    src = Path(c.get("source_file", ""))
                    win = library.edit_win(c)
                    if win and src.is_file():
                        from .download import needs_sync_fix
                        if needs_sync_fix(src):
                            src = win[0]
                    if src.is_file():
                        return self._file(src)
                except (SystemExit, IndexError, TypeError):
                    pass
                return self._send(404, "not found")
            if p.startswith("/overlay/"):
                f = DATA / "overlays" / Path(p[len("/overlay/"):]).name
                if f.is_file():
                    return self._file(f)
            if p == "/calib.jpg" and (DATA / "calibrate.jpg").exists():
                return self._file(DATA / "calibrate.jpg")
            if p.startswith("/media/"):
                f = (out_root / p[len("/media/"):]).resolve()
                if out_root in f.parents and f.is_file():
                    return self._file(f)
            self._send(404, "not found")

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            p = urlparse(self.path).path
            if p == "/api/overlay_upload":
                from urllib.parse import parse_qs
                name = Path(parse_qs(urlparse(self.path).query).get("name", ["banner.png"])[0]).name
                name = re.sub(r"[^\w.\- ]+", "_", name)
                folder = DATA / "overlays"
                folder.mkdir(parents=True, exist_ok=True)
                with open(folder / name, "wb") as fh:
                    left = n
                    while left > 0:
                        chunk = self.rfile.read(min(1 << 20, left))
                        if not chunk:
                            break
                        fh.write(chunk)
                        left -= len(chunk)
                st = load_config()["settings"]
                ovs = [o for o in st.get("overlays", []) if o.get("file") != name]
                ovs.append({"file": name, "position": "full", "enabled": True, "offset": 0})
                save_settings({"overlays": ovs})
                return self._send(200, {"ok": True})
            raw = self.rfile.read(n) if n else b"{}"
            cfg = load_config()
            if p == "/api/client_secret":
                try:
                    data = json.loads(raw)
                    assert "installed" in data or "web" in data
                except Exception:  # noqa: BLE001
                    return self._send(400, {"error": "That isn't a Google OAuth client file (client_secret...json)."})
                (DATA / "client_secret.json").write_bytes(raw)
                (DATA / "token.json").unlink(missing_ok=True)
                return self._send(200, {"ok": True})
            body = json.loads(raw or b"{}")
            if p == "/api/run":
                kind = body.get("kind")
                section = None
                if kind == "vod":
                    url = (body.get("url") or "").strip()
                    if not url:
                        return self._send(400, {"error": "Paste a stream link first."})
                    args = ["vod", url] + (["--layout", body["layout"]] if body.get("layout") else [])
                    if body.get("from"):
                        args += ["--from", body["from"]]
                    if body.get("to"):
                        args += ["--to", body["to"]]
                    label = "Starting..."
                    a_, b_ = parse_hms(body.get("from") or None), parse_hms(body.get("to") or None)
                    section = (b_ - (a_ or 0)) if b_ else None
                elif kind == "clips":
                    args, label = ["clips"] + (["--layout", body["layout"]] if body.get("layout") else []), \
                        "Getting today's top Twitch clips..."
                elif kind == "upload":
                    args, label = ["upload"], "Uploading to YouTube..."
                elif kind == "auto":
                    args, label = ["auto"], "Checking the channel for a finished stream..."
                elif kind == "hwtest":
                    args, label = ["hwtest"], "Testing your graphics card..."
                elif kind == "search":
                    url = (body.get("url") or "").strip()
                    if not url or not (body.get("words") or "").strip():
                        return self._send(400, {"error": "Paste a stream link and type the words to look for."})
                    args = ["search", url, "--words", body["words"]] + (["--layout", body["layout"]] if body.get("layout") else [])
                    if body.get("from"):
                        args += ["--from", body["from"]]
                    if body.get("to"):
                        args += ["--to", body["to"]]
                    if not body.get("chat", True):
                        args.append("--no-chat")
                    if body.get("exact"):
                        args.append("--exact")
                    label = "Starting the search..."
                    a_, b_ = parse_hms(body.get("from") or None), parse_hms(body.get("to") or None)
                    section = (b_ - (a_ or 0)) if b_ else None
                elif kind == "fromsearch":
                    args = ["fromsearch", body["sid"], str(int(body["idx"]))] + (["--export"] if body.get("export") else []) + \
                        (["--layout", body["layout"]] if body.get("layout") else [])
                    label = "Exporting for Premiere..." if body.get("export") else "Making the Short..."
                elif kind == "syncfix":
                    args = ["syncfix", body["sid"], "--search"] if body.get("sid") else ["syncfix", body["job"], body["id"]]
                    label = "Converting the stream so it plays smoothly (one time, a few minutes)..."
                elif kind == "rerender":
                    args = ["rerender", body["job"], body["id"], str(float(body["start"])), str(float(body["end"]))] + \
                        (["--layout", body["layout"]] if body.get("layout") else [])
                    if body.get("framing") == "none":
                        args += ["--framing", "none"]
                    elif isinstance(body.get("framing"), dict):
                        args += ["--framing", json.dumps(body["framing"])]
                    label = "Re-cutting the Short..."
                elif kind == "export":
                    args = ["export", body["job"], body["id"]] if body.get("id") else ["export", "--all"]
                    label = "Exporting for Premiere..."
                elif kind == "frame":
                    args, label = ["frame", body.get("url", ""), "--at", body.get("at") or "1:00:00"], "Grabbing a frame..."
                else:
                    return self._send(400, {"error": "unknown job"})
                started = RUNNER.start(kind, args, label, section if kind in ("vod", "search") else (8 if kind == "frame" else None))
                if started == "queued":
                    return self._send(200, {"ok": True, "queued": True})
                if not started:
                    return self._send(409, {"error": "Something is already running - wait for it or cancel it."})
                return self._send(200, {"ok": True})
            if p == "/api/check_update":
                threading.Thread(target=check_updates, daemon=True).start()
                return self._send(200, {"ok": True})
            if p == "/api/update":
                if RUNNER.running:
                    # don't cut the job short: update by itself as soon as it (and anything waiting in line) is done
                    UPDATE["after_job"] = True
                    UPDATE_SRV[0] = self.server
                    return self._send(200, {"ok": True, "after_job": True})
                if UPDATE.get("busy"):
                    return self._send(409, {"error": "Already updating."})
                threading.Thread(target=run_update, args=(self.server,), daemon=True).start()
                return self._send(200, {"ok": True})
            if p == "/api/quit":
                threading.Thread(target=quit_app, args=(self.server,), daemon=True).start()
                return self._send(200, {"ok": True})
            if p == "/api/cancel":
                RUNNER.cancel()
                return self._send(200, {"ok": True})
            if p == "/api/decide":
                library.decide(cfg, body["job"], body["id"], body["status"], body.get("title"))
                return self._send(200, {"ok": True})
            if p == "/api/settings":
                from .auto import install_task, remove_task
                if body.get("twitch_client_secret") == "********":
                    body.pop("twitch_client_secret")
                st = save_settings(body)
                msg = "Saved."
                if st["auto_enabled"]:
                    ok, out = install_task(st["auto_time"])
                    msg = "Saved. Auto mode is on." if ok else f"Saved, but Windows refused the nightly task: {out}"
                else:
                    remove_task()
                return self._send(200, {"ok": True, "message": msg})
            if p == "/api/overlays":
                ovs = body.get("overlays", [])
                keep = {o["file"] for o in ovs}
                for f in (DATA / "overlays").glob("*") if (DATA / "overlays").exists() else []:
                    if f.name not in keep:
                        f.unlink(missing_ok=True)
                save_settings({"overlays": ovs})
                return self._send(200, {"ok": True})
            if p == "/api/layouts":
                from .util import save_layouts
                clean = []
                for l in body.get("layouts", []):
                    item = {"id": str(l["id"])[:40], "name": (str(l.get("name") or "Layout").strip() or "Layout")[:40],
                            "mode": l.get("mode") if l.get("mode") in ("stack", "single", "blurfit") else "blurfit",
                            "top_height": int(l.get("top_height", 760)), "banners": l.get("banners")}
                    for k in ("avatar", "gameplay"):
                        b = l.get(k) or {}
                        item[k] = {q: max(0.0, min(1.0, float(b.get(q, 0.5)))) for q in ("x", "y", "w", "h")}
                    clean.append(item)
                try:
                    save_layouts({"default": body.get("default"), "layouts": clean})
                except ValueError as e:
                    return self._send(400, {"error": str(e)})
                return self._send(200, {"ok": True})
            self._send(404, {"error": "not found"})

    return H


UPDATE_SRV = [None]     # the server to restart after an update that waited for a job
UPDATE = {"after_job": False, "current": None, "latest": None, "available": False, "notes": "", "busy": False, "msg": ""}


def check_updates():
    from .updater import check
    UPDATE.update(check())


def run_update(srv):
    from .updater import apply
    UPDATE.update(busy=True, msg="Starting update...")
    try:
        apply(say=lambda m: UPDATE.update(msg=m))
    except Exception as e:  # noqa: BLE001
        UPDATE.update(busy=False, msg=f"Update failed: {e}")
        return
    UPDATE.update(msg="Restarting...")
    restart(srv)


def _spawn_app(extra=()):
    exe = Path(sys.executable)
    w = exe.with_name("pythonw.exe")
    cmd = [str(w if w.exists() else exe), "-m", "clipper", "launch", "--no-browser", *extra]
    kw = {"cwd": ROOT}
    if os.name == "nt":
        kw["creationflags"] = 0x00000008 | 0x00000200   # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    else:
        kw["start_new_session"] = True
    subprocess.Popen(cmd, **kw)


def restart(srv):
    RUNNER.cancel()
    _spawn_app(["--wait"])
    time.sleep(0.5)
    srv.shutdown()
    srv.server_close()
    os._exit(0)


def quit_app(srv):
    time.sleep(0.4)
    RUNNER.cancel()
    srv.shutdown()
    srv.server_close()
    os._exit(0)


def already_running(port):
    import urllib.request
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/ping", timeout=2) as r:
            return b"peanut-clipper" in r.read()
    except Exception:  # noqa: BLE001
        return False


def serve_app(cfg, port=8765, open_browser=True, wait=False):
    url = f"http://127.0.0.1:{port}/"
    if already_running(port) and not wait:
        if open_browser:
            webbrowser.open(url)
        return
    try:
        library.cleanup_sources(cfg)
    except Exception:  # noqa: BLE001
        pass
    srv = None
    for _ in range(40 if wait else 1):      # after an update, wait for the old app to let go of the port
        try:
            srv = ThreadingHTTPServer(("127.0.0.1", port), make_handler())
            break
        except OSError:
            time.sleep(0.5)
    if srv is None:
        webbrowser.open(url)
        print("Something else is using the app's address; opened it in your browser.")
        return
    print(f"\n  Peanut Clipper is running at {url}\n")
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    threading.Thread(target=check_updates, daemon=True).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        RUNNER.cancel()
