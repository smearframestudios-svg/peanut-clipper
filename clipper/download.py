"""Downloads a stream VOD (YouTube or Twitch) plus its chat replay."""
import os
import re
import shutil
import subprocess
from pathlib import Path

from .util import hms, need


def is_url(s):
    return str(s).startswith(("http://", "https://"))


def cache_key(url, start=None, end=None):
    m = re.search(r"(?:v=|youtu\.be/|/live/|/videos/|/shorts/)([\w-]{6,})", url)
    vid = m.group(1) if m else re.sub(r"\W+", "_", url)[-40:]
    rng = f"_{int(start or 0)}-{int(end) if end else 'end'}" if (start or end) else ""
    return vid + rng


def _yt_dlp():
    return [need("yt-dlp", "Run setup.bat (it installs yt-dlp).")]


def video_codec(src):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name",
                        "-of", "csv=p=0", str(src)], capture_output=True, text=True)
    return r.stdout.strip().lower()


def needs_sync_fix(src):
    """True when the stream isn't H.264. YouTube often serves AV1/VP9, which the RTX 2080 can't
    decode in hardware - in the trim editor the picture falls behind the sound. Converted once."""
    src = Path(src)
    if not src.is_file() or (src.parent / "synced.ok").exists():
        return False
    codec = video_codec(src)
    if codec in ("h264", ""):
        (src.parent / "synced.ok").write_text("h264")
        return False
    return True


def _sync_args(cfg):
    """H.264 settings for converted video (GPU encode when available)."""
    gpu = cfg.get("render_encoder") == "h264_nvenc"
    v = (["-c:v", "h264_nvenc", "-preset", "p4", "-profile:v", "high", "-rc", "vbr", "-cq", "19", "-b:v", "0",
          "-bf", "2", "-b_ref_mode", "disabled"] if gpu
         else ["-c:v", "libx264", "-preset", "veryfast", "-profile:v", "high", "-crf", "18", "-threads", "4"])
    return gpu, v + ["-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                     "-af", "aresample=async=1:first_pts=0", "-avoid_negative_ts", "make_zero", "-movflags", "+faststart"]


def run_ffmpeg_progress(cmd, total, lo, hi, label):
    """Run ffmpeg and turn its position into "@@ pct label (x%, about N min left)" lines for the progress bar."""
    import re
    import time as _t
    cmd = cmd[:1] + ["-progress", "pipe:1", "-nostats"] + cmd[1:]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace")
    t0, last = _t.time(), 0.0
    for line in p.stdout:
        m = re.match(r"out_time_us=(\d+)", line.strip())
        if not m or total <= 0:
            if line.strip() and not re.match(r"^[\w.]+=", line.strip()):
                print("  " + line.rstrip(), flush=True)
            continue
        done = int(m.group(1)) / 1e6
        frac = max(0.0, min(1.0, done / total))
        if _t.time() - last < 2:
            continue
        last = _t.time()
        el = last - t0
        left = (el / frac - el) / 60 if frac > 0.02 else None
        eta = (", under a minute left" if left < 1 else f", about {round(left)} min left") if left is not None else ""
        print(f"@@ {int(lo + frac * (hi - lo))} {label} ({frac * 100:.0f}%{eta})", flush=True)
    return p.wait()


def fix_sync(src, cfg):
    """Convert a non-H.264 download to H.264 once (GPU when available)."""
    src = Path(src)
    if not needs_sync_fix(src):
        return src
    print("@@ 33 Converting the stream so it plays smoothly (one time)", flush=True)
    print(f"  converting {video_codec(src) or 'video'} -> H.264 so it plays in sync and edits smoothly...")
    tmp = src.with_name("source.syncing.mp4")
    from .util import probe
    total = probe(src)[0]
    gpu, v = _sync_args(cfg)
    base = ["ffmpeg", "-v", "error", "-y"]
    tail = ["-i", str(src), "-map", "0:v:0", "-map", "0:a:0?"] + v + [str(tmp)]
    label = "Converting the stream so it plays smoothly (one time)"
    rc = run_ffmpeg_progress(base + (["-hwaccel", "cuda"] if gpu else []) + tail, total, 33, 95, label)
    if rc != 0 and gpu:      # GPU decode not available - decode on CPU, still encode on GPU
        rc = run_ffmpeg_progress(base + tail, total, 33, 95, label)
    if rc != 0 or not tmp.exists():
        tmp.unlink(missing_ok=True)
        print("  [!] couldn't convert the stream - continuing with the original download")
        return src
    final = src.with_suffix(".mp4")
    os.replace(tmp, final)
    if final != src:
        src.unlink(missing_ok=True)
    (final.parent / "synced.ok").write_text("ok")
    return final


def full_video(job_dir):
    """The whole video downloaded earlier into this folder, or None."""
    done = [p for p in Path(job_dir).glob("source.*") if p.suffix in (".mp4", ".mkv", ".webm")
            and ".syncing" not in p.name and p.stat().st_size > 1_000_000]
    return done[0] if done else None


def _check_live(url, job_dir):
    """Remember the stream's title; stop if it's still live / not processed yet."""
    got = subprocess.run(_yt_dlp() + ["--no-playlist", "--skip-download", "--print", "%(live_status)s\t%(title)s", url],
                         capture_output=True, text=True, encoding="utf-8", errors="ignore").stdout.strip().splitlines()
    status, _, title = (got[-1] if got else "").partition("\t")
    if title and title != "NA":
        (job_dir / "title.txt").write_text(title, encoding="utf-8")   # shown in History next to the stream time
    if status in ("is_live", "is_upcoming", "post_live"):
        msg = {"is_live": "is LIVE right now", "is_upcoming": "hasn't started yet",
               "post_live": "just ended and YouTube is still processing it"}[status]
        raise SystemExit(f"\n[!] That stream {msg}. Wait until it's a finished replay "
                         f"(usually a few hours after it ends), use Record live, or use an older stream.\n")


def download_audio(url, job_dir, start=None, end=None):
    """Just the sound (about 60 MB an hour) - for keyword search. Uses the full video instead if it's already here."""
    full = full_video(job_dir)
    if full:
        print(f"  using the video downloaded earlier ({full.stat().st_size // 1_000_000} MB)")
        return full
    have = [p for p in job_dir.glob("audio.*") if p.suffix in (".m4a", ".webm", ".opus", ".mp3") and p.stat().st_size > 10_000]
    if have:
        print("  using the sound downloaded earlier")
        return have[0]
    _check_live(url, job_dir)
    cmd = _yt_dlp() + ["-f", "ba[ext=m4a]/ba", "-o", str(job_dir / "audio.%(ext)s"), "--no-playlist"]
    if start is not None or end is not None:
        cmd += ["--download-sections", f"*{hms(start or 0)}-{hms(end) if end else 'inf'}"]
    print("  downloading just the sound (small)...")
    subprocess.run(cmd + [url], check=True)
    have = sorted(job_dir.glob("audio.*"), key=lambda p: p.stat().st_size, reverse=True)
    if not have:
        raise RuntimeError("yt-dlp finished but no sound file was found")
    return have[0]


def download_part(url, cfg, start, end, work_dir):
    """One piece of the video (seconds start-end of the stream), for a match from a sound-only search."""
    d = Path(work_dir) / "_downloads" / cache_key(url, round(start), round(end))
    d.mkdir(parents=True, exist_ok=True)
    return download_video(url, d, cfg, round(start), round(end))


def download_video(url, job_dir, cfg, start=None, end=None):
    done = full_video(job_dir)
    if done:
        print(f"  using the video downloaded earlier ({done.stat().st_size // 1_000_000} MB)")
        return fix_sync(done, cfg)
    _check_live(url, job_dir)
    h = int(cfg["download"]["max_height"])
    cmd = _yt_dlp() + [
        # prefer H.264 + AAC: plays smoothly in the editor and Premiere, decoded by the graphics card
        "-f", (f"bv*[height<={h}][vcodec^=avc1]+ba[ext=m4a]/bv*[height<={h}][vcodec^=avc1]+ba/"
               f"bv*[height<={h}]+ba/b[height<={h}]/bv*+ba/b"),
        "--merge-output-format", "mp4",
        "-o", str(job_dir / "source.%(ext)s"), "--no-playlist",
    ]
    if start is not None or end is not None:
        try:
            print("  downloading just the part you asked for...")
            subprocess.run(cmd + ["--download-sections", f"*{hms(start or 0)}-{hms(end) if end else 'inf'}",
                                  url], check=True)
        except subprocess.CalledProcessError:
            print("  [!] partial download failed - downloading the whole video and cutting it here instead...")
            for f in job_dir.glob("source.*"):
                f.unlink()
            full_cmd = [c if not str(c).endswith("source.%(ext)s") else str(job_dir / "full.%(ext)s") for c in cmd]
            subprocess.run(full_cmd + [url], check=True)
            full = max(job_dir.glob("full.*"), key=lambda p: p.stat().st_size)
            cut = ["ffmpeg", "-v", "error", "-y", "-ss", str(start or 0), "-i", str(full)]
            if end:
                cut += ["-t", str(end - (start or 0))]
            subprocess.run(cut + ["-c", "copy", str(job_dir / "source.mp4")], check=True)
            full.unlink()
    else:
        print("  downloading video (big streams take a while)...")
        subprocess.run(cmd + [url], check=True)
    files = sorted([p for p in job_dir.glob("source.*") if p.suffix in (".mp4", ".mkv", ".webm")], key=lambda p: p.stat().st_size, reverse=True)
    if not files:
        raise RuntimeError("yt-dlp finished but no video file was found")
    return fix_sync(files[0], cfg)


def stream_extras(folder):
    """Stream title + how far into the stream our file starts (a live recording begun late), for clips.json."""
    out = {}
    if not folder:
        return out
    folder = Path(folder)
    try:
        out["stream_title"] = (folder / "title.txt").read_text(encoding="utf-8").strip()
    except OSError:
        pass
    try:
        out["stream_offset"] = float((folder / "live_offset.txt").read_text().strip())
    except (OSError, ValueError):
        pass
    return out


def download_chat(url, job_dir, start=None, end=None):
    """Returns a chat file path or None. YouTube: yt-dlp live_chat. Twitch: TwitchDownloaderCLI if installed."""
    if "youtube.com" in url or "youtu.be" in url:
        found = list(job_dir.glob("chat*.live_chat.json"))
        if found:
            return found[0]
        if (job_dir / "no_chat").exists():
            return None
        print("  downloading YouTube live chat replay...")
        try:
            subprocess.run(_yt_dlp() + ["--skip-download", "--write-subs", "--sub-langs", "live_chat",
                                        "-o", str(job_dir / "chat"), "--no-playlist", url], check=True)
        except subprocess.CalledProcessError:
            print("  [!] no chat replay available - continuing with audio + speech only")
            return None
        found = list(job_dir.glob("chat*.live_chat.json"))
        if not found:
            (job_dir / "no_chat").touch()
            print("  [!] this video has no chat replay (it's probably a normal upload, not a stream).")
        return found[0] if found else None

    m = re.search(r"twitch\.tv/videos/(\d+)", url)
    if m:
        exe = shutil.which("TwitchDownloaderCLI")
        if not exe:
            print("  [!] TwitchDownloaderCLI not found - skipping Twitch chat (see README)")
            return None
        out = job_dir / "chat.json"
        cmd = [exe, "chatdownload", "--id", m.group(1), "-o", str(out), "--collision", "Overwrite"]
        if start:
            cmd += ["-b", str(int(start))]
        if end:
            cmd += ["-e", str(int(end))]
        print("  downloading Twitch chat...")
        subprocess.run(cmd, check=True)
        return out if out.exists() else None
    return None


def download_url(url, out_path):
    subprocess.run(_yt_dlp() + ["-f", "best[ext=mp4]/best", "-o", str(out_path), url], check=True)
    return Path(out_path)


EDIT_PAD = 15 * 60   # the editor gets 15 minutes before and after the Short


def edit_window(src, start, end, cfg, out, minutes=None):
    """Convert just the part of a non-H.264 stream around one Short (a minute or two instead of the whole stream).
    Returns (file, offset): editor time 0 = `offset` seconds into the stream."""
    from .util import probe
    total = probe(src)[0]
    # the owner picks the total minutes (Settings); always at least the Short plus 30 s each side
    pad = EDIT_PAD if minutes is None else max(30.0, (float(minutes) * 60 - (end - start)) / 2)
    a = max(0.0, start - pad)
    b = min(total or end + pad, end + pad)
    gpu, v = _sync_args(cfg)
    tmp = Path(out).with_name(Path(out).stem + ".part.mp4")
    base = ["ffmpeg", "-v", "error", "-y"]
    tail = ["-ss", f"{a:.2f}", "-t", f"{b - a:.2f}", "-i", str(src), "-map", "0:v:0", "-map", "0:a:0?"] + v + [str(tmp)]
    label = f"Converting {round((b - a) / 60)} min around this Short"
    rc = run_ffmpeg_progress(base + (["-hwaccel", "cuda"] if gpu else []) + tail, b - a, 5, 95, label)
    if rc != 0 and gpu:
        rc = run_ffmpeg_progress(base + tail, b - a, 5, 95, label)
    if rc != 0 or not tmp.exists():
        tmp.unlink(missing_ok=True)
        raise SystemExit("[!] Couldn't convert this part of the stream.")
    os.replace(tmp, out)
    return Path(out), round(a, 2), round(b, 2)
