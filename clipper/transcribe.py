"""Speech-to-text with word timings (faster-whisper). Only the candidate windows are
transcribed, so a 7-hour stream takes minutes, not hours."""
import os
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

from .util import load_json, save_json

_model = None
_failed = False


def _get_model(cfg):
    global _model, _failed
    if _model is None and not _failed:
        try:
            from faster_whisper import WhisperModel
            w = cfg["whisper"]
            print(f"  loading speech model '{w['model']}' (first run downloads it)...")
            threads = max(2, (os.cpu_count() or 4) // 2)   # leave half the CPU free for you
            try:
                _model = WhisperModel(w["model"], device=w["device"], compute_type=w["compute_type"],
                                      cpu_threads=threads)
            except Exception as e:  # noqa: BLE001
                if w["device"] == "cpu":
                    raise
                print(f"  [!] GPU speech failed ({e}); using CPU")
                _model = WhisperModel(w["model"], device="cpu", compute_type="int8", cpu_threads=threads)
        except Exception as e:  # noqa: BLE001
            print(f"  [!] speech model unavailable ({e}). Clips will have no captions or name detection.")
            _failed = True
    return _model


def transcribe_range(video, start, dur, cfg, cache_path):
    """Returns {"words": [{"w","s","e"}], "segments": [{"s","e","text"}]} with absolute times."""
    cache = load_json(cache_path, {}) or {}
    key = f"{start:.1f}-{dur:.1f}"
    if key in cache:
        return cache[key]
    model = _get_model(cfg)
    result = {"words": [], "segments": []}
    if model is None:
        return result
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "a.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.2f}", "-t", f"{dur:.2f}",
                        "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
        # Load the wav ourselves and hand Whisper raw samples. This skips PyAV entirely,
        # which breaks when an older/newer 'av' package is installed.
        with wave.open(str(wav), "rb") as wf:
            pcm = wf.readframes(wf.getnframes())
        samples = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
        if samples.size < 1600:
            return result
        segments, _ = model.transcribe(samples, word_timestamps=True, vad_filter=True,
                                       language="en" if cfg["whisper"]["model"].endswith(".en") else None)
        for seg in segments:
            result["segments"].append({"s": start + seg.start, "e": start + seg.end, "text": seg.text.strip()})
            for w in seg.words or []:
                result["words"].append({"w": w.word.strip(), "s": start + w.start, "e": start + w.end})
    cache[key] = result
    save_json(cache_path, cache)
    return result
