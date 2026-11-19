"""Reads chat replays into [(seconds, text)]. Supports:
- YouTube live chat from yt-dlp (*.live_chat.json, one JSON object per line)
- TwitchDownloaderCLI chat JSON ({"comments": [...]})
- plain CSV/TXT lines "seconds,message"
"""
import json
from pathlib import Path


def _yt_runs(runs):
    out = []
    for r in runs:
        if "text" in r:
            out.append(r["text"])
        elif "emoji" in r:
            e = r["emoji"]
            eid = e.get("emojiId", "")
            out.append(eid if len(eid) <= 4 else (e.get("shortcuts") or [""])[0])
    return "".join(out)


def _parse_youtube_line(obj):
    rep = obj.get("replayChatItemAction")
    if not rep:
        return None
    t = float(rep.get("videoOffsetTimeMsec", 0)) / 1000.0
    for act in rep.get("actions", []):
        item = act.get("addChatItemAction", {}).get("item", {})
        for kind in ("liveChatTextMessageRenderer", "liveChatPaidMessageRenderer"):
            if kind in item:
                return t, _yt_runs(item[kind].get("message", {}).get("runs", []))
    return None


def load_chat(path, offset=0.0, duration=None):
    path = Path(path)
    text = path.read_text(encoding="utf-8", errors="ignore")
    msgs = []
    stripped = text.lstrip()
    if stripped.startswith("{") and '"comments"' in stripped[:5000]:
        data = json.loads(text)
        for c in data.get("comments", []):
            body = (c.get("message") or {}).get("body", "")
            msgs.append((float(c.get("content_offset_seconds", 0)), body))
    elif stripped.startswith("{"):
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                got = _parse_youtube_line(json.loads(line))
            except json.JSONDecodeError:
                continue
            if got:
                msgs.append(got)
    else:
        for line in text.splitlines():
            sec, _, msg = line.partition(",")
            try:
                msgs.append((float(sec), msg))
            except ValueError:
                pass
    out = []
    for t, m in msgs:
        t -= offset
        if t >= 0 and (duration is None or t < duration):
            out.append((t, m))
    out.sort()
    return out
