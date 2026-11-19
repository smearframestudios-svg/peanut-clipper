"""Finds clip-worthy moments.

Pass 1 (whole stream, cheap): chat speed, hype words, loudness, names/topics typed in chat.
Pass 2 (top candidates only): names/topics actually SAID on stream, and snapping the cut
to sentence boundaries so clips don't start mid-word.
"""
import re
from collections import defaultdict

import numpy as np

from .util import compile_terms


def smooth(x, k):
    if k <= 1 or len(x) == 0:
        return x
    return np.convolve(x, np.ones(k) / k, mode="same")


def rolling_z(x, win=600):
    """z-score of each second vs. the surrounding ~10 minutes (streams get busier over time)."""
    n = len(x)
    if n == 0:
        return x
    c = np.concatenate([[0.0], np.cumsum(x)])
    c2 = np.concatenate([[0.0], np.cumsum(x * x)])
    idx = np.arange(n)
    lo = np.clip(idx - win // 2, 0, n)
    hi = np.clip(idx + win // 2 + 1, 0, n)
    cnt = hi - lo
    mean = (c[hi] - c[lo]) / cnt
    var = np.maximum((c2[hi] - c2[lo]) / cnt - mean ** 2, 0)
    return (x - mean) / (np.sqrt(var) + 1e-3)


def shift_earlier(x, sec):
    if sec <= 0:
        return x
    return np.concatenate([x[sec:], np.zeros(min(sec, len(x)))])


class Detector:
    def __init__(self, cfg):
        self.cfg = cfg
        d = cfg["detect"]
        self.d = d
        self.w = d["weights"]
        self.names = compile_terms(cfg.get("names"))
        self.topics = compile_terms(cfg.get("topics"))
        toks = [t for t in cfg.get("hype_tokens", []) if t.strip()]
        self.hype_re = re.compile("|".join(re.escape(t.strip()) for t in toks), re.I) if toks else None

    # ---------- pass 1 ----------
    def candidates(self, n, chat, loud, t0=0, t1=None):
        d, w = self.d, self.w
        delay = int(d["chat_delay_sec"])
        rate = np.zeros(n)
        hype = np.zeros(n)
        mentions = defaultdict(lambda: np.zeros(n))
        kinds = {}
        for t, text in chat:
            s = int(t)
            if not 0 <= s < n:
                continue
            rate[s] += 1
            if self.hype_re and self.hype_re.search(text):
                hype[s] += 1
            for kind, terms in (("names", self.names), ("topics", self.topics)):
                for label, rx, _ in terms:
                    if rx.search(text):
                        mentions[label][s] += 1
                        kinds[label] = kind

        have_chat = rate.sum() > 0
        score = np.zeros(n)
        rate_s = smooth(rate, 5)
        if have_chat:
            score += w["chat"] * np.clip(shift_earlier(rolling_z(rate_s), delay), 0, None)
            score += w["hype"] * np.clip(shift_earlier(rolling_z(smooth(hype, 5)), delay), 0, None)
        loud = np.asarray(loud[:n], dtype=float)
        if len(loud) < n:
            loud = np.concatenate([loud, np.full(n - len(loud), loud.min() if len(loud) else -60)])
        za = rolling_z(smooth(loud, 3))
        score += w["audio"] * (1.0 if have_chat else 2.0) * np.clip(za, 0, None)

        mention_s = {}
        weights = {label: wt for terms in (self.names, self.topics) for label, _, wt in terms}
        for label, arr in mentions.items():
            m = shift_earlier(smooth(arr, 15) * 15, delay)  # mentions within ~15s
            mention_s[label] = m
            score += w[kinds[label]] * weights[label] * 0.35 * np.minimum(m, 4) / 4

        lo = int(t0 or 0)
        hi = int(t1) if t1 else n
        score[:lo] = 0
        score[hi:] = 0

        picks = []
        spacing = int(d["spacing_sec"])
        for p in np.argsort(-score):
            if score[p] <= 0.5 or len(picks) >= int(d["candidates"]):
                break
            if all(abs(int(p) - q) >= spacing for q in picks):
                picks.append(int(p))

        base_rate = max(float(np.mean(rate_s)), 0.05) if have_chat else 1
        out = []
        for p in picks:
            end = min(n, p + int(d["tail_sec"]))
            start = max(0, end - int(d["clip_len_sec"]))
            reasons = []
            if have_chat:
                peak_rate = float(rate_s[min(n - 1, p + delay)])
                ratio = peak_rate / base_rate
                if ratio >= 1.5:
                    reasons.append(f"chat {ratio:.1f}x faster than normal")
                hy = float(smooth(hype, 5)[min(n - 1, p + delay)] * 5)
                if hy >= 3:
                    reasons.append(f"{int(hy)} laughing/hype msgs")
            if za[p] > 2:
                reasons.append("loud moment")
            for label, m in mention_s.items():
                if m[p] >= 2:
                    reasons.append(f"chat says '{label}'")
            out.append({"peak": p, "start": float(start), "end": float(end),
                        "score": round(float(score[p]), 2), "reasons": reasons})
        return out

    # ---------- pass 2 ----------
    def refine(self, cand, tr):
        d, w = self.d, self.w
        start, end = cand["start"], cand["end"]
        segs = tr.get("segments", [])
        if segs:
            # start at the beginning of the sentence we land in (pull back up to 10s for setup)
            for s in segs:
                if s["s"] <= start + 1.5 and s["e"] > start:
                    if start - s["s"] <= 10:
                        start = s["s"]
                    break
            # end at the end of the sentence that contains the punchline (up to +5s)
            for s in segs:
                if s["s"] < end <= s["e"] + 0.01 or (s["s"] < end and s["e"] > end):
                    if s["e"] - end <= 5:
                        end = s["e"] + 0.4
                    break
        length = end - start
        if length > d["max_len_sec"]:
            start = end - d["max_len_sec"]
        if length < d["min_len_sec"]:
            start = max(0.0, end - d["min_len_sec"])
        text = " ".join(x["w"] for x in tr.get("words", []) if start <= x["s"] < end)
        score = cand["score"]
        reasons = list(cand["reasons"])
        tags = []
        for kind, terms in (("names", self.names), ("topics", self.topics)):
            for label, rx, wt in terms:
                if rx.search(text):
                    score += w[kind] * wt
                    reasons.append(f"says '{label}'")
                    tags.append(label)
        cand.update(start=round(start, 2), end=round(end, 2), score=round(score, 2),
                    reasons=reasons, text=text, tags=tags)
        return cand
