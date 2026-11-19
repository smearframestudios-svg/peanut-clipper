"""Big bold word-by-word captions (.ass) - the spoken word lights up yellow."""
import re


def _t(sec):
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int(sec % 3600 // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def _clean(word):
    w = re.sub(r"[{}\\]", "", word).strip()
    return w.upper()


def build_ass(words, clip_start, clip_end, cfg, y, width=1080, height=1920):
    c = cfg["captions"]
    col, hl = c["color"], c["highlight"]
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,{c['font']},{c['size']},{col},{col},&H00000000,&H96000000,-1,0,0,0,100,100,1,0,1,{c['outline']},3,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ws = [dict(w, w=_clean(w["w"])) for w in words if clip_start <= w["s"] < clip_end and _clean(w["w"])]
    # group into short lines; break on pauses
    chunks, cur = [], []
    per = int(c["words_per_line"])
    for w in ws:
        if cur and (len(cur) >= per or w["s"] - cur[-1]["e"] > 0.6):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)

    lines = []
    for ci, ch in enumerate(chunks):
        next_start = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else clip_end
        for i, w in enumerate(ch):
            s = w["s"]
            e = ch[i + 1]["s"] if i + 1 < len(ch) else min(w["e"] + 0.35, next_start)
            if e <= s:
                e = s + 0.08
            parts = [("{\\c" + hl + "}" + x["w"] + "{\\c" + col + "}") if j == i else x["w"]
                     for j, x in enumerate(ch)]
            pop = "{\\fscx112\\fscy112\\t(0,90,\\fscx100\\fscy100)}" if i == 0 else ""
            lines.append(f"Dialogue: 0,{_t(s - clip_start)},{_t(e - clip_start)},Main,,0,0,0,,"
                         f"{{\\pos({width // 2},{int(y)})}}{pop}{' '.join(parts)}")
    return header + "\n".join(lines) + "\n", len(chunks)
