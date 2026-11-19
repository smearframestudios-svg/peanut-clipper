import subprocess

import numpy as np


def loudness_per_sec(path, sr=8000):
    """Loudness (dB) for every second of the file, streamed so 8-hour VODs don't eat RAM."""
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
        stdout=subprocess.PIPE)
    out = []
    chunk = sr * 2
    while True:
        buf = proc.stdout.read(chunk)
        if not buf:
            break
        a = np.frombuffer(buf, dtype=np.int16).astype(np.float32) / 32768.0
        rms = float(np.sqrt(np.mean(a * a))) if a.size else 0.0
        out.append(20 * np.log10(rms + 1e-6))
    proc.wait()
    return np.array(out, dtype=np.float32)
