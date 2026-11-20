"""Self-update from GitHub. Replaces only the app's code; never touches your data.

Kept on update: .venv (installed packages), bin (ffmpeg/deno), data (settings, layout,
banners, YouTube login), work (downloads), output (Shorts), exports.
"""
import io
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from .util import ROOT

REPO = "smearframestudios-svg/peanut-clipper"
BRANCH = "main"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"
ZIP = f"https://github.com/{REPO}/archive/refs/heads/{BRANCH}.zip"
KEEP = {".venv", "bin", "data", "work", "output", "exports", "compilations", ".git"}


def _get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "PeanutClipper", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _ver(text):
    try:
        return tuple(int(x) for x in text.strip().split("."))
    except ValueError:
        return (0,)


def local_version():
    f = ROOT / "VERSION"
    return f.read_text().strip() if f.exists() else "0.0.0"


def check():
    """{'current', 'latest', 'available', 'notes'}; never raises."""
    cur = local_version()
    try:
        latest = _get(f"{RAW}/VERSION").decode().strip()
    except Exception as e:  # noqa: BLE001
        return {"current": cur, "latest": None, "available": False, "error": str(e)}
    notes = ""
    if _ver(latest) > _ver(cur):
        try:
            log = _get(f"{RAW}/CHANGELOG.md").decode()
            notes = _notes_since(log, cur)
        except Exception:  # noqa: BLE001
            pass
    return {"current": cur, "latest": latest, "available": _ver(latest) > _ver(cur), "notes": notes}


def _notes_since(changelog, cur):
    """Changelog sections newer than the installed version (sections start with '## x.y.z')."""
    out, keep = [], False
    for line in changelog.splitlines():
        if line.startswith("## "):
            keep = _ver(line[3:].split()[0]) > _ver(cur)
        if keep:
            out.append(line)
    return "\n".join(out).strip()


def python_exe():
    exe = Path(sys.executable)
    p = exe.with_name("python.exe")
    return str(p if p.exists() else exe)


def apply(say=print, zip_bytes=None):
    """Download the newest code and swap it in. zip_bytes lets tests supply a local zip."""
    say("Downloading the update...")
    data = zip_bytes if zip_bytes is not None else _get(ZIP, timeout=120)
    with tempfile.TemporaryDirectory() as td:
        zipfile.ZipFile(io.BytesIO(data)).extractall(td)
        roots = [p for p in Path(td).iterdir() if p.is_dir()]
        src = roots[0] if len(roots) == 1 else Path(td)
        if not (src / "clipper" / "__main__.py").exists():
            raise RuntimeError("The download didn't look like Peanut Clipper - nothing was changed.")
        say("Installing the new version...")
        # swap the code folder in one go so a half-copied app can't happen
        new_code = ROOT / "clipper.new"
        shutil.rmtree(new_code, ignore_errors=True)
        shutil.copytree(src / "clipper", new_code)
        old_code = ROOT / "clipper.old"
        shutil.rmtree(old_code, ignore_errors=True)
        (ROOT / "clipper").rename(old_code)
        new_code.rename(ROOT / "clipper")
        shutil.rmtree(old_code, ignore_errors=True)
        for item in src.iterdir():
            if item.name in KEEP or item.name == "clipper":
                continue
            dest = ROOT / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)
    (ROOT / "Peanut Clipper.bat").unlink(missing_ok=True)   # old launcher, replaced by the shortcut
    say("Checking for new packages...")
    flags = 0x08000000 if sys.platform == "win32" else 0
    r = subprocess.run([python_exe(), "-m", "clipper", "setup"], cwd=ROOT, capture_output=True, text=True,
                       creationflags=flags)
    if r.returncode != 0:
        raise RuntimeError("Setup after the update failed:\n" + (r.stdout + r.stderr)[-800:])
    say(f"Updated to {local_version()}.")
    return local_version()
