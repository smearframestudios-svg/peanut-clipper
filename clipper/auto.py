"""Nightly auto mode: find the newest finished stream on the channel and make Shorts from it.
Runs from a Windows scheduled task (low priority, hidden window) or the app's "Run now" button."""
import datetime as dt
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .util import DATA, ROOT, load_json, save_json

TASK = "Peanut Clipper Nightly"
MIN_FREE_GB = 30


def _log(msg):
    line = f"{dt.datetime.now():%Y-%m-%d %H:%M}  {msg}"
    print(line, flush=True)
    with open(DATA / "auto.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def recent_streams(url, n=6):
    r = subprocess.run(["yt-dlp", "--flat-playlist", "--playlist-end", str(n),
                        "--print", "%(id)s\t%(live_status)s\t%(duration)s\t%(title)s", url],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    out = []
    for line in r.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) >= 4 and len(parts[0]) == 11:
            out.append({"id": parts[0], "status": parts[1], "duration": parts[2], "title": parts[3]})
    return out


def run_auto(cfg):
    from . import pipeline
    st = cfg["settings"]
    _log("auto mode started")
    try:                                     # tidy up first - it may free the space this run needs
        from .storage import auto_clean
        n, freed = auto_clean(cfg)
        if n:
            _log(f"auto-delete: removed {n} item(s), freed {freed / 1e9:.1f} GB")
    except Exception as e:  # noqa: BLE001
        _log(f"auto-delete skipped: {e}")
    free_gb = shutil.disk_usage(ROOT).free / 1e9
    if free_gb < MIN_FREE_GB:
        _log(f"skipped: only {free_gb:.0f} GB free (need {MIN_FREE_GB} GB for a full stream)")
        return
    if st.get("live_in_auto"):
        from . import live
        if not live.state().get("alive"):
            status, vid, title, _ = live.check(st["channel_url"])
            if status == "is_live":
                live.start_background(st["channel_url"], from_start=st.get("live_from_start", True),
                                      then_make=st.get("live_then_make", True))
                _log(f"he's live - started recording: {title}")
    done = set(load_json(DATA / "processed.json", []) or [])
    made = 0
    try:
        for s in recent_streams(st["channel_url"]):
            if s["id"] in done or s["status"] in ("is_live", "is_upcoming", "post_live"):
                continue
            try:
                dur = float(s["duration"])
            except ValueError:
                dur = 0
            if dur and dur < 1800:
                continue          # not a full stream
            _log(f"making Shorts from: {s['title']}")
            try:
                pipeline.process_vod(f"https://www.youtube.com/watch?v={s['id']}", cfg)
                made += 1
            except SystemExit as e:   # e.g. still processing on YouTube
                _log(f"skipped for now: {str(e).strip()}")
                continue
            break                 # one stream per night is plenty
        if st.get("auto_twitch_clips") and st.get("twitch_client_id"):
            _log("checking today's top Twitch clips")
            if pipeline.process_twitch_clips(cfg, 24, 8):
                made += 1
    except Exception as e:  # noqa: BLE001
        _log(f"error: {e}")
        raise
    _log("finished - new Shorts are waiting for review" if made else "finished - nothing new")
    save_json(DATA / "last_auto.json", {"time": dt.datetime.now().isoformat(timespec="minutes"), "made": made})


# ---------- Windows scheduled task ----------

TASK_XML = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo><Description>Makes Shorts from the newest finished stream.</Description></RegistrationInfo>
  <Triggers><CalendarTrigger><StartBoundary>{start}</StartBoundary><Enabled>true</Enabled>
    <ScheduleByDay><DaysInterval>1</DaysInterval></ScheduleByDay></CalendarTrigger></Triggers>
  <Principals><Principal id="Author"><LogonType>InteractiveToken</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal></Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <StartWhenAvailable>true</StartWhenAvailable>
    <WakeToRun>true</WakeToRun>
    <ExecutionTimeLimit>PT6H</ExecutionTimeLimit>
    <Priority>7</Priority>
    <Enabled>true</Enabled>
  </Settings>
  <Actions Context="Author"><Exec>
    <Command>{python}</Command>
    <Arguments>-m clipper auto</Arguments>
    <WorkingDirectory>{root}</WorkingDirectory>
  </Exec></Actions>
</Task>"""


def _pythonw():
    exe = Path(sys.executable)
    w = exe.with_name("pythonw.exe")
    return w if w.exists() else exe


def install_task(time_hhmm):
    if os.name != "nt":
        return False, "Auto mode needs Windows."
    start = f"{dt.date.today().isoformat()}T{time_hhmm}:00"
    from xml.sax.saxutils import escape
    xml = TASK_XML.format(start=start, python=escape(str(_pythonw())), root=escape(str(ROOT)))
    with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-16") as f:
        f.write(xml)
        path = f.name
    r = subprocess.run(["schtasks", "/Create", "/TN", TASK, "/XML", path, "/F"], capture_output=True, text=True)
    os.unlink(path)
    _task_cache["t"] = 0.0
    return r.returncode == 0, (r.stderr or r.stdout).strip()


def remove_task():
    if os.name != "nt":
        return True, ""
    r = subprocess.run(["schtasks", "/Delete", "/TN", TASK, "/F"], capture_output=True, text=True)
    _task_cache["t"] = 0.0
    return True, (r.stderr or r.stdout).strip()


_task_cache = {"t": 0.0, "v": False}


def task_exists(max_age=120):
    """Asked by the app every couple of seconds, so only really check Windows every 2 minutes."""
    import time
    if os.name != "nt":
        return False
    if time.time() - _task_cache["t"] > max_age:
        _task_cache["v"] = subprocess.run(["schtasks", "/Query", "/TN", TASK], capture_output=True).returncode == 0
        _task_cache["t"] = time.time()
    return _task_cache["v"]
