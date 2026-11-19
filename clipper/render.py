"""Cuts a moment out of the stream and renders a 1080x1920 Short."""
import subprocess
from pathlib import Path

from .captions import build_ass

W, H = 1080, 1920


def _even(v):
    return max(2, int(v) // 2 * 2)


def _crop(box, sw, sh):
    x, y = box["x"] * sw, box["y"] * sh
    w, h = box["w"] * sw, box["h"] * sh
    w = min(w, sw - x)
    h = min(h, sh - y)
    return f"crop={_even(w)}:{_even(h)}:{int(x)}:{int(y)}"


def layout_filter(cfg, sw, sh):
    """Returns (filter_complex ending in [v], caption_y)."""
    lay = cfg["layout"]
    if lay.get("mode") == "stack":
        top = _even(lay["top_height"])
        bot = H - top
        fc = (f"[0:v]split=2[a][b];"
              f"[a]{_crop(lay['avatar'], sw, sh)},scale={W}:{top}:force_original_aspect_ratio=increase,crop={W}:{top}[t];"
              f"[b]{_crop(lay['gameplay'], sw, sh)},scale={W}:{bot}:force_original_aspect_ratio=increase,crop={W}:{bot}[g];"
              f"[t][g]vstack=inputs=2,setsar=1[v]")
        return fc, top, top
    if lay.get("mode") == "single":
        fc = (f"[0:v]{_crop(lay['gameplay'], sw, sh)},scale={W}:{H}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H},setsar=1[v]")
        return fc, H * 0.72, H // 2
    fg_h = _even(W * sh / sw)
    fc = (f"[0:v]split=2[a][b];"
          f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=22:2,eq=brightness=-0.18[bg];"
          f"[b]scale={W}:{fg_h}[fg];[bg][fg]overlay=0:(H-h)/2,setsar=1[v]")
    return fc, min(H - 220, H / 2 + fg_h / 2 + 150), (H - fg_h) // 2


def _encoder_args(cfg):
    if cfg.get("render_encoder") == "h264_nvenc":
        return ["-c:v", "h264_nvenc", "-preset", "p5", "-profile:v", "high", "-rc", "vbr", "-cq", "21", "-b:v", "0",
                "-bf", "2", "-b_ref_mode", "disabled"]
    return ["-c:v", "libx264", "-preset", "veryfast", "-profile:v", "high", "-crf", "20", "-threads", "4"]


IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def overlay_inputs(cfg, seam):
    """Your banners: (extra ffmpeg inputs, filter text that takes [v], final label)."""
    from .util import DATA
    inputs, chain = [], ""
    k = 0
    cur = "v"
    only = cfg.get("layout", {}).get("banners")      # this layout's banners (None = every banner that's on)
    for ov in cfg.get("settings", {}).get("overlays", []):
        path = DATA / "overlays" / ov.get("file", "")
        if not path.is_file():
            continue
        if only is not None:
            if ov.get("file") not in only:
                continue
        elif not ov.get("enabled", True):
            continue
        k += 1
        idx = k   # input 0 is the stream
        if path.suffix.lower() in IMAGE_EXT:
            inputs += ["-loop", "1", "-i", str(path)]
        else:
            inputs += ["-stream_loop", "-1", "-i", str(path)]
        pos = ov.get("position", "full")
        if pos == "full":
            chain += f";[{idx}:v]scale={W}:{H},format=rgba[o{k}];[{cur}][o{k}]overlay=0:0:shortest=1[vo{k}]"
            cur = f"vo{k}"
            continue
        y = {"top": "0", "bottom": "H-h", "seam": f"{seam}-h/2"}.get(pos, "0")
        y = y.replace("H", str(H))
        off = int(ov.get("offset", 0))
        chain += (f";[{idx}:v]scale={W}:-2,format=rgba[o{k}];"
                  f"[{cur}][o{k}]overlay=0:'{y}+({off})':shortest=1[vo{k}]")
        cur = f"vo{k}"
    return inputs, chain, cur


def render_short(src, start, end, out_path, words, cfg, sw, sh):
    out_path = Path(out_path)
    out_dir = out_path.parent
    fc, cap_y, seam = layout_filter(cfg, sw, sh)
    extra_in, ov_chain, last = overlay_inputs(cfg, seam)
    fc += ov_chain
    vmap = f"[{last}]"
    ass_name = out_path.stem + ".ass"
    if cfg["captions"]["enabled"] and words:
        ass, n = build_ass(words, start, end, cfg, cap_y)
        if n:
            (out_dir / ass_name).write_text(ass, encoding="utf-8")
            fc += f";[{last}]ass={ass_name}[out]"   # relative name avoids Windows path escaping
            vmap = "[out]"
    fps = str(cfg.get("settings", {}).get("output_fps", 60))
    cmd = (["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.2f}", "-i", str(Path(src).resolve())] + extra_in +
           ["-t", f"{end - start:.2f}", "-filter_complex", fc, "-map", vmap, "-map", "0:a:0?",
            "-r", fps] + _encoder_args(cfg)) + ["-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", out_path.name]
    subprocess.run(cmd, check=True, cwd=out_dir)
    poster = out_path.with_suffix(".jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{min(1.5, (end - start) / 2):.2f}",
                    "-i", out_path.name, "-frames:v", "1", "-vf", "scale=360:-2", poster.name],
                   check=True, cwd=out_dir)
    return out_path, poster
