"""Uploads approved Shorts to YouTube, scheduled into your daily posting slots."""
import datetime as dt
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from .library import after_upload
from .util import DATA, load_json, save_json

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def _service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    secret = DATA / "client_secret.json"
    token = DATA / "token.json"
    if not secret.exists():
        sys.exit("\n[!] YouTube isn't connected yet - add your client_secret.json on the Upload screen.\n")
    creds = Credentials.from_authorized_user_file(str(token), SCOPES) if token.exists() else None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("A browser window will open. Pick the BurntPeanutXD channel when Google asks.")
            creds = InstalledAppFlow.from_client_secrets_file(str(secret), SCOPES).run_local_server(port=0)
        token.write_text(creds.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=creds)


def _slots(cfg, count, taken):
    up = cfg["upload"]
    tz = ZoneInfo(up["timezone"])
    now = dt.datetime.now(tz) + dt.timedelta(minutes=45)
    times = sorted(dt.time.fromisoformat(t) for t in up["schedule_times"])
    out, day = [], now.date()
    while len(out) < count:
        for t in times:
            when = dt.datetime.combine(day, t, tz)
            if when > now and when.isoformat() not in taken:
                out.append(when)
                if len(out) == count:
                    break
        day += dt.timedelta(days=1)
    return out


def approved_clips(cfg):
    for f in sorted(Path(cfg["paths"]["output_dir"]).glob("*/clips.json")):
        data = load_json(f)
        for c in data["clips"]:
            if c["status"] == "approved" and not c.get("youtube_id"):
                yield f, data, c


def plan(cfg):
    """[(title, when_iso)] for the Upload screen."""
    todo = list(approved_clips(cfg))
    taken = set(load_json(cfg["paths"]["work_dir"] / "schedule.json", []))
    slots = _slots(cfg, len(todo), taken) if cfg["upload"].get("schedule") else [None] * len(todo)
    return [{"title": c["title"], "when": w.strftime("%a %b %d, %I:%M %p") if w else "right away",
             "job": p.parent.name, "id": c["id"], "length": c.get("length"),
             "poster": f"/media/{p.parent.name}/{c['poster']}"} for (p, _, c), w in zip(todo, slots)]


def upload_approved(cfg, dry_run=False):
    todo = list(approved_clips(cfg))
    if not todo:
        print("Nothing approved and waiting. Approve clips on the review page first.")
        return
    up = cfg["upload"]
    sched_path = cfg["paths"]["work_dir"] / "schedule.json"
    taken = set(load_json(sched_path, []))
    slots = _slots(cfg, len(todo), taken) if up.get("schedule") else [None] * len(todo)
    if dry_run:
        for (_, _, c), when in zip(todo, slots):
            print(f"  would upload  {c['title'][:60]:<60}  {when:%a %b %d %I:%M %p}" if when else c["title"])
        return

    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
    yt = _service()
    for (path, data, c), when in zip(todo, slots):
        status = {"privacyStatus": up["privacy"], "selfDeclaredMadeForKids": bool(up["made_for_kids"])}
        if when:
            status["privacyStatus"] = "private"
            status["publishAt"] = when.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        body = {"snippet": {"title": c["title"][:100], "description": c["description"][:4900],
                            "tags": [t.lstrip("#") for t in cfg["streamer"]["hashtags"]],
                            "categoryId": str(up["category_id"])}, "status": status}
        media = MediaFileUpload(str(path.parent / c["file"]), mimetype="video/mp4", chunksize=-1, resumable=True)
        try:
            req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
            resp = None
            while resp is None:
                _, resp = req.next_chunk()
        except HttpError as e:
            if "quota" in str(e).lower():
                print("\n[!] YouTube's daily upload limit for this app was hit. Run upload again tomorrow.")
                return
            raise
        c["youtube_id"] = resp["id"]
        c["status"] = "uploaded"
        c["publish_at"] = when.isoformat() if when else "now"
        after_upload(cfg, path, data, c)
        if when:
            taken.add(when.isoformat())
            save_json(sched_path, sorted(taken))
        print(f"@@ {int(100 * (todo.index((path, data, c)) + 1) / len(todo))} Uploaded {todo.index((path, data, c)) + 1} of {len(todo)}", flush=True)
        print(f"  uploaded  https://youtu.be/{resp['id']}  {c['title'][:50]}"
              + (f"  -> goes live {when:%a %b %d %I:%M %p}" if when else ""))
