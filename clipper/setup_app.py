"""First-run setup: Python packages, ffmpeg, Deno, NVIDIA GPU libraries, and a hardware test.
Runs every time the app starts but only does work when something is missing."""
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

from .util import BIN, DATA, ROOT, load_json, save_json

FFMPEG_ZIP = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
DENO_ZIP = "https://github.com/denoland/deno/releases/latest/download/deno-x86_64-pc-windows-msvc.zip"
GPU_PKGS = ["nvidia-cublas-cu12", "nvidia-cudnn-cu12==9.*"]


def say(msg):
    print(msg, flush=True)


def _pip(args):
    subprocess.run([sys.executable, "-m", "pip", "install", "--disable-pip-version-check"] + args, check=True)


def _download(url, label):
    say(f"  downloading {label}...")
    req = urllib.request.Request(url, headers={"User-Agent": "PeanutClipper"})
    with urllib.request.urlopen(req, timeout=60) as r:
        total = int(r.headers.get("Content-Length") or 0)
        buf = io.BytesIO()
        got = 0
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            buf.write(chunk)
            got += len(chunk)
            if total:
                print(f"\r    {got * 100 // total:3d}%  ({got >> 20} / {total >> 20} MB)", end="", flush=True)
        print()
    return buf


def _extract(buf, names):
    BIN.mkdir(exist_ok=True)
    with zipfile.ZipFile(buf) as z:
        for info in z.infolist():
            base = Path(info.filename).name.lower()
            if base in names:
                (BIN / base).write_bytes(z.read(info))


def _has_nvidia():
    return bool(shutil.which("nvidia-smi")) or Path(r"C:\Windows\System32\nvidia-smi.exe").exists()


def ensure_packages():
    req = (ROOT / "requirements.txt").read_bytes()
    want = hashlib.sha1(req + (b"gpu" if _has_nvidia() else b"")).hexdigest()
    marker = DATA / "packages.ok"
    if marker.exists() and marker.read_text().strip() == want:
        return
    say("\n[1/4] Installing Python packages (first time takes a few minutes)...")
    _pip(["-r", str(ROOT / "requirements.txt")])
    if _has_nvidia():
        say("\n      NVIDIA card found - installing GPU libraries (about 1.5 GB, one time only)...")
        try:
            _pip(GPU_PKGS)
        except subprocess.CalledProcessError:
            say("  [!] GPU libraries failed to install - the app will use the CPU instead.")
    marker.write_text(want)
    (DATA / "hardware.json").unlink(missing_ok=True)   # re-test hardware after package changes


def ensure_tools():
    BIN.mkdir(exist_ok=True)
    # reuse an ffmpeg that's already next to the app or in the old peanut-clipper folder
    if not (BIN / "ffmpeg.exe").exists() and os.name == "nt":
        for cand in [ROOT, ROOT.parent, ROOT.parent / "peanut-clipper", ROOT.parent / "peanut-clipper" / "peanut-clipper"]:
            if (cand / "ffmpeg.exe").exists() and (cand / "ffprobe.exe").exists():
                shutil.copy2(cand / "ffmpeg.exe", BIN / "ffmpeg.exe")
                shutil.copy2(cand / "ffprobe.exe", BIN / "ffprobe.exe")
                break
    if os.name == "nt" and not (BIN / "ffmpeg.exe").exists():
        say("\n[2/4] Getting ffmpeg (video tool, ~100 MB)...")
        _extract(_download(FFMPEG_ZIP, "ffmpeg"), {"ffmpeg.exe", "ffprobe.exe"})
    if os.name == "nt" and not (BIN / "deno.exe").exists() and not shutil.which("deno"):
        say("\n[3/4] Getting Deno (needed for YouTube downloads, ~40 MB)...")
        _extract(_download(DENO_ZIP, "Deno"), {"deno.exe"})


def hardware_test(force=False):
    path = DATA / "hardware.json"
    hw = load_json(path)
    if hw and not force:
        return hw
    say("\n[4/4] Testing your graphics card...")
    hw = {"nvenc": False, "whisper_gpu": False}
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=640x360:d=1",
                        "-c:v", "h264_nvenc", "-f", "null", "-"], capture_output=True)
    hw["nvenc"] = r.returncode == 0
    say(f"  GPU video rendering: {'YES' if hw['nvenc'] else 'no (using CPU)'}")
    if _has_nvidia():
        say("  testing GPU speech recognition (downloads the speech model the first time)...")
        try:
            r = subprocess.run([sys.executable, "-m", "clipper", "whispertest"],
                               capture_output=True, text=True, timeout=1800)
            hw["whisper_gpu"] = r.returncode == 0 and "WHISPER_GPU_OK" in r.stdout
            if not hw["whisper_gpu"]:
                hw["gpu_error"] = (r.stderr or r.stdout)[-600:]
        except subprocess.TimeoutExpired:
            hw["gpu_error"] = "timed out"
    say(f"  GPU speech recognition: {'YES' if hw['whisper_gpu'] else 'no (using CPU)'}")
    save_json(path, hw)
    return hw


def whisper_gpu_selftest():
    """Runs in its own process: a missing CUDA DLL can crash Python outright."""
    import numpy as np
    from faster_whisper import WhisperModel

    from .util import load_config
    cfg = load_config()
    m = WhisperModel(cfg["whisper"]["model"], device="cuda", compute_type="float16")
    segs, _ = m.transcribe(np.zeros(16000 * 2, dtype=np.float32), language="en")
    list(segs)
    print("WHISPER_GPU_OK", flush=True)


def run_setup():
    DATA.mkdir(exist_ok=True)
    ensure_packages()
    ensure_tools()
    hardware_test()
    say("\nSetup OK.\n")
