"""Most-viewed Twitch clips of the streamer (viewers already found the best moments)."""
import datetime as dt
import os
import sys

import requests


def _creds(cfg):
    st = cfg.get("settings", {})
    cid = st.get("twitch_client_id") or os.environ.get("TWITCH_CLIENT_ID") or cfg["twitch"].get("client_id")
    sec = st.get("twitch_client_secret") or os.environ.get("TWITCH_CLIENT_SECRET") or cfg["twitch"].get("client_secret")
    if not cid or not sec:
        sys.exit("\n[!] Add your Twitch Client ID and Secret on the Settings screen first.\n")
    return cid, sec


def top_clips(cfg, hours=24, limit=30):
    cid, sec = _creds(cfg)
    tok = requests.post("https://id.twitch.tv/oauth2/token", timeout=30, params={
        "client_id": cid, "client_secret": sec, "grant_type": "client_credentials"}).json()["access_token"]
    h = {"Client-Id": cid, "Authorization": f"Bearer {tok}"}
    login = cfg["streamer"]["twitch_login"]
    users = requests.get("https://api.twitch.tv/helix/users", headers=h, params={"login": login}, timeout=30).json()
    if not users.get("data"):
        sys.exit(f"[!] Twitch user '{login}' not found")
    bid = users["data"][0]["id"]
    now = dt.datetime.now(dt.timezone.utc)
    params = {"broadcaster_id": bid, "first": min(100, max(1, limit)),
              "started_at": (now - dt.timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "ended_at": now.strftime("%Y-%m-%dT%H:%M:%SZ")}
    data = requests.get("https://api.twitch.tv/helix/clips", headers=h, params=params, timeout=30).json()
    clips = data.get("data", [])
    clips.sort(key=lambda c: -c.get("view_count", 0))
    return clips
