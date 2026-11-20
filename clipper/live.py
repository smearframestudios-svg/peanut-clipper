"""Record a YouTube stream while it's live (video + chat), so Shorts can be made the moment it ends.

Runs as its own background process (`python -m clipper live ...`), separate from the app's job runner, so the rest
of the app stays usable. It reports to data/live.json (with a heartbeat) and stops when data/live.stop appears.

The finished recording is saved exactly where a normal download of that stream would go
(work/_downloads/<video id>/source.mp4 + chat.live_chat.json), so Make Shorts, keyword search and compilations
use it with no extra download.
"""
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from .download import _yt_dlp, cache_key
from .util import DATA, ROOT, load_json, probe, save_json

STATE = DATA / "live.json"
STOP = DATA / "live.stop"
CHECK_EVERY = 300          # seconds between "is he live yet?" checks while waiting
BEAT_STALE = 45            # no heartbeat for this long = the recorder isn't running
NO_WINDOW = 0x08000000 if os.name == "nt" else 0


def _now():
    return time.time()


def _write(**kw):
    st = load_json(STATE, {}) or {}
    st.update(kw, beat=_now(), pid=os.getpid())
    save_json(STATE, st)
    return st


def state():
    """What the app shows. Adds `alive` (the recorder is running) and free disk space."""
    st = load_json(STATE, {}) or {}
    st["alive"] = bool(st.get("beat")) and _now() - st["beat"] < BEAT_STALE and st.get("state") in (
        "checking", "waiting", "recording", "saving", "making")
    try:
        from .util import load_config
        work = Path(load_config()["paths"]["work_dir"])
        work.mkdir(parents=True, exist_ok=True)
        st["free_gb"] = round(shutil.disk_usage(work).free / 1e9)
    except Exception:  # noqa: BLE001
        st["free_gb"] = None
    if st.get("state") in ("checking", "waiting", "recording", "saving", "making") and not st["alive"]:
        st["state"] = "crashed"     # PC slept, app was killed, power cut...
    return st


def live_url(url):
    """A channel link -> its /live page (which is the current stream while he's live)."""
    u = url.strip().rstrip("/")
    if "watch?v=" in u or "youtu.be/" in u or "/live/" in u:
        return u
    for tail in ("/streams", "/videos", "/featured", "/live"):
        if u.endswith(tail):
            u = u[: -len(tail)]
    return u + "/live"


def check(url):
    """(live_status, video id, title, start epoch) for a channel or stream link. Not live -> status ''."""
    r = subprocess.run(_yt_dlp() + ["--no-playlist", "--skip-download", "--no-warnings", "--print",
                                    "%(live_status)s\t%(id)s\t%(release_timestamp)s\t%(title)s", live_url(url)],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore", creationflags=NO_WINDOW)
    for line in r.stdout.splitlines()[::-1]:
        parts = line.split("\t")
        if len(parts) >= 4 and len(parts[1]) == 11:
            try:
                start = float(parts[2])
            except ValueError:
                start = None
            return parts[0], parts[1], parts[3], start
    return "", "", "", None


def _stopped():
    return STOP.exists()


def _sleep(seconds):
    """Sleep, but wake up for a stop request (and keep the heartbeat going)."""
    end = _now() + seconds
    while _now() < end:
        if _stopped():
            return True
        time.sleep(1)
        _write()
    return False


def _kill(p):
    if p is None or p.poll() is not None:
        return
    if os.name == "nt":       # yt-dlp runs ffmpeg as a child: take the whole tree down
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True, creationflags=NO_WINDOW)
    else:
        p.terminate()
    try:
        p.wait(15)
    except subprocess.TimeoutExpired:
        p.kill()


def _size(folder, prefix):
    return sum(f.stat().st_size for f in folder.glob(prefix + "*") if f.is_file())


def _chat_file(folder):
    files = sorted(folder.glob("chatlive*.live_chat.json*"), key=lambda f: f.stat().st_size, reverse=True)
    return files[0] if files else None


def _count_lines(f, cache):
    """Count chat lines incrementally (the file grows; don't re-read it all every 2 seconds)."""
    if not f:
        return 0
    if cache.get("f") != str(f):
        cache.update(f=str(f), pos=0, n=0)
    try:
        with open(f, "rb") as h:
            h.seek(cache["pos"])
            chunk = h.read()
        cache["pos"] += len(chunk)
        cache["n"] += chunk.count(b"\n")
    except OSError:
        pass
    return cache["n"]


def record(cfg, url, from_start=True, wait=False, then_make=False):
    STOP.unlink(missing_ok=True)
    _write(state="checking", url=url, from_start=from_start, wait=wait, then_make=then_make, message="",
           started=None, title="", seconds=0, bytes=0, chat=0, video_id="", job_dir="", file="", made=None,
           made_pct=None, made_label="")
    # 1) wait until he's live
    while True:
        status, vid, title, start_epoch = check(url)
        _write(last_check=_now(), title=title, video_id=vid)
        if status == "is_live":
            break
        if not wait:
            msg = {"is_upcoming": "He hasn't gone live yet (the stream is scheduled).",
                   "post_live": "That stream just ended - YouTube is still processing it.",
                   "was_live": "That stream already ended. Use Make Shorts with the link instead."}.get(
                status, "He's not live right now.")
            _write(state="idle", message=msg)
            print(msg)
            return None
        _write(state="waiting", message="Not live yet")
        if _sleep(CHECK_EVERY):
            _write(state="idle", message="Stopped waiting.")
            STOP.unlink(missing_ok=True)
            return None
    watch = f"https://www.youtube.com/watch?v={vid}"
    folder = Path(cfg["paths"]["work_dir"]) / "_downloads" / cache_key(watch)
    folder.mkdir(parents=True, exist_ok=True)
    if (folder / "source.mp4").exists():
        _write(state="done", message="This stream was already recorded.", job_dir=str(folder), url=watch,
               file=str(folder / "source.mp4"))
        return folder / "source.mp4"
    print(f"recording: {title}")
    h = int(cfg["download"]["max_height"])
    fmt = (f"bv*[height<={h}][vcodec^=avc1]+ba[ext=m4a]/b[height<={h}][vcodec^=avc1]/"
           f"bv*[height<={h}]+ba/b[height<={h}]/b")
    base = _yt_dlp() + ["--no-playlist", "--no-warnings", "--newline", "--no-part", "-f", fmt]
    chat_cmd = _yt_dlp() + ["--skip-download", "--write-subs", "--sub-langs", "live_chat", "--no-warnings",
                            "-o", str(folder / "chatlive"), watch]
    log = open(DATA / "live.log", "a", encoding="utf-8")
    log.write(f"\n== {dt.datetime.now():%Y-%m-%d %H:%M} {title} ({watch})\n")
    chat_p = subprocess.Popen(chat_cmd, stdout=log, stderr=subprocess.STDOUT, creationflags=NO_WINDOW)
    parts = []           # [(file prefix, wall clock when it started)]
    t0 = start_epoch if (from_start and start_epoch) else _now()
    _write(state="recording", started=t0, job_dir=str(folder), url=watch, title=title, message="")
    lines = {}
    vid_p = None
    stopped = False
    restarts = 0
    try:
        while True:
            prefix = f"rec{len(parts) + 1}"
            cmd = base + (["--live-from-start"] if from_start and not parts else ["--hls-use-mpegts"]) + \
                ["-o", str(folder / (prefix + ".%(ext)s")), watch]
            parts.append((prefix, _now()))
            vid_p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, creationflags=NO_WINDOW)
            while vid_p.poll() is None:
                if _stopped():
                    stopped = True
                    break
                time.sleep(2)
                _write(seconds=round(_now() - t0), bytes=sum(_size(folder, p) for p, _ in parts),
                       chat=_count_lines(_chat_file(folder), lines))
            if stopped:
                break
            # yt-dlp ended on its own: the stream ended - or the connection dropped. Still live -> keep going.
            status = check(watch)[0]
            if status != "is_live" or restarts >= 30:
                break
            restarts += 1
            log.write(f"-- connection dropped, still live: recording again ({restarts})\n")
            _sleep(5)
    finally:
        _kill(vid_p)
        time.sleep(3 if not stopped else 0)
        _kill(chat_p)
        log.close()
        STOP.unlink(missing_ok=True)
    try:
        out = finish(folder, parts, t0, from_start)
    except Exception as e:  # noqa: BLE001
        _write(state="error", message=f"Saving the recording failed: {e}")
        raise
    if out and then_make:
        make_shorts(watch)
    return out


def finish(folder, parts, t0, from_start):
    """Turn the recorded pieces into source.mp4 + chat.live_chat.json."""
    _write(state="saving", message="Saving the recording")
    folder = Path(folder)
    pieces = []
    for k, (prefix, wall) in enumerate(parts):
        files = [f for f in folder.glob(prefix + ".*") if f.is_file() and f.stat().st_size > 0]
        if not files:
            continue
        merged = [f for f in files if ".f" not in f.name.split(prefix, 1)[1]]
        if merged:               # yt-dlp finished normally and joined video + audio itself
            pieces.append((max(merged, key=lambda f: f.stat().st_size), None, wall))
        else:                    # stopped part-way (live-from-start): separate video / audio pieces
            vids = [f for f in files if f.suffix.lower() in (".mp4", ".webm", ".mkv")]
            auds = [f for f in files if f.suffix.lower() in (".m4a", ".webm", ".opus") and f not in vids[:1]]
            v = max(vids, key=lambda f: f.stat().st_size) if vids else None
            a = max(auds, key=lambda f: f.stat().st_size) if auds else None
            if v:
                pieces.append((v, a, wall))
    if not pieces:
        _write(state="error", message="Nothing was recorded (did the stream end right away?).")
        return None
    tmp = folder / "_join"
    tmp.mkdir(exist_ok=True)
    fixed, walls = [], []
    for k, (v, a, wall) in enumerate(pieces):
        out = tmp / f"p{k}.mp4"
        head = ["ffmpeg", "-v", "error", "-y", "-fflags", "+genpts", "-i", str(v)]
        tries = []                                   # best first; a damaged audio piece falls back to video only
        if a:
            tries += [head + ["-i", str(a), "-map", "0:v:0", "-map", "1:a:0", "-c", "copy"],
                      head + ["-i", str(a), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k"]]
        tries += [head + ["-map", "0:v:0", "-map", "0:a:0?", "-c", "copy"],
                  head + ["-map", "0:v:0", "-map", "0:a:0?", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k"]]
        for cmd in tries:
            out.unlink(missing_ok=True)
            # same clock for every piece, so pieces from different download methods join cleanly
            r = subprocess.run(cmd + ["-video_track_timescale", "90000", "-avoid_negative_ts", "make_zero",
                                      "-movflags", "+faststart", str(out)], capture_output=True, creationflags=NO_WINDOW)
            if r.returncode == 0 and out.exists() and out.stat().st_size > 1000:
                break
        if out.exists() and out.stat().st_size > 1000:
            fixed.append(out)
            walls.append(wall)
    final = folder / "source.mp4"
    if not fixed:
        _write(state="error", message="The recording couldn't be saved (the recorded file was damaged).")
        return None
    if len(fixed) == 1:
        os.replace(fixed[0], final)
    else:
        (tmp / "list.txt").write_text("".join(f"file '{p.name}'\n" for p in fixed), encoding="utf-8")
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy",
                            "-movflags", "+faststart", str(final)], cwd=tmp, creationflags=NO_WINDOW)
        if r.returncode != 0 or not _in_sync(final, sum(_dur(p) for p in fixed)):
            # pieces don't match (quality or sound settings changed mid-stream): re-encode while joining
            from .download import _sync_args
            from .util import load_config
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt"] +
                           _sync_args(load_config())[1] + [str(final)], cwd=tmp, check=True, creationflags=NO_WINDOW)
    durs = []
    for p in fixed:
        try:
            durs.append(probe(p if p.exists() else final)[0])
        except RuntimeError:
            durs.append(0.0)
    try:
        total = probe(final)[0]
    except RuntimeError:
        total = 0
    if total < 1:
        _write(state="error", message="The recording came out empty.")
        return None
    # chat: live timestamps -> seconds into the recording (replay format, which the app already reads)
    starts = [t0 if (from_start and k == 0) else w for k, w in enumerate(walls)]
    n = convert_chat(_chat_file(folder), folder / "chat.live_chat.json", starts, durs)
    for f in list(folder.glob("rec*")) + list(folder.glob("chatlive*")):
        f.unlink(missing_ok=True)
    shutil.rmtree(tmp, ignore_errors=True)
    (folder / "recorded_live").write_text(dt.datetime.now().isoformat(timespec="seconds"))
    _write(state="done", file=str(final), seconds=round(total), bytes=final.stat().st_size, chat=n,
           message="", ended=_now())
    print(f"saved: {final} ({round(total / 60)} min, {n} chat messages)")
    return final


def _dur(f):
    try:
        return probe(f)[0]
    except RuntimeError:
        return 0.0


def _in_sync(f, expected):
    """True when the joined file's video and sound are both about as long as the pieces added up."""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration", "-of", "csv=p=0",
                        str(f)], capture_output=True, text=True, creationflags=NO_WINDOW)
    lens = []
    for line in r.stdout.split():
        kind, _, d = line.partition(",")
        try:
            lens.append(float(d))
        except ValueError:
            pass
    return bool(lens) and all(abs(d - expected) < 3 for d in lens)


def convert_chat(src, dest, starts, durs):
    """yt-dlp live chat lines -> replay lines with videoOffsetTimeMsec = seconds into our recording."""
    if not src or not Path(src).exists():
        return 0
    from .chat import _parse_youtube_line  # noqa: F401  (same format the app reads)
    out, n = [], 0
    offsets = [sum(durs[:k]) for k in range(len(durs))]
    for line in Path(src).read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        rep = obj.get("replayChatItemAction") or {}
        ts = None
        for act in rep.get("actions", []):
            item = act.get("addChatItemAction", {}).get("item", {})
            for r in item.values():
                if isinstance(r, dict) and r.get("timestampUsec"):
                    ts = int(r["timestampUsec"]) / 1e6
        if ts is None:
            continue
        k = max([i for i, s in enumerate(starts) if s <= ts] or [0])
        t = offsets[k] + (ts - starts[k])
        if t < 0 or (durs and t > sum(durs) + 5):
            continue
        rep["videoOffsetTimeMsec"] = str(int(t * 1000))
        out.append(json.dumps({"replayChatItemAction": rep}, ensure_ascii=False))
        n += 1
    Path(dest).write_text("\n".join(out) + "\n", encoding="utf-8")
    return n


def make_shorts(watch):
    """'Make Shorts as soon as he ends': run the normal Make Shorts job on the recording, showing progress here."""
    _write(state="making", made_pct=0, made_label="Finding the best moments")
    p = subprocess.Popen([sys.executable, "-m", "clipper", "vod", watch], cwd=ROOT, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, errors="replace", creationflags=NO_WINDOW)
    for line in p.stdout:
        if line.startswith("@@ "):
            pct, _, label = line[3:].strip().partition(" ")
            try:
                _write(made_pct=int(pct), made_label=label)
            except ValueError:
                pass
    ok = p.wait() == 0
    _write(state="done", made=ok, made_pct=100 if ok else None,
           made_label="New Shorts are waiting in Review" if ok else "Making Shorts didn't finish - try Make Shorts from it")


def start_background(url, from_start=True, wait=False, then_make=False):
    """Start the recorder as its own process (keeps going if the app is closed)."""
    st = state()
    if st.get("alive"):
        return False, "A recording is already running."
    STOP.unlink(missing_ok=True)
    save_json(STATE, {"state": "checking", "url": url, "beat": _now(), "message": "Checking if he's live..."})
    args = [sys.executable, "-m", "clipper", "live", url] + (["--from-start"] if from_start else []) + \
        (["--wait"] if wait else []) + (["--then-make"] if then_make else [])
    flags = (0x00000008 | 0x00000200 | NO_WINDOW | 0x00004000) if os.name == "nt" else 0  # detached, below normal
    subprocess.Popen(args, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                     creationflags=flags, start_new_session=os.name != "nt")
    return True, ""


def stop():
    STOP.write_text("stop")


def recover(cfg):
    """The recorder stopped unexpectedly (PC slept, power cut): save whatever was recorded."""
    st = load_json(STATE, {}) or {}
    folder = Path(st.get("job_dir") or "")
    if not folder.is_dir():
        _write(state="idle", message="Nothing to save.")
        return None
    parts = sorted({f.name.split(".")[0] for f in folder.glob("rec*")})
    walls = [st.get("started") or _now()] + [None] * (len(parts) - 1)
    return finish(folder, [(p, w or st.get("started")) for p, w in zip(parts, walls)], st.get("started") or _now(),
                  bool(st.get("from_start")))
