"""Compilations: long horizontal videos made of many moments (e.g. every GTA crash), from keyword-search matches
across any number of streams.

Each moment is copied out of its stream the moment it's added (1920x1080, 60 fps, with a few seconds of handles
each side), so auto-delete can clean up old streams without breaking a compilation. Saved in compilations/<id>/.
"""
import datetime as dt
import json
import random
import re
import shutil
import subprocess
import uuid
from pathlib import Path
from urllib.parse import quote

from .util import ROOT, load_json, probe, safe_unlink, save_json

FOLDER = ROOT / "compilations"
HANDLE = 5.0          # seconds kept each side of a moment, so it can be widened later (and in Premiere)
LEAD, TAIL = 6, 6     # default seconds before / after the matched words
FPS = 60
TRANSITIONS = ("cut", "flash", "fade")
FADE = 0.5            # crossfade length (seconds)
CRASH_WORDS = "crash, crashed, wreck, my car, flip, flipped, oh no, bro, what the, hit me"


def progress(pct, label):
    print(f"@@ {int(pct)} {label}", flush=True)


def _path(cid):
    return FOLDER / re.sub(r"[^\w-]", "", cid) / "comp.json"


def _safe(name):
    return re.sub(r'[<>:"/\\|?*]+', "", name).strip()[:80] or "Compilation"


SHAPES = ("vertical", "horizontal")


def _src(c, m):
    """(file, in, out, file length, width, height) of one clip for this compilation/collection's shape.
    Collections keep both the finished vertical Short (vfile) and the horizontal moment with handles (file)."""
    if c.get("kind") == "collection" and (c.get("shape", "vertical") == "vertical" or not m.get("file")):
        w, h = (1080, 1920) if c.get("shape", "vertical") == "vertical" else (1920, 1080)
        return m["vfile"], 0.0, m["vdur"], m["vdur"], w, h
    return m["file"], m["a"], m["b"], m["dur"], 1920, 1080


def _length(c):
    return sum(_src(c, m)[2] - _src(c, m)[1] for m in c["moments"])


def _summary(c):
    return {"id": c["id"], "name": c["name"], "count": len(c["moments"]), "length": round(_length(c), 1),
            "goal": c.get("goal", 480), "created": c.get("created", ""), "kind": c.get("kind", "compilation")}


def all_comps(kind="compilation"):
    out = []
    for f in sorted(FOLDER.glob("*/comp.json")) if FOLDER.exists() else []:
        c = load_json(f)
        if c and c.get("kind", "compilation") == kind:
            out.append(_summary(c))
    return sorted(out, key=lambda x: x["created"], reverse=True)


def memberships():
    """Which collections each Review Short is in: {"job:id": ["GTA fails montage", ...]}."""
    out = {}
    for f in sorted(FOLDER.glob("*/comp.json")) if FOLDER.exists() else []:
        c = load_json(f)
        if c and c.get("kind") == "collection":
            for m in c["moments"]:
                out.setdefault(f"{m.get('job')}:{m.get('clip_id')}", []).append({"id": c["id"], "name": c["name"]})
    return out


def get(cid):
    c = load_json(_path(cid))
    if not c:
        raise SystemExit("[!] That compilation wasn't found.")
    return c


def info(cid):
    c = get(cid)
    return dict(c, length=round(_length(c), 1))


def new(name, goal=480, kind="compilation"):
    cid = dt.datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:4]
    kind = "collection" if kind == "collection" else "compilation"
    c = {"id": cid, "name": (name or "").strip()[:60] or f"New {kind}", "goal": int(goal or 480),
         "transition": "cut", "numbers": False, "created": dt.datetime.now().isoformat(timespec="seconds"),
         "kind": kind, "moments": []}
    if kind == "collection":
        c["shape"] = "vertical"
    _path(cid).parent.mkdir(parents=True, exist_ok=True)
    save_json(_path(cid), c)
    return c


def edit(cid, action, body):
    """Quick changes from the Compilations tab (no ffmpeg)."""
    f = _path(cid)
    c = get(cid)
    ms = c["moments"]
    find = lambda: next((m for m in ms if m["mid"] == body.get("mid")), None)  # noqa: E731
    if action == "delete":
        shutil.rmtree(f.parent, ignore_errors=True)
        return None
    if action == "settings":
        if "name" in body:
            c["name"] = str(body["name"]).strip()[:60] or c["name"]
        if "goal" in body:
            c["goal"] = max(30, min(4 * 3600, int(float(body["goal"]))))
        if body.get("transition") in TRANSITIONS:
            c["transition"] = body["transition"]
        if "numbers" in body:
            c["numbers"] = bool(body["numbers"])
        if body.get("shape") in SHAPES:
            c["shape"] = body["shape"]
    elif action == "remove":
        m = find()
        if m:
            ms.remove(m)
            for k in ("file", "vfile", "poster"):
                if m.get(k):
                    safe_unlink(f.parent / m[k])
    elif action == "trim":
        m = find()
        if m:
            a = min(max(0.0, float(body.get("a", m["a"]))), m["dur"])
            b = min(max(0.0, float(body.get("b", m["b"]))), m["dur"])
            if b - a >= 1:
                m["a"], m["b"] = round(a, 2), round(b, 2)
    elif action == "order":
        pos = {mid: i for i, mid in enumerate(body.get("order") or [])}
        ms.sort(key=lambda m: pos.get(m["mid"], 10 ** 6))
    elif action == "shuffle":
        random.shuffle(ms)
    elif action == "oldest":
        ms.sort(key=lambda m: (m.get("stream_date", ""), m.get("stream_t", 0)))
    save_json(f, c)
    return dict(c, length=round(_length(c), 1))


def _enc(cfg, quality=18):
    if cfg.get("render_encoder") == "h264_nvenc":
        return ["-c:v", "h264_nvenc", "-preset", "p5", "-profile:v", "high", "-rc", "vbr", "-cq", str(quality),
                "-b:v", "0", "-bf", "2", "-b_ref_mode", "disabled"]
    return ["-c:v", "libx264", "-preset", "fast", "-profile:v", "high", "-crf", str(quality), "-threads", "4"]


NORM = (f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"
        f"fps={FPS},setsar=1,format=yuv420p")
AUDIO = ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]


def copy_range(cfg, folder, src, start, end):
    """Copy start..end of a video (plus HANDLE seconds each side) into a compilation folder as 1920x1080 60 fps.
    Returns (mid, file name, poster name, where the copy starts in src, copy length)."""
    fdur = probe(src)[0]
    ca, cb = max(0.0, start - HANDLE), min(fdur, end + HANDLE)
    mid = uuid.uuid4().hex[:8]
    name = f"m_{mid}.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{ca:.3f}", "-i", str(src), "-t", f"{cb - ca:.3f}",
           "-map", "0:v:0", "-map", "0:a:0?", "-vf", NORM, "-af", "aresample=async=1"] + _enc(cfg) + \
        ["-pix_fmt", "yuv420p", "-fps_mode", "cfr"] + AUDIO + ["-movflags", "+faststart", name]
    subprocess.run(cmd, check=True, cwd=folder)
    fdur, _, _ = probe(Path(folder) / name)
    poster = f"m_{mid}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{min(fdur, start - ca + 1):.2f}", "-i", name,
                    "-frames:v", "1", "-vf", "scale=320:-2", poster], check=True, cwd=folder)
    return mid, name, poster, ca, fdur


def add_moment(cfg, cid, sid, idx):
    """Copy a keyword-search match into a compilation (one quick encode)."""
    from .search import _segments_from_cache, snap
    f = _path(cid)
    c = get(cid)
    out_dir = Path(cfg["paths"]["output_dir"]) / sid
    data = load_json(out_dir / "search.json")
    if not data:
        raise SystemExit("[!] That search wasn't found.")
    m = next((x for x in data["matches"] if x["i"] == int(idx)), None)
    if not m:
        raise SystemExit("[!] That match wasn't found.")
    if any(x.get("sid") == sid and x.get("i") == m["i"] for x in c["moments"]):
        print("  already in this compilation")
        progress(100, "Already in the compilation")
        return
    from .search import match_video
    from .util import media_duration
    segs, words = _segments_from_cache(data["transcript_cache"])
    if data.get("audio_only"):
        dur = float(data.get("duration") or 0) or media_duration(data["source_file"])
    else:
        src = Path(data["source_file"])
        if not src.exists():
            raise SystemExit("[!] The stream for this search was already deleted. Search again to re-download it.")
        dur = probe(src)[0]
    start, end = snap(segs, max(0.0, m["t"] - LEAD), min(dur, m["t_end"] + TAIL))
    end = min(end, start + 60)
    src, shift = match_video(cfg, data, start, end)
    progress(40, "Copying the moment")
    mid, name, poster, ca, fdur = copy_range(cfg, f.parent, src, start - shift, end - shift)
    said = " ".join(w["w"].strip() for w in words if start <= w["s"] < end)
    title = (m["text"].split('"')[1] if m["kind"] == "chat" and '"' in m["text"] else said)[:70].strip() or m["query"]
    c = get(cid)                       # re-read: the page may have changed it while this ran
    c["moments"].append({
        "mid": mid, "file": name, "poster": poster, "title": title, "query": m["query"], "kind": m["kind"],
        "sid": sid, "i": m["i"], "stream": data.get("source", ""), "stream_date": data.get("created", "")[:10],
        "stream_t": round(data.get("offset", 0) + start, 2),
        "a": round(start - shift - ca, 2), "b": round(min(fdur, end - shift - ca), 2), "dur": round(fdur, 2),
        "added": dt.datetime.now().isoformat(timespec="seconds")})
    save_json(f, c)
    progress(100, f"Added to {c['name']} ({len(c['moments'])} moments, {_mmss(_length(c))})")


def add_short(cfg, cid, job, clip_id):
    """Put a Review Short into a collection: a copy of the finished vertical Short, plus the horizontal moment
    (with handles) cut from the stream while it's still on the PC - so a montage can be either shape."""
    from .library import stream_info
    f = _path(cid)
    c = get(cid)
    jf = Path(cfg["paths"]["output_dir"]) / job / "clips.json"
    data = load_json(jf)
    clip = next((x for x in (data or {}).get("clips", []) if x["id"] == clip_id), None)
    if not clip:
        raise SystemExit("[!] That Short wasn't found.")
    if any(m.get("job") == job and m.get("clip_id") == clip_id for m in c["moments"]):
        progress(100, "Already in this collection")
        return
    short = jf.parent / (clip.get("file") or "")
    if not clip.get("file") or not short.is_file():
        raise SystemExit("[!] That Short's video was already deleted.")
    mid = uuid.uuid4().hex[:8]
    progress(10, "Copying the Short")
    vname = f"v_{mid}.mp4"
    shutil.copy2(short, f.parent / vname)
    vdur = probe(f.parent / vname)[0]
    poster = f"m_{mid}.jpg"
    if clip.get("poster") and (jf.parent / clip["poster"]).is_file():
        shutil.copy2(jf.parent / clip["poster"], f.parent / poster)
    else:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", vname, "-frames:v", "1", "-vf", "scale=360:-2",
                        poster], cwd=f.parent)
    m = {"mid": mid, "vfile": vname, "vdur": round(vdur, 2), "file": "", "a": 0.0, "b": round(vdur, 2), "dur": 0.0,
         "poster": poster, "title": clip.get("title", ""), "job": job, "clip_id": clip_id, "kind": "short",
         "query": "", "added": dt.datetime.now().isoformat(timespec="seconds")}
    info = stream_info(data, clip)
    m.update(stream_date=info["stream_date"], stream_t=info["stream_start"], stream_title=info["stream_title"],
             stream_link=info["stream_link"])
    src = Path(clip.get("source_file") or "")
    if src.is_file():                       # the horizontal moment, for 16:9 montages / Premiere handles
        progress(40, "Copying the horizontal moment")
        dur, _, _ = probe(src)
        s, e = float(clip["src_start"]), float(clip["src_end"])
        ca, cb = max(0.0, s - HANDLE), min(dur, e + HANDLE)
        name = f"m_{mid}.mp4"
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{ca:.3f}", "-i", str(src), "-t", f"{cb - ca:.3f}",
               "-map", "0:v:0", "-map", "0:a:0?", "-vf", NORM, "-af", "aresample=async=1"] + _enc(cfg) + \
            ["-pix_fmt", "yuv420p", "-fps_mode", "cfr"] + AUDIO + ["-movflags", "+faststart", name]
        if subprocess.run(cmd, cwd=f.parent).returncode == 0:
            fd = probe(f.parent / name)[0]
            m.update(file=name, a=round(s - ca, 2), b=round(min(fd, e - ca), 2), dur=round(fd, 2))
    c = get(cid)
    c["moments"].append(m)
    save_json(f, c)
    progress(100, f"Added to {c['name']} ({len(c['moments'])} Shorts, {_mmss(_length(c))})")


def _mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


# ------------------------------------------------------------------ number badge (no fonts needed)
_DIGITS = {
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    "#": ["01010", "01010", "11111", "01010", "11111", "01010", "01010"],
}


def _badge(text, path, px=12):
    """A small '#12' badge as raw RGBA (yellow on dark). Returns (width, height)."""
    import numpy as np
    pad, gap = 2 * px, px
    cw = 5 * px
    w = pad * 2 + len(text) * cw + (len(text) - 1) * gap
    h = pad * 2 + 7 * px
    img = np.zeros((h, w, 4), dtype=np.uint8)
    img[:, :] = (17, 18, 20, 215)
    for k, ch in enumerate(text):
        rows = _DIGITS.get(ch)
        if not rows:
            continue
        x0 = pad + k * (cw + gap)
        for r, line in enumerate(rows):
            for q, bit in enumerate(line):
                if bit == "1":
                    img[pad + r * px: pad + (r + 1) * px, x0 + q * px: x0 + (q + 1) * px] = (255, 201, 60, 255)
    Path(path).write_bytes(img.tobytes())
    return w, h


# ------------------------------------------------------------------ export
def _export_folder(cfg):
    st = cfg["settings"]
    folder = Path(st.get("export_folder") or (ROOT / "exports"))
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _unique(path):
    n = 2
    p = path
    while p.exists():
        p = path.with_name(f"{path.stem} ({n}){path.suffix}")
        n += 1
    return p


def export_video(cfg, cid):
    """One 16:9 video of every moment in order, with the chosen transition."""
    c = get(cid)
    ms = c["moments"]
    if not ms:
        raise SystemExit("[!] There's nothing in it yet.")
    folder = _export_folder(cfg)
    stamp = dt.datetime.now().strftime("%Y-%m-%d")
    out = _unique(folder / f"{stamp} - {_safe(c['name'])}.mp4")
    tmp = _path(cid).parent / "_export"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir()
    try:
        pieces = []
        n = len(ms)
        for k, m in enumerate(ms, 1):
            progress(2 + 80 * (k - 1) / n, f"Preparing clip {k} of {n}")
            name, a, b, _, W, H = _src(c, m)
            src = _path(cid).parent / name
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(src)]
            _, sw, sh = probe(src)
            if (sw, sh) == (W, H):
                vf = "[0:v]setpts=PTS-STARTPTS"
            else:                                  # a vertical Short in a 16:9 montage: blurred sides
                vf = (f"[0:v]setpts=PTS-STARTPTS,split[x][y];[x]scale={W}:{H}:force_original_aspect_ratio=increase,"
                      f"crop={W}:{H},boxblur=22:2,eq=brightness=-0.15[bg];[y]scale=-2:{H}[fg];"
                      f"[bg][fg]overlay=(W-w)/2:0,setsar=1")
            if c.get("transition") == "flash" and k > 1:
                vf += ",fade=t=in:st=0:d=0.25:color=white"
            if c.get("numbers"):
                bw, bh = _badge(f"#{k}", tmp / f"b{k}.rgba")
                cmd += ["-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{bw}x{bh}", "-i", str(tmp / f"b{k}.rgba")]
                vf += f"[v0];[v0][1:v]overlay=60:60:enable='lt(t,2.5)':format=auto,format=yuv420p[v]"
            else:
                vf += ",format=yuv420p[v]"
            p = tmp / f"p{k:03d}.mp4"
            subprocess.run(cmd + ["-filter_complex", vf, "-map", "[v]", "-map", "0:a:0?", "-af", "asetpts=PTS-STARTPTS",
                                  "-r", str(FPS)] + _enc(cfg) + ["-pix_fmt", "yuv420p", "-fps_mode", "cfr"] + AUDIO +
                           [str(p)], check=True)
            pieces.append(p)
        progress(85, "Joining the moments")
        if c.get("transition") == "fade" and len(pieces) > 1:
            lens = [probe(p)[0] for p in pieces]
            cmd = ["ffmpeg", "-v", "error", "-y"]
            for p in pieces:
                cmd += ["-i", str(p)]
            fc, v, a, off = "", "0:v", "0:a", 0.0
            for k in range(1, len(pieces)):
                off += lens[k - 1] - FADE
                fc += (f"[{v}][{k}:v]xfade=transition=fade:duration={FADE}:offset={off:.3f}[v{k}];"
                       f"[{a}][{k}:a]acrossfade=d={FADE}[a{k}];")
                v, a = f"v{k}", f"a{k}"
            subprocess.run(cmd + ["-filter_complex", fc.rstrip(";"), "-map", f"[{v}]", "-map", f"[{a}]"] + _enc(cfg) +
                           ["-pix_fmt", "yuv420p"] + AUDIO + ["-movflags", "+faststart", str(out)], check=True)
        else:
            lst = tmp / "list.txt"
            lst.write_text("".join(f"file '{p.name}'\n" for p in pieces), encoding="utf-8")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst.name, "-c", "copy",
                            "-movflags", "+faststart", str(out)], check=True, cwd=tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"  exported: {out}")
    c = get(cid)
    c["exported_to"] = str(out)
    save_json(_path(cid), c)
    progress(100, f"{'Montage' if c.get('kind') == 'collection' else 'Compilation'} exported ({_mmss(probe(out)[0])})")
    return out


def _xml(c, files, folder):
    """Final Cut Pro 7 XML (Premiere: File > Import) - one sequence, each moment on its own cut."""
    def url(p):
        s = Path(p).resolve().as_posix()
        return "file://localhost/" + quote(s.lstrip("/"), safe="/:")

    def rate():
        return f"<rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate>"

    def esc(s):
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    vid, aud, t = [], [], 0
    W, H = 1920, 1080
    for k, (m, p) in enumerate(zip(c["moments"], files), 1):
        _, a, b, d, W, H = _src(c, m)
        try:
            _, fw, fh = probe(p)               # the file's real size (a vertical Short in a 16:9 sequence)
        except RuntimeError:
            fw, fh = W, H
        fd = int(round(d * FPS))
        i0, i1 = int(round(a * FPS)), int(round(b * FPS))
        s, e = t, t + (i1 - i0)
        fileel = (f'<file id="file-{k}"><name>{esc(p.name)}</name><pathurl>{url(p)}</pathurl>{rate()}'
                  f"<duration>{fd}</duration><media><video><samplecharacteristics>{rate()}<width>{fw}</width>"
                  f"<height>{fh}</height></samplecharacteristics></video><audio><samplecharacteristics>"
                  f"<depth>16</depth><samplerate>48000</samplerate></samplecharacteristics><channelcount>2</channelcount>"
                  f"</audio></media></file>")
        common = f"<name>{esc(p.stem)}</name><enabled>TRUE</enabled><duration>{fd}</duration>{rate()}" \
                 f"<start>{s}</start><end>{e}</end><in>{i0}</in><out>{i1}</out>"
        links = (f'<link><linkclipref>v{k}</linkclipref><mediatype>video</mediatype><trackindex>1</trackindex>'
                 f'<clipindex>{k}</clipindex></link><link><linkclipref>a{k}</linkclipref><mediatype>audio</mediatype>'
                 f'<trackindex>1</trackindex><clipindex>{k}</clipindex></link>')
        vid.append(f'<clipitem id="v{k}">{common}{fileel}{links}</clipitem>')
        aud.append(f'<clipitem id="a{k}">{common}<file id="file-{k}"/><sourcetrack><mediatype>audio</mediatype>'
                   f'<trackindex>1</trackindex></sourcetrack>{links}</clipitem>')
        t = e
    fmt = (f"<format><samplecharacteristics>{rate()}<width>{W}</width><height>{H}</height>"
           f"<pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics></format>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4">'
            f'<sequence id="sequence-1"><name>{esc(c["name"])}</name><duration>{t}</duration>{rate()}'
            f"<media><video>{fmt}<track>{''.join(vid)}</track></video>"
            f"<audio><numOutputChannels>2</numOutputChannels><track>{''.join(aud)}</track></audio></media>"
            "</sequence></xmeml>\n")


def export_premiere(cfg, cid):
    """Every moment as its own file (with handles) + a sequence XML with each one on its own cut."""
    c = get(cid)
    if not c["moments"]:
        raise SystemExit("[!] There's nothing in it yet.")
    folder = _unique(_export_folder(cfg) / f"{_safe(c['name'])} (Premiere)")
    folder.mkdir(parents=True)
    files = []
    n = len(c["moments"])
    for k, m in enumerate(c["moments"], 1):
        progress(5 + 85 * (k - 1) / n, f"Copying clip {k} of {n}")
        dest = folder / f"{k:02d} - {_safe(m['title'])[:50]}.mp4"
        shutil.copy2(_path(cid).parent / _src(c, m)[0], dest)
        files.append(dest)
    xml = folder / f"{_safe(c['name'])}.xml"
    xml.write_text(_xml(c, files, folder), encoding="utf-8")
    (folder / "How to open in Premiere.txt").write_text(
        "In Premiere Pro: File > Import, pick the .xml file in this folder.\n"
        "You get a sequence with every moment already cut in order. Each clip has a few extra seconds\n"
        "on both ends, so you can drag the edges out if a moment needs more room.\n", encoding="utf-8")
    print(f"  exported: {folder}")
    c = get(cid)
    c["premiere_to"] = str(folder)
    save_json(_path(cid), c)
    progress(100, "Exported for Premiere")
    return folder


def in_use(cid):
    """Moments already in a compilation, as {(sid, i): position} so search results can say 'Added (4th)'."""
    try:
        c = get(cid)
    except SystemExit:
        return {}
    return {f"{m['sid']}:{m['i']}": k for k, m in enumerate(c["moments"], 1)}


if __name__ == "__main__":
    print(json.dumps(all_comps(), indent=1))
