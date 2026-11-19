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
    "export_folder": "",
    "export_handles_sec": 3,
    "export_vertical_too": False,
    "output_fps": 60,
    "overlays": [],
    "twitch_client_id": "",
    "twitch_client_secret": "",
}


def setup_env():
    """Put our own tools (and NVIDIA's CUDA DLLs from pip) first on PATH."""
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


def load_config():
    import yaml
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    DATA.mkdir(exist_ok=True)
    lay = DATA / "layout.json"  # written by the layout screen
    if lay.exists():
        cfg["layout"].update(json.loads(lay.read_text(encoding="utf-8")))
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
