"""Title + description for each Short. Uses Claude if ANTHROPIC_API_KEY is set."""
import os
import re


def _claude_title(text, hint, cfg):
    import anthropic
    t = cfg["titles"]
    examples = "\n".join(f"- {e}" for e in t.get("examples", []))
    prompt = (
        f"You title YouTube Shorts for a fan clip channel of the streamer {cfg['streamer']['name']} "
        f"(an animated peanut, plays ARC Raiders / Rust / Tarkov).\n"
        f"These titles performed best on the channel:\n{examples}\n\n"
        f"Write ONE title for this clip in the same style: ALL CAPS, under 60 characters, says what "
        f"happens or the funniest line, names any famous person involved, no hashtags, no quotes, no emojis.\n"
        + (f"Context: {hint}\n" if hint else "")
        + f"Transcript:\n{text[:2500]}\n\nTitle:")
    client = anthropic.Anthropic()
    msg = client.messages.create(model=t["model"], max_tokens=60,
                                 messages=[{"role": "user", "content": prompt}])
    title = msg.content[0].text.strip().splitlines()[0].strip().strip('"')
    return title[:95]


def _template_title(text, tags, hint):
    if hint:
        base = hint.upper()
        return base if "PEANUT" in base else f"PEANUT: {base}"[:95]
    words = re.sub(r"\s+", " ", text).strip().split(" ")
    snippet = " ".join(words[-9:]).upper().strip(" ,.") if words and words[0] else "WHAT JUST HAPPENED"
    if tags:
        return f"PEANUT X {tags[0].upper()}: {snippet}"[:95]
    return f"PEANUT: {snippet}"[:95]


def make_title(text, tags=None, hint="", cfg=None):
    tags = tags or []
    mode = str(cfg["titles"].get("use_claude", "auto")).lower()
    if mode in ("auto", "true", "yes") and os.environ.get("ANTHROPIC_API_KEY") and text.strip():
        try:
            return _claude_title(text, hint, cfg)
        except Exception as e:  # noqa: BLE001
            print(f"  [!] Claude title failed ({e}); using template")
    return _template_title(text, tags, hint)


def make_description(title, cfg, source_url=""):
    s = cfg["streamer"]
    lines = [title, "", s["credit_line"]]
    if source_url:
        lines.append(f"Full stream: {source_url}")
    lines += ["", " ".join(s["hashtags"])]
    return "\n".join(lines)
