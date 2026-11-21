"""Title cards: big outlined thumbnail-style text as a transparent 1080x1920 PNG, for the top of a Short.

A card is a list of lines. Each line: text, color (white / yellow / red), size (S / M / L) and an extra
(none / swoosh / box). Consecutive "box" lines share one red box. Card options: a rough red brush behind the
top lines, slant, line spacing, and where it sits (top / middle / bottom, kept clear of YouTube's buttons).
"""
import io
import math
import random
import re
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = Path(__file__).parent / "fonts" / "BarlowCondensed-BlackItalic.ttf"
COLORS = ("white", "yellow", "red")
SIZES = {"S": 0.66, "M": 0.84, "L": 1.0}
EXTRAS = ("none", "swoosh", "box")
FILLS = {"white": [(255, 255, 255), (236, 236, 236)], "yellow": [(255, 245, 20), (255, 196, 0)],
         "red": [(255, 40, 30), (200, 0, 0)]}
RED = (232, 20, 20, 255)
STRETCH = 0.82          # letters a little narrower (taller lines), like the reference cards


@lru_cache(maxsize=64)
def _font(size):
    return ImageFont.truetype(str(FONT), size)


def _grad(w, h, top, bot):
    col = Image.new("RGB", (1, 256))
    for y in range(256):
        t = y / 255
        col.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return col.resize((max(1, w), max(1, h)))


def _masks(text, f):
    """Fill / black outline / red inner outline masks for one line, letters placed one by one."""
    font = _font(f)
    so, si, sb = max(4, int(f * 0.11)), max(2, int(f * 0.06)), max(1, int(f * 0.01))
    track = -f * 0.005
    asc, desc = font.getmetrics()
    pad = so + 10
    widths = [font.getlength(ch) for ch in text]
    tw = int(sum(w * 0.45 if ch == " " else w for ch, w in zip(text, widths)) + track * max(0, len(text) - 1)) + 2 * pad
    th = asc + desc + 2 * pad
    m = {k: Image.new("L", (max(1, tw), th)) for k in ("fill", "out", "inn")}
    d = {k: ImageDraw.Draw(v) for k, v in m.items()}
    x = pad
    for ch, w in zip(text, widths):
        if ch != " ":
            d["out"].text((x, pad), ch, font=font, fill=255, stroke_width=so, stroke_fill=255)
            d["inn"].text((x, pad), ch, font=font, fill=255, stroke_width=si, stroke_fill=255)
            d["fill"].text((x, pad), ch, font=font, fill=255, stroke_width=sb, stroke_fill=255)
        x += (w * 0.45 if ch == " " else w) + track
    bb = m["out"].getbbox() or (0, 0, 1, 1)
    m = {k: v.crop(bb) for k, v in m.items()}
    nw = max(1, int(m["out"].width * STRETCH))
    return {k: v.resize((nw, v.height)) for k, v in m.items()}, so


def clean(spec):
    """Make a card spec safe to render (whatever the page sent)."""
    lines = []
    for ln in (spec.get("lines") or [])[:8]:
        text = re.sub(r"\s+", " ", str(ln.get("text", ""))).strip().upper()[:40]
        if not text:
            continue
        lines.append({"text": text, "color": ln.get("color") if ln.get("color") in COLORS else "white",
                      "size": ln.get("size") if ln.get("size") in SIZES else "L",
                      "extra": ln.get("extra") if ln.get("extra") in EXTRAS else "none"})
    def num(k, lo, hi, d):
        try:
            return min(hi, max(lo, float(spec.get(k, d))))
        except (TypeError, ValueError):
            return d
    return {"lines": lines, "brush": bool(spec.get("brush")), "slant": num("slant", 0.0, 0.2, 0.05),
            "gap": num("gap", -0.25, 0.2, -0.10), "position": spec.get("position") if spec.get("position") in ("top", "middle", "bottom") else "middle",
            "seed": int(num("seed", 0, 10 ** 6, 3))}


def render(spec, scale=1.0):
    """The card as a transparent RGBA image, 1080x1920 at scale 1 (smaller for quick previews)."""
    spec = clean(spec)
    W, H = int(1080 * scale), int(1920 * scale)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if not spec["lines"]:
        return out
    rnd = random.Random(spec["seed"])
    k = scale
    target = W - int(120 * k)
    rows = []
    for ln in spec["lines"]:
        f = int(200 * k)
        for _ in range(3):                                         # size that fills the width for this line
            ms, so = _masks(ln["text"], f)
            f = max(int(24 * k), int(f * target * SIZES[ln["size"]] / max(1, ms["out"].width)))
        ms, so = _masks(ln["text"], f)
        rows.append(dict(ln, m=ms, so=so, f=f))
    sw_gap = lambda r: int(r["f"] * 0.50) if r["extra"] == "swoosh" else 0  # noqa: E731
    total = sum(r["m"]["out"].height + sw_gap(r) for r in rows) + sum(int(r["f"] * spec["gap"]) for r in rows[1:])
    card = Image.new("RGBA", (W, max(H, total + int(200 * k))), (0, 0, 0, 0))
    y = (card.height - total) // 2
    placed = []
    for r in rows:
        placed.append((r, (W - r["m"]["out"].width) // 2, y))
        y += r["m"]["out"].height + sw_gap(r) + int(r["f"] * spec["gap"])
    under = Image.new("RGBA", card.size, (0, 0, 0, 0))
    ud = ImageDraw.Draw(under)
    if spec["brush"]:                                              # rough red brush behind the top lines
        free = [p for p in placed if p[0]["extra"] != "box"][:2] or placed[:2]
        top, bot = free[0][2] - 50 * k, free[-1][2] + free[-1][0]["m"]["out"].height + 30 * k
        lx = min(x for _, x, _ in free) - 40 * k
        rx = max(x + r["m"]["out"].width for r, x, _ in free) + 40 * k
        pts = [(lx + i * (rx - lx) / 50, top + rnd.uniform(-55, 20) * k - 30 * k * (1 - i / 50)) for i in range(51)]
        pts += [(rx + rnd.uniform(-25, 30) * k, top + i * (bot - top) / 40) for i in range(41)]
        pts += [(rx - i * (rx - lx) / 50, bot + rnd.uniform(-20, 45) * k) for i in range(51)]
        pts += [(lx + rnd.uniform(-35, 20) * k, bot - i * (bot - top) / 40) for i in range(41)]
        ud.polygon(pts, fill=RED)
        for _ in range(220):                                       # dry-brush streaks
            side = rnd.random()
            if side < .5:
                x0, y0 = rnd.uniform(lx - 40 * k, lx + (rx - lx) * .6), top + rnd.uniform(-70, 30) * k
            elif side < .8:
                x0, y0 = rx + rnd.uniform(-30, 40) * k, rnd.uniform(top, bot)
            else:
                x0, y0 = lx + rnd.uniform(-40, 10) * k, rnd.uniform(top, bot)
            ln_ = rnd.uniform(30, 120) * k
            ud.line([(x0, y0), (x0 + ln_, y0 - ln_ * .25 + rnd.uniform(-6, 6) * k)], fill=RED, width=max(1, int(rnd.randint(2, 7) * k)))
    groups, cur = [], []
    for p in placed:                                               # consecutive "box" lines share one red box
        if p[0]["extra"] == "box":
            cur.append(p)
        elif cur:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    for g in groups:
        x0 = min(x for _, x, _ in g) - 10 * k
        x1 = max(x + r["m"]["out"].width for r, x, _ in g) + 10 * k
        y0, y1 = g[0][2] - 8 * k, g[-1][2] + g[-1][0]["m"]["out"].height + 6 * k
        e = 14 * k
        ud.rounded_rectangle([x0 - e, y0 - e, x1 + e, y1 + e], int(18 * k), fill=(0, 0, 0, 255))
        ud.rounded_rectangle([x0, y0, x1, y1], int(10 * k), fill=RED)
    card.alpha_composite(under)
    for r, x, yy in placed:
        ms, mo = r["m"], r["m"]["out"]
        sh = Image.new("RGBA", mo.size, (0, 0, 0, 255))
        sh.putalpha(mo.filter(ImageFilter.GaussianBlur(max(1, 6 * k))).point(lambda v: int(v * 0.6)))
        card.alpha_composite(sh, (x + int(r["f"] * 0.03), yy + int(r["f"] * 0.05)))
        blk = Image.new("RGBA", mo.size, (0, 0, 0, 255))
        blk.putalpha(mo)
        card.alpha_composite(blk, (x, yy))
        if r["color"] == "yellow":                                 # red edge inside the black one
            rd = Image.new("RGBA", mo.size, (225, 15, 15, 255))
            rd.putalpha(ms["inn"])
            card.alpha_composite(rd, (x, yy))
        fl = _grad(mo.width, mo.height, *FILLS[r["color"]]).convert("RGBA")
        fl.putalpha(ms["fill"])
        card.alpha_composite(fl, (x, yy))
    for r, x, yy in placed:                                        # swooshes on top, so the next line can't hide them
        if r["extra"] != "swoosh":
            continue
        mo = r["m"]["out"]
        sw = Image.new("RGBA", card.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(sw)
        ys = yy + mo.height + int(r["f"] * 0.20)
        xa, xb = x - mo.width * 0.03, x + mo.width * 1.03
        for col, extra in (((0, 0, 0, 255), r["so"] * 2), (RED, 0)):
            top_, bot_ = [], []
            for i in range(61):
                t = i / 60
                xx = xa + (xb - xa) * t
                curve = -math.sin(math.pi * t) * r["f"] * 0.06
                thick = (r["f"] * 0.26) * (0.12 + 0.88 * max(0.0, math.sin(math.pi * min(1, t * 1.08))) ** 0.7) + extra
                top_.append((xx, ys + curve - thick / 2))
                bot_.append((xx, ys + curve + thick / 2))
            sd.polygon(top_ + bot_[::-1], fill=col)
        card.alpha_composite(sw)
    s = spec["slant"]                                              # slant, then fit into the frame
    card = card.transform(card.size, Image.AFFINE, (1, s, -s * card.height / 2, 0, 1, 0), resample=Image.BICUBIC)
    bb = card.getbbox()
    if not bb:
        return out
    card = card.crop(bb)
    top_lim, bot_lim = {"top": (300 * k, H * 0.62), "middle": (40 * k, H - 40 * k),
                        "bottom": (H * 0.38, H - 480 * k)}[spec["position"]]
    fit = min((W - 30 * k) / card.width, (bot_lim - top_lim) / card.height, 1.0)
    card = card.resize((max(1, int(card.width * fit)), max(1, int(card.height * fit))), Image.LANCZOS)
    cy = {"top": top_lim, "middle": (H - card.height) / 2, "bottom": bot_lim - card.height}[spec["position"]]
    out.alpha_composite(card, ((W - card.width) // 2, int(cy)))
    return out


def png_bytes(spec, scale=1.0):
    buf = io.BytesIO()
    render(spec, scale).save(buf, "PNG", optimize=scale >= 1)
    return buf.getvalue()


# ------------------------------------------------------------------ a first draft from a Short's title
LOUD = {"NOT", "NEVER", "WORST", "BEST", "GTA", "GTA 6", "MILLION", "INSANE", "STOLE", "STOLEN", "WRONG", "PAY",
        "FREE", "CRASH", "CRASHED", "COPS", "POLICE", "WASTED", "HOURS", "MONEY", "BROKE", "FIRED", "BANNED", "FAST",
        "FURIOUS", "STUCK", "LOST", "CAUGHT", "RAGE", "WON", "LOSES", "LOST", "BIGGEST", "FIRST", "LAST"}


def _split(title):
    words = re.sub(r"\s+", " ", re.sub(r"[#\"]", "", title)).strip().upper().split(" ")
    out, cur = [], ""
    for w in words:
        if w == "6" and cur.endswith("GTA"):                       # keep "GTA 6" together
            cur += " 6"
            continue
        if cur and len(cur) + 1 + len(w) > 11:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    while len(out) > 6:                                            # too many lines: merge the shortest neighbours
        i = min(range(len(out) - 1), key=lambda j: len(out[j]) + len(out[j + 1]))
        out[i:i + 2] = [out[i] + " " + out[i + 1]]
    return out


def from_title(title, variant=0, texts=None):
    """A first draft of a card from a title (variant = Shuffle styles). texts = keep these lines, restyle only."""
    rnd = random.Random(variant)
    texts = [re.sub(r"\s+", " ", t).strip().upper()[:40] for t in (texts or []) if str(t).strip()][:8] or \
        _split(title or "") or ["PEANUT"]
    lines = []
    for i, t in enumerate(texts):
        loud = any(w in LOUD for w in t.split()) or "GTA" in t or bool(re.search(r"\d", t))
        color = "yellow" if loud else "white"
        if i == len(texts) - 1 and re.search(r"[!?]$", t):
            color = rnd.choice(["red", "yellow"]) if variant else "red"
        size = "L" if len(t) <= 8 or loud else ("M" if len(t) <= 12 else "S")
        lines.append({"text": t, "color": color, "size": size, "extra": "none"})
    if variant:
        for ln in lines:                                           # shuffle a few colours around
            if rnd.random() < .3:
                ln["color"] = rnd.choice(COLORS)
    yellows = [i for i, ln in enumerate(lines) if ln["color"] == "yellow"]
    style = variant % 3
    if style == 0 and yellows:
        lines[yellows[0]]["extra"] = "swoosh"
    elif style == 1 and len(lines) >= 3:
        for ln in lines[-2:]:
            ln["extra"] = "box"
            ln["color"] = "yellow"
    elif style == 2 and yellows:
        lines[yellows[-1]]["extra"] = "swoosh"
    return {"lines": lines, "brush": style == 1, "slant": 0.05, "gap": -0.10, "position": "middle", "seed": variant + 3}
