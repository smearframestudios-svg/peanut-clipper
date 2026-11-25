"""Cut out Peanut (Cut-out tab): rotoscopes Peanut off the gameplay behind him, frame by frame, on the owner's PC.

Methods
  follow  RVM (person matting) + U2-Net human (catches the jacket RVM misses), keeping only the shape the owner
          clicked; a box follows him frame to frame so the gameplay, map and banners stay out.
  person  everything those models see as a person (no click needed).
  key     colour key, for green-screen / flat backgrounds.
What
  whole   everything the stream shows of him: head, glasses, lips, shirt, jacket.
  head    only the peanut shell + whatever sits inside its outline (glasses, lips): learns the shell colour around
          the click, takes the outline around it (convex hull) and keeps every Peanut pixel inside it.
Outputs (exports/Cut-outs/): transparent .mov (ProRes 4444) for Premiere, green-screen .mp4, PNG frames.

Models (data/models/, downloaded once from GitHub): RVM mobilenetv3 (Robust Video Matting, GPL-3.0) and U2-Net human
seg (from rembg's releases). They run through ONNX Runtime; on Windows the job loads its own DirectML build from
bin/ort-dml (any DX12 GPU, no CUDA setup), separate from the onnxruntime faster-whisper uses.
"""
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from .util import DATA, ROOT, probe

MODELS = DATA / "models"
DML_DIR = ROOT / "bin" / "ort-dml"
URLS = {
    "rvm_mobilenetv3_fp32.onnx": "https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx",
    "u2net_human_seg.onnx": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx",
}
S = 4                       # masks are tracked at 1/4 size (fast), the soft edge comes from the full-size matte
MAX_SIDE = 1920             # bigger videos are cut out at this size, then scaled back
EDGES = {"sharp": (3, 5), "normal": (7, 9), "soft": (13, 15)}   # (edge blur, core blur) in pixels


def progress(pct, label):
    print(f"@@ {int(pct)} {label}", flush=True)


# ---------- the engine: ONNX Runtime + models ----------
def _runtime():
    """onnxruntime, preferring the DirectML build in bin/ort-dml on Windows (installed once, on first use)."""
    if sys.platform == "win32":
        if not (DML_DIR / "onnxruntime").is_dir():
            progress(1, "Getting the GPU cut-out engine (one time, about 25 MB)")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "--no-deps",
                                "--target", str(DML_DIR), "onnxruntime-directml"], check=True,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            except Exception as e:  # noqa: BLE001
                print(f"  couldn't get the GPU engine ({e}) - using the CPU (slower)")
                shutil.rmtree(DML_DIR, ignore_errors=True)
        if (DML_DIR / "onnxruntime").is_dir():
            sys.path.insert(0, str(DML_DIR))
    import onnxruntime as ort
    return ort


def _download(name):
    MODELS.mkdir(parents=True, exist_ok=True)
    f = MODELS / name
    if f.is_file() and f.stat().st_size > 1_000_000:
        return f
    part = f.with_name(name + ".part")
    progress(2, f"Downloading the cut-out model {name} (one time)")
    with urllib.request.urlopen(URLS[name], timeout=60) as r, open(part, "wb") as out:
        total, done, last = int(r.headers.get("Content-Length") or 0), 0, 0.0
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            out.write(chunk)
            done += len(chunk)
            if total and time.time() - last > 1:
                last = time.time()
                progress(2, f"Downloading the cut-out model ({done * 100 // total}%)")
    os.replace(part, f)
    return f


class Engine:
    def __init__(self, need_body=True):
        ort = _runtime()
        avail = ort.get_available_providers()
        prov = [p for p in ("DmlExecutionProvider", "CUDAExecutionProvider") if p in avail] + ["CPUExecutionProvider"]
        self.gpu = prov[0] != "CPUExecutionProvider"
        opt = ort.SessionOptions()
        opt.log_severity_level = 3
        self.rvm = ort.InferenceSession(str(_download("rvm_mobilenetv3_fp32.onnx")), opt, providers=prov)
        self.u2 = ort.InferenceSession(str(_download("u2net_human_seg.onnx")), opt, providers=prov) if need_body else None
        self.rec = None
        print(f"  cut-out engine: {'GPU (' + prov[0].replace('ExecutionProvider', '') + ')' if self.gpu else 'CPU'}")

    def matte(self, img, ratio):
        """RVM alpha (0..1) - remembers the previous frames, which keeps the edges steady."""
        src = (img.astype(np.float32) / 255).transpose(2, 0, 1)[None]
        if self.rec is None:              # settle RVM's memory on the first frame, or the first second comes out messy
            self.rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4
            for _ in range(4):
                o = self.rvm.run(None, {"src": src, "r1i": self.rec[0], "r2i": self.rec[1], "r3i": self.rec[2],
                                        "r4i": self.rec[3], "downsample_ratio": np.array([ratio], np.float32)})
                self.rec = o[2:]
        o = self.rvm.run(None, {"src": src, "r1i": self.rec[0], "r2i": self.rec[1], "r3i": self.rec[2],
                                "r4i": self.rec[3], "downsample_ratio": np.array([ratio], np.float32)})
        self.rec = o[2:]
        return o[1][0, 0]

    def body(self, img):
        """U2-Net human (0..1): good at the jacket and shoulders, blind to the peanut head."""
        a = np.asarray(Image.fromarray(img).resize((320, 320), Image.BILINEAR)).astype(np.float32)
        a = a / max(float(a.max()), 1e-6)
        a = ((a - np.array([0.485, 0.456, 0.406], np.float32)) / np.array([0.229, 0.224, 0.225], np.float32))
        o = self.u2.run(None, {self.u2.get_inputs()[0].name: a.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
        o = (o - o.min()) / (o.max() - o.min() + 1e-6)
        return np.asarray(Image.fromarray((o * 255).astype(np.uint8)).resize((img.shape[1], img.shape[0]),
                                                                          Image.BILINEAR)).astype(np.float32) / 255


# ---------- following Peanut ----------
class Track:
    """A box around what's being kept; each frame keeps the shapes that overlap it, then moves to fit them."""

    def __init__(self, x, y, r):
        self.box = [x - r, y - r, x + r, y + r]

    def pick(self, lab):
        from scipy import ndimage  # noqa: F401
        x0, y0, x1, y1 = [int(v) for v in self.box]
        ids = set(np.unique(lab[max(0, y0):max(0, y1), max(0, x0):max(0, x1)])) - {0}
        keep = np.isin(lab, list(ids)) if ids else np.zeros(lab.shape, bool)
        if keep.any():
            ys, xs = np.nonzero(keep)
            nb = [xs.min(), ys.min(), xs.max() + 1, ys.max() + 1]
            pw, ph = (nb[2] - nb[0]) * 0.08 + 3, (nb[3] - nb[1]) * 0.08 + 3
            nb = [nb[0] - pw, nb[1] - ph, nb[2] + pw, nb[3] + ph]
            self.box = [0.6 * b + 0.4 * c for b, c in zip(nb, self.box)]
        else:                                        # lost him: widen the search until he's back
            self.box = [self.box[0] - 2, self.box[1] - 2, self.box[2] + 2, self.box[3] + 2]
        return keep


def _feats(img):
    f = img.astype(np.float32) + 1
    s = f.sum(-1, keepdims=True)
    return np.concatenate([f[..., :2] / s, s / 765.], -1)      # colour share + brightness


def _hull_fill(mask):
    from scipy.spatial import ConvexHull
    ys, xs = np.nonzero(mask)
    if len(xs) < 12:
        return mask
    pts = np.stack([xs, ys], 1)
    try:
        hull = pts[ConvexHull(pts).vertices]
    except Exception:  # noqa: BLE001
        return mask
    im = Image.new("L", (mask.shape[1], mask.shape[0]), 0)
    ImageDraw.Draw(im).polygon([tuple(map(float, p)) for p in hull], fill=1)
    return np.asarray(im) > 0


def _key_alpha(img, color, strength):
    """Colour key: how far each pixel's colour is from the key colour (chroma only, so shadows key out too)."""
    f = img.astype(np.float32)
    y = f @ np.array([0.299, 0.587, 0.114], np.float32)
    cb, cr = f[..., 2] - y, f[..., 0] - y
    kc = np.array(color, np.float32)
    ky = kc @ np.array([0.299, 0.587, 0.114], np.float32)
    d = np.hypot(cb - (kc[2] - ky), cr - (kc[0] - ky))
    lo = 20 + strength * 1.2
    return np.clip((d - lo) / 30.0, 0, 1)


class Cutter:
    def __init__(self, opts, size):
        from scipy import ndimage
        self.nd = ndimage
        self.o = opts
        self.w, self.h = size
        self.what = opts.get("what", "whole")
        self.method = opts.get("method", "follow")
        if self.what == "head" and self.method == "person":
            self.method = "follow"                       # head only needs to know which shape is Peanut
        self.engine = Engine(need_body=self.what == "whole") if self.method != "key" else None
        self.ratio = 0.4 if max(size) >= 1000 else 0.6
        self.edge, self.core = EDGES.get(opts.get("edges", "normal"), EDGES["normal"])
        cx, cy = opts.get("click") or (self.w / 2, self.h / 3)
        self.cx, self.cy = int(cx) // S, int(cy) // S
        self.body = Track(self.cx, self.cy, 12)
        self.head = Track(self.cx, self.cy, 8)
        self.model = None
        # [x0, y0, x1, y1, from, to]: seconds from the start of the cut (a banner can move when a Short zooms)
        self.leave = [[int(v) for v in b[:4]] + [float(b[4]) if len(b) > 4 else 0.0,
                                                  float(b[5]) if len(b) > 5 and b[5] is not None else 1e9]
                      for b in (opts.get("leave_out") or [])]
        self.key = opts.get("key_color") or None
        self.strength = float(opts.get("key_strength", 50))

    def _up(self, m):
        return np.kron(m.astype(np.float32), np.ones((S, S), np.float32))[:self.h, :self.w]

    def _alpha(self, soft, keep):
        nd = self.nd
        solid = nd.binary_fill_holes(keep)                        # nothing see-through inside his outline
        core = self._up(nd.binary_erosion(solid, iterations=2))
        m = nd.uniform_filter(self._up(nd.binary_dilation(keep | solid, iterations=2)), self.edge)
        return np.maximum(soft * m, nd.uniform_filter(core, self.core))

    def frame(self, img, t=0.0):
        """img (h, w, 3) uint8, t = seconds from the start of the cut -> alpha (h, w) float 0..1"""
        nd = self.nd
        boxes = [b[:4] for b in self.leave if b[4] - 0.02 <= t <= b[5]]
        sm = img[::S, ::S]
        if self.method == "key":
            if self.key is None:                                  # the most common colour along the edges
                edge = np.concatenate([img[0], img[-1], img[:, 0], img[:, -1]])
                q = (edge // 16).astype(np.int32)
                vals, cnt = np.unique(q[:, 0] * 256 + q[:, 1] * 16 + q[:, 2], return_counts=True)
                v = vals[cnt.argmax()]
                self.key = [int(v // 256) * 16 + 8, int(v // 16 % 16) * 16 + 8, int(v % 16) * 16 + 8]
                print(f"  key colour: rgb{tuple(self.key)}")
            head_soft = soft = _key_alpha(img, self.key, self.strength)
        else:
            head_soft = self.engine.matte(img, self.ratio)
            soft = head_soft
            if self.what == "whole":
                ub = self.engine.body(img)
                soft = np.maximum(head_soft, np.where(ub > 0.6, ub, 0))
        for x0, y0, x1, y1 in boxes:
            soft[max(0, y0):max(0, y1), max(0, x0):max(0, x1)] = 0
        small = soft[::S, ::S] > (0.5 if self.method == "key" else 0.22)
        if self.method == "person" or (self.method == "key" and self.what == "whole" and not self.o.get("click")):
            keep = small                                           # everything, no tracking
        else:
            keep = self.body.pick(nd.label(small)[0])
        if self.what == "head":
            F = _feats(sm)
            if self.model is None:
                r = 6
                y0, x0 = max(0, self.cy - r), max(0, self.cx - r)
                patch = F[y0:self.cy + r, x0:self.cx + r].reshape(-1, 3)
                pm = keep[y0:self.cy + r, x0:self.cx + r].reshape(-1)
                patch = patch[pm] if pm.sum() > 10 else patch
                self.model = (patch.mean(0), np.linalg.inv(np.cov(patch.T) + np.eye(3) * 1e-4))
            d = F - self.model[0]
            shell = (np.einsum("...i,ij,...j->...", d, self.model[1], d) < 16) & keep
            hk = self.head.pick(nd.label(nd.binary_closing(shell, iterations=2))[0])
            hk = nd.binary_fill_holes(_hull_fill(hk) & nd.binary_dilation(keep, iterations=1))
            a = self._alpha(head_soft, hk)
        else:
            a = self._alpha(soft, keep)
        for x0, y0, x1, y1 in boxes:
            a[max(0, y0):max(0, y1), max(0, x0):max(0, x1)] = 0
        return np.clip(a, 0, 1)


# ---------- the job ----------
def _out_folder(cfg):
    st = cfg["settings"]
    f = Path(st.get("export_folder") or (ROOT / "exports")) / "Cut-outs"
    f.mkdir(parents=True, exist_ok=True)
    return f


def _safe(s):
    return "".join(c if c.isalnum() or c in " -_()" else "_" for c in s).strip()[:60] or "cut-out"


def run(cfg, src, opts, preview=False):
    """Cut Peanut out of src between opts.start..opts.end. Preview = 3 s, green only, into data/cutout_preview.mp4."""
    src = Path(src)
    dur, sw, sh = probe(src)
    fps = _fps(src)
    a = max(0.0, float(opts.get("start") or 0))
    b = min(dur, float(opts.get("end") or dur))
    if preview:
        a = max(a, float(opts.get("at") or a))
        b = min(b, a + 3)
    if b - a < 0.2:
        raise SystemExit("[!] That part is too short to cut out.")
    k = min(1.0, MAX_SIDE / max(sw, sh))
    w, h = int(sw * k) // 2 * 2, int(sh * k) // 2 * 2
    sx, sy = w / sw, h / sh
    o = dict(opts)
    if o.get("click"):
        o["click"] = [o["click"][0] * sx, o["click"][1] * sy]
    base_t = float(opts.get("clip_start") or 0)        # box times are on the clip's clock; this run starts at a
    o["leave_out"] = [[b[0] * sx, b[1] * sy, b[2] * sx, b[3] * sy,
                       (b[4] if len(b) > 4 else 0) + base_t - a, (b[5] + base_t - a) if len(b) > 5 and b[5] is not None else None]
                      for b in (o.get("leave_out") or [])]
    progress(3, "Starting the cut-out engine")
    cut = Cutter(o, (w, h))
    total = max(1, int((b - a) * fps))
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-i", str(src), "-t", f"{b - a:.3f}",
                            "-vf", f"scale={w}:{h},fps={fps}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE, **_nowin())
    has_audio = bool(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                                     "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout.strip())
    aud = (["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(src), "-map", "0:v", "-map", "1:a"] if has_audio else []) + \
        (["-c:a", "aac", "-b:a", "192k"] if has_audio else [])
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H%M")
    what = "head" if o.get("what") == "head" else "Peanut"
    base = _out_folder(cfg) / f"{stamp} - {_safe(o.get('title') or src.stem)} - {what} cut-out"
    outs, encs = [], []
    raw = ["-f", "rawvideo", "-s", f"{w}x{h}", "-r", f"{fps}", "-i", "-"]
    if preview:
        prev = DATA / "cutout_preview.mp4"
        encs.append(("green", subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-pix_fmt", "rgb24"] + raw +
                     ["-map", "0:v", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                      "-movflags", "+faststart", str(prev)], stdin=subprocess.PIPE, **_nowin())))
        outs.append(prev)
    else:
        make = o.get("make") or ["mov", "green"]
        if "mov" in make:
            f = base.with_suffix(".mov")
            encs.append(("rgba", subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-pix_fmt", "rgba"] + raw + aud +
                         ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-vendor", "apl0", str(f)],
                         stdin=subprocess.PIPE, **_nowin())))
            outs.append(f)
        if "green" in make:
            f = base.with_name(base.name + " (green).mp4")
            encs.append(("green", subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-pix_fmt", "rgb24"] + raw + aud +
                         ["-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags",
                          "+faststart", str(f)], stdin=subprocess.PIPE, **_nowin())))
            outs.append(f)
        if "png" in make:
            d = base.with_name(base.name + " (PNG frames)")
            d.mkdir(exist_ok=True)
            encs.append(("rgba", subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-pix_fmt", "rgba"] + raw +
                         [str(d / "frame_%05d.png")], stdin=subprocess.PIPE, **_nowin())))
            outs.append(d)
        if not encs:
            raise SystemExit("[!] Pick at least one thing to make.")
    green = np.zeros((h, w, 3), np.float32)
    green[..., 1] = 255
    n, t0, last = 0, time.time(), 0.0
    try:
        while True:
            buf = dec.stdout.read(w * h * 3)
            if len(buf) < w * h * 3:
                break
            img = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
            al = cut.frame(img, n / fps)
            for kind, p in encs:
                if kind == "rgba":
                    p.stdin.write(np.dstack([img, (al * 255).astype(np.uint8)]).tobytes())
                else:
                    p.stdin.write((img * al[..., None] + green * (1 - al[..., None])).astype(np.uint8).tobytes())
            n += 1
            if time.time() - last > 1:
                last = time.time()
                per = (time.time() - t0) / n
                left = per * (total - n)
                progress(5 + 93 * n / total, f"Cutting out Peanut: frame {n} of {total}"
                         + (f", about {int(left // 60)} min {int(left % 60)} s left" if left >= 60 else
                            f", about {int(left)} s left" if n > 5 else ""))
    finally:
        for _, p in encs:
            try:
                p.stdin.close()
            except OSError:
                pass
            p.wait()
        dec.stdout.close()
        dec.wait()
    if not n:
        raise SystemExit("[!] Couldn't read any frames from that video.")
    print(f"  {n} frames, {(time.time() - t0) / n:.2f} s per frame")
    for f in outs:
        print(f"  saved: {f}")
    json.dump({"outs": [str(f) for f in outs], "preview": preview, "at": time.time()},
              open(DATA / "last_cutout.json", "w"))
    progress(100, "Preview ready" if preview else f"Cut-out ready: {len(outs)} file{'s' if len(outs) != 1 else ''} in Exports\\Cut-outs")
    return outs


def resolve(cfg, spec):
    """Where a cut-out's video comes from -> (file, start, end, title).
    short: a Review/Approved Short, from the Short itself or from its stream (16:9, no banners);
    part: a part in the Compilations editor; upload: a video dropped on the Cut-out tab."""
    from .util import load_json
    t = spec.get("type")
    if t == "short":
        job = Path(cfg["paths"]["output_dir"]) / Path(str(spec["job"])).name
        data = load_json(job / "clips.json") or {}
        c = next((x for x in data.get("clips", []) if x.get("id") == spec.get("id")), None)
        if not c:
            raise SystemExit("[!] That Short isn't there any more.")
        if spec.get("from") == "stream":
            f = Path(c.get("source_file") or "")
            if not f.is_file():
                raise SystemExit("[!] The stream this Short came from was already cleaned up. Use the Short itself.")
            return f, float(c.get("src_start") or 0), float(c.get("src_end") or 0) or None, c.get("title", "")
        return job / c["file"], None, None, c.get("title", "")
    if t == "part":
        from .compile import get, _path
        c = get(str(spec["comp"]))
        m = next((x for x in c["moments"] if x["mid"] == spec.get("mid")), None)
        if not m:
            raise SystemExit("[!] That part isn't in the compilation any more.")
        return _path(c["id"]).parent / m["file"], float(m["a"]), float(m["b"]), m.get("title", "")
    if t == "upload":
        f = UPLOADS / Path(str(spec["name"])).name
        if not f.is_file():
            raise SystemExit("[!] That video isn't there any more - drop it in again.")
        return f, None, None, f.stem
    raise SystemExit("[!] Nothing picked to cut out.")


UPLOADS = ROOT / "work" / "_cutout_in"


def job(cfg, jobfile, preview=False):
    """`python -m clipper roto <jobfile> [--preview]` (the page writes the job file: {spec, opts})."""
    j = json.loads(Path(jobfile).read_text(encoding="utf-8"))
    f, a, b, title = resolve(cfg, j["spec"])
    opts = dict(j.get("opts") or {})
    opts["clip_start"] = a or 0.0
    if a is not None:                     # times on the page are inside the clip; the file may be the whole stream
        opts["start"] = a + float(opts.get("start") or 0)
        opts["end"] = min(b if b else 1e9, a + float(opts["end"])) if opts.get("end") else b
        if opts.get("at") is not None:
            opts["at"] = a + float(opts["at"])
    opts.setdefault("title", title)
    return run(cfg, f, opts, preview)


def _fps(src):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=avg_frame_rate",
                        "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout.strip()
    try:
        a, b = r.split("/")
        f = float(a) / float(b)
    except (ValueError, ZeroDivisionError):
        f = 30.0
    return round(min(60.0, max(10.0, f)), 3)


def _nowin():
    return {"creationflags": subprocess.CREATE_NO_WINDOW} if sys.platform == "win32" else {}
