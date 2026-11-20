import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "bin"            # ffmpeg.exe, ffprobe.exe, deno.exe live here
DATA = ROOT / "data"          # settings, layout, tokens, state

DEFAULT_SETTINGS = {
    "channel_url": "https://www.youtube.com/@TheBurntPeanut/streams",
    "live_from_start": True,
    "live_then_make": True,
    "live_in_auto": False,
    "auto_enabled": False,
    "auto_time": "04:30",
    "auto_twitch_clips": False,
    "shorts_per_stream": 12,
    "captions": False,
    "delete_source": True,
    "delete_rejected": True,
    "delete_uploaded": True,
    "use_gpu": True,
    "schedule_times": ["11:45", "16:30", "20:15"],
    "keep_source_days": 3,
    "edit_window_min": 6,       # AV1 streams: minutes converted for the trim editor, centred on the Short
    "export_folder": "",
    "screenshot_folder": "",
    "export_handles_sec": 3,
    "export_vertical_too": False,
    "output_fps": 60,
    "overlays": [],
    "saved_keywords": [],
    "saved_keywords_max": 5,
    "search_lead_sec": 10,
    "search_tail_sec": 8,
    "twitch_client_id": "",
    "twitch_client_secret": "",
}


def _hide_console_windows():
    """On Windows, every console program we start (ffmpeg, yt-dlp, schtasks...) would flash a
    black window because the app itself runs without one. Make all of them start hidden."""
    import subprocess
    if os.name != "nt" or getattr(subprocess.Popen, "_pc_hidden", False):
        return
    orig = subprocess.Popen.__init__

    def init(self, *args, **kw):
        flags = kw.get("creationflags", 0) or 0
        if not flags & 0x00000008:          # leave DETACHED_PROCESS launches alone
            kw["creationflags"] = flags | 0x08000000   # CREATE_NO_WINDOW
        orig(self, *args, **kw)

    subprocess.Popen.__init__ = init
    subprocess.Popen._pc_hidden = True


def setup_env():
    """Put our own tools (and NVIDIA's CUDA DLLs from pip) first on PATH."""
    _hide_console_windows()
    paths = [str(BIN)]
    try:
        import site
        for sp in site.getsitepackages():
            nv = Path(sp) / "nvidia"
            if nv.is_dir():
                for b in nv.glob("*/bin"):
                    paths.append(str(b))
                    if hasattr(os, "add_dll_directory"):
                        try:
                            os.add_dll_directory(str(b))
                        except OSError:
                            pass
    except Exception:  # noqa: BLE001
        pass
    os.environ["PATH"] = os.pathsep.join(paths + [os.environ.get("PATH", "")])


def load_settings():
    DATA.mkdir(exist_ok=True)
    s = dict(DEFAULT_SETTINGS)
    s.update(load_json(DATA / "settings.json", {}) or {})
    return s


def save_settings(new):
    s = load_settings()
    s.update({k: v for k, v in new.items() if k in DEFAULT_SETTINGS})
    save_json(DATA / "settings.json", s)
    return s


LAYOUT_KEYS = ("mode", "avatar", "gameplay", "top_height", "banners")


def load_layouts(base=None):
    """Saved layouts: {"default": id, "layouts": [{id, name, mode, avatar, gameplay, top_height, banners}]}.
    banners = list of banner file names for that layout, or None for "all banners that are on"."""
    DATA.mkdir(exist_ok=True)
    f = DATA / "layouts.json"
    data = load_json(f)
    if data and data.get("layouts"):
        return data
    base = dict(base or {"mode": "blurfit", "top_height": 760,
                         "avatar": {"x": 0.7, "y": 0.5, "w": 0.3, "h": 0.5},
                         "gameplay": {"x": 0.15, "y": 0.0, "w": 0.7, "h": 1.0}})
    old = load_json(DATA / "layout.json")       # from before saved layouts existed
    if old:
        base.update(old)
    main = {"id": "main", "name": "Main", "banners": None}
    main.update({k: base[k] for k in ("mode", "avatar", "gameplay", "top_height") if k in base})
    data = {"default": "main", "layouts": [main]}
    save_json(f, data)
    return data


def save_layouts(data):
    ids = [l["id"] for l in data.get("layouts", [])]
    if not ids:
        raise ValueError("at least one layout is needed")
    if data.get("default") not in ids:
        data["default"] = ids[0]
    save_json(DATA / "layouts.json", data)


def get_layout(cfg, lid=None):
    lays = cfg["layouts"]["layouts"]
    want = lid or cfg["layouts"]["default"]
    return next((l for l in lays if l["id"] == want), None) or \
        next((l for l in lays if l["id"] == cfg["layouts"]["default"]), lays[0])


def apply_layout(cfg, lid=None):
    """Point cfg["layout"] (what the renderer reads) at a saved layout. Returns its id."""
    lay = get_layout(cfg, lid)
    merged = dict(cfg["layout_base"])
    merged.update({k: lay[k] for k in LAYOUT_KEYS if k in lay})
    merged["id"], merged["name"] = lay["id"], lay["name"]
    cfg["layout"] = merged
    return lay["id"]


def load_config():
    import yaml
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    DATA.mkdir(exist_ok=True)
    cfg["layout_base"] = dict(cfg["layout"])
    cfg["layouts"] = load_layouts(cfg["layout"])
    apply_layout(cfg, None)
    st = load_settings()
    cfg["settings"] = st
    cfg["detect"]["keep"] = int(st["shorts_per_stream"])
    cfg["captions"]["enabled"] = bool(st["captions"])
    cfg["upload"]["schedule_times"] = st["schedule_times"]
    hw = load_json(DATA / "hardware.json", {}) or {}
    gpu = st["use_gpu"] and hw.get("whisper_gpu")
    cfg["whisper"]["device"] = "cuda" if gpu else "cpu"
    cfg["whisper"]["compute_type"] = "float16" if gpu else "int8"
    cfg["render_encoder"] = "h264_nvenc" if (st["use_gpu"] and hw.get("nvenc")) else "libx264"
    for key in ("work_dir", "output_dir"):
        p = Path(cfg["paths"][key])
        cfg["paths"][key] = p if p.is_absolute() else ROOT / p
        cfg["paths"][key].mkdir(parents=True, exist_ok=True)
    return cfg


def need(tool, hint=""):
    path = shutil.which(tool)
    if not path:
        sys.exit(f"\n[!] '{tool}' was not found. {hint}\n")
    return path


def run(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height:format=duration", "-of", "json", str(path)],
        capture_output=True, text=True).stdout or "{}"
    d = json.loads(out)
    if not d.get("streams") or "duration" not in d.get("format", {}):
        raise RuntimeError(f"no video found in {path}")
    s = d["streams"][0]
    return float(d["format"]["duration"]), int(s["width"]), int(s["height"])


def hms(sec):
    sec = int(round(sec))
    return f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


def parse_hms(text):
    if text is None:
        return None
    parts = [float(p) for p in str(text).split(":")]
    total = 0.0
    for p in parts:
        total = total * 60 + p
    return total


def slug(text, n=40):
    return re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-")[:n].lower() or "job"


def save_json(path, data):
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def load_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def compile_terms(table):
    """{"A|B|C": weight} -> [(label, regex, weight)]"""
    terms = []
    for key, weight in (table or {}).items():
        aliases = [a.strip() for a in str(key).split("|") if a.strip()]
        pat = r"(?<![\w])(" + "|".join(re.escape(a) for a in aliases) + r")"
        terms.append((aliases[0], re.compile(pat, re.I), float(weight)))
    return terms


# ---------------------------------------------------------------- deleting files Windows has locked
PENDING = "pending_deletes.json"


def safe_unlink(path):
    """Delete a file. If Windows says it's in use (a preview playing, Premiere open), try again later
    instead of stopping the job. Returns True if it's gone now."""
    path = Path(path)
    try:
        path.unlink(missing_ok=True)
        return True
    except PermissionError:
        f = DATA / PENDING
        todo = load_json(f, []) or []
        if str(path) not in todo:
            todo.append(str(path))
            save_json(f, todo)
        return False


def retry_pending_deletes():
    """Delete files that were locked earlier (called after every job and when the app starts)."""
    f = DATA / PENDING
    todo = load_json(f, []) or []
    if not todo:
        return
    left = []
    for p in todo:
        try:
            Path(p).unlink(missing_ok=True)
        except PermissionError:
            left.append(p)
    save_json(f, left)
