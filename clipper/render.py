"""Cuts a moment out of the stream and renders a 1080x1920 Short."""
import json
import subprocess
from pathlib import Path

W, H = 1080, 1920


def _even(v):
    return max(2, int(v) // 2 * 2)


def _crop(box, sw, sh):
    x, y = box["x"] * sw, box["y"] * sh
    w, h = box["w"] * sw, box["h"] * sh
    w = min(w, sw - x)
    h = min(h, sh - y)
    return f"crop={_even(w)}:{_even(h)}:{int(x)}:{int(y)}"


def layout_filter(cfg, sw, sh, src="0:v", out="v", tag=""):
    """Returns (filter text from [src] ending in [out], caption_y, seam)."""
    lay = cfg["layout"]
    a, b, t, g = (f"{x}{tag}" for x in ("a", "b", "t", "g"))
    if lay.get("mode") == "stack":
        top = _even(lay["top_height"])
        bot = H - top
        fc = (f"[{src}]split=2[{a}][{b}];"
              f"[{a}]{_crop(lay['avatar'], sw, sh)},scale={W}:{top}:force_original_aspect_ratio=increase,crop={W}:{top}[{t}];"
              f"[{b}]{_crop(lay['gameplay'], sw, sh)},scale={W}:{bot}:force_original_aspect_ratio=increase,crop={W}:{bot}[{g}];"
              f"[{t}][{g}]vstack=inputs=2,setsar=1[{out}]")
        return fc, top, top
    if lay.get("mode") == "single":
        fc = (f"[{src}]{_crop(lay['gameplay'], sw, sh)},scale={W}:{H}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H},setsar=1[{out}]")
        return fc, H * 0.72, H // 2
    fg_h = _even(W * sh / sw)
    bg, fg = f"bg{tag}", f"fg{tag}"
    fc = (f"[{src}]split=2[{a}][{b}];"
          f"[{a}]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=22:2,eq=brightness=-0.18[{bg}];"
          f"[{b}]scale={W}:{fg_h}[{fg}];[{bg}][{fg}]overlay=0:(H-h)/2,setsar=1[{out}]")
    return fc, min(H - 220, H / 2 + fg_h / 2 + 150), (H - fg_h) // 2


LOOKS = ("normal", "closeup", "gameplay")
BANNERS = ("layout", "bottom", "top", "off")


def look_filter(cfg, sw, sh, look, box, src, out, tag):
    """One look for part of a Short: normal = the layout, closeup = Peanut fills the screen,
    gameplay = the game fills the screen. box = the part of the stream to show (0..1), else the layout's."""
    if look not in ("closeup", "gameplay"):
        return layout_filter(cfg, sw, sh, src, out, tag)
    lay = cfg["layout"]
    b = box or lay.get("avatar" if look == "closeup" else "gameplay") or {"x": 0, "y": 0, "w": 1, "h": 1}
    fc = (f"[{src}]{_crop(b, sw, sh)},scale={W}:{H}:force_original_aspect_ratio=increase,"
          f"crop={W}:{H},setsar=1[{out}]")
    return fc, H * 0.70, H // 2

def _encoder_args(cfg):
    if cfg.get("render_encoder") == "h264_nvenc":
        return ["-c:v", "h264_nvenc", "-preset", "p5", "-profile:v", "high", "-rc", "vbr", "-cq", "21", "-b:v", "0",
                "-bf", "2", "-b_ref_mode", "disabled"]
    return ["-c:v", "libx264", "-preset", "veryfast", "-profile:v", "high", "-crf", "20", "-threads", "4"]


IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def overlay_inputs(cfg, seam, banner="layout", first=1, tag="", cur="v"):
    """Your banners: (extra ffmpeg inputs, filter text that takes [cur], final label).
    banner: layout = where the Layout screen puts them, bottom/top = moved there, off = no banners.
    first = the ffmpeg input number the first banner gets."""
    from .util import DATA
    inputs, chain = [], ""
    k = 0
    if banner == "off":
        return inputs, chain, cur
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
        idx = first + k
        k += 1
        if path.suffix.lower() in IMAGE_EXT:
            inputs += ["-loop", "1", "-i", str(path)]
        else:
            inputs += ["-stream_loop", "-1", "-i", str(path)]
        o, vo = f"o{tag}_{k}", f"vo{tag}_{k}"
        pos = ov.get("position", "full")
        if pos == "full":
            chain += f";[{idx}:v]scale={W}:{H},format=rgba[{o}];[{cur}][{o}]overlay=0:0:shortest=1[{vo}]"
            cur = vo
            continue
        off = int(ov.get("offset", 0))
        if banner in ("bottom", "top"):
            pos, off = banner, 0                       # moved for this part of the Short
        y = {"top": "0", "bottom": "H-h", "seam": f"{seam}-h/2"}.get(pos, "0")
        y = y.replace("H", str(H))
        chain += (f";[{idx}:v]scale={W}:-2,format=rgba[{o}];"
                  f"[{cur}][{o}]overlay=0:'{y}+({off})':shortest=1[{vo}]")
        cur = vo
    return inputs, chain, cur


def clean_sections(sections, start, end):
    """Parts of the Short with their own look, in seconds from the Short's start (only the ones that differ)."""
    out = []
    for sec in sections or []:
        a, b = max(0.0, float(sec["start"]) - start), min(end - start, float(sec["end"]) - start)
        look = sec.get("look") if sec.get("look") in LOOKS else "normal"
        ban = sec.get("banner") if sec.get("banner") in BANNERS else "layout"
        if b - a < 0.05 or (look == "normal" and ban == "layout"):
            continue
        out.append({"start": a, "end": b, "look": look, "banner": ban, "box": sec.get("box") if look != "normal" else None})
    return out


def compose(cfg, sw, sh, sections, words, start, end, out_dir, stem):
    """The whole picture: (extra inputs, filter_complex, final label, caption files made).
    Every look used gets its own chain; each part's look is laid over the normal one only while that part plays."""
    from .captions import build_ass
    combos = [("normal", "layout", None)]
    when = {0: []}
    for sec in sections:
        key = (sec["look"], sec["banner"], json.dumps(sec["box"], sort_keys=True) if sec["box"] else None)
        if key not in combos:
            combos.append(key)
        when.setdefault(combos.index(key), []).append((sec["start"], sec["end"]))
    n = len(combos)
    fc = f"[0:v]split={n}" + "".join(f"[s{i}]" for i in range(n)) if n > 1 else "[0:v]null[s0]"
    inputs, ass_files, finals = [], [], []
    for i, (look, ban, box) in enumerate(combos):
        part, cap_y, seam = look_filter(cfg, sw, sh, look, json.loads(box) if box else None, f"s{i}", f"l{i}", str(i))
        ins, chain, cur = overlay_inputs(cfg, seam, ban, 1 + inputs.count("-i"), str(i), f"l{i}")
        inputs += ins
        fc += ";" + part + chain
        if cfg["captions"]["enabled"] and words:
            ass, nw = build_ass(words, start, end, cfg, cap_y)
            if nw:
                name = f"{stem}.ass" if i == 0 else f"{stem}_{i}.ass"
                (Path(out_dir) / name).write_text(ass, encoding="utf-8")
                ass_files.append(name)
                fc += f";[{cur}]ass={name}[c{i}]"   # relative name avoids Windows path escaping
                cur = f"c{i}"
        finals.append(cur)
    last = finals[0]
    for i in range(1, n):
        en = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in when[i])
        fc += f";[{last}][{finals[i]}]overlay=0:0:enable='{en}'[m{i}]"
        last = f"m{i}"
    return inputs, fc, last, ass_files


def render_short(src, start, end, out_path, words, cfg, sw, sh, sections=None):
    """sections: parts with their own look/banner, in seconds of the stream file (see clean_sections)."""
    out_path = Path(out_path)
    out_dir = out_path.parent
    secs = clean_sections(sections, start, end)
    extra_in, fc, last, ass_files = compose(cfg, sw, sh, secs, words, start, end, out_dir, out_path.stem)
    fps = str(cfg.get("settings", {}).get("output_fps", 60))
    cmd = (["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.2f}", "-i", str(Path(src).resolve())] + extra_in +
           ["-t", f"{end - start:.2f}", "-filter_complex", fc, "-map", f"[{last}]", "-map", "0:a:0?",
            "-r", fps] + _encoder_args(cfg)) + ["-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", out_path.name]
    subprocess.run(cmd, check=True, cwd=out_dir)
    for name in ass_files[1:]:                 # extra caption files are only needed while rendering
        (out_dir / name).unlink(missing_ok=True)
    poster = out_path.with_suffix(".jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{min(1.5, (end - start) / 2):.2f}",
                    "-i", out_path.name, "-frames:v", "1", "-vf", "scale=360:-2", poster.name],
                   check=True, cwd=out_dir)
    return out_path, poster


def snapshot(src, at, out_png, cfg, sw, sh, section=None, vertical=True):
    """One full-size PNG of the frame at `at` (seconds in src): as it looks in the Short, or the plain stream frame."""
    out_png = Path(out_png)
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0.0, at):.3f}", "-i", str(Path(src).resolve())]
    if vertical:
        secs = clean_sections([dict(section, start=at - 1, end=at + 1)] if section else [], at, at + 1)
        if secs:
            secs[0].update(start=0.0, end=1.0)
        extra_in, fc, last, _ = compose(dict(cfg, captions=dict(cfg["captions"], enabled=False)), sw, sh, secs, [],
                                        at, at + 1, out_png.parent, out_png.stem)
        cmd += extra_in + ["-filter_complex", fc, "-map", f"[{last}]"]
    else:
        cmd += ["-map", "0:v:0"]
    subprocess.run(cmd + ["-frames:v", "1", "-update", "1", str(out_png)], check=True)
    return out_png
