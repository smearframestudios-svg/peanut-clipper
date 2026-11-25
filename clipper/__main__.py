"""Peanut Clipper. Normally started by double-clicking "Peanut Clipper.bat" (runs `app`).

  python -m clipper app                     # the app (opens in your browser)
  python -m clipper vod <link or file> [--from 1:00:00 --to 2:30:00]
  python -m clipper clips [--hours 24 --top 8]
  python -m clipper upload [--dry-run]
  python -m clipper auto                    # what the nightly task runs
"""
import argparse
import sys

from .util import parse_hms, setup_env


def _log_to_file():
    """The shortcut runs without a console window; keep a log for troubleshooting."""
    from .util import DATA
    if sys.stdout is None or not sys.stdout.isatty():
        DATA.mkdir(exist_ok=True)
        log = DATA / "app.log"
        if log.exists() and log.stat().st_size > 2_000_000:
            log.unlink()
        f = open(log, "a", encoding="utf-8", buffering=1)
        sys.stdout = sys.stderr = f


def main(argv=None):
    setup_env()
    ap = argparse.ArgumentParser(prog="clipper", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a_app = sub.add_parser("app")
    a_app.add_argument("--port", type=int, default=8765)
    a_app.add_argument("--no-browser", action="store_true")
    la = sub.add_parser("launch", help="what the desktop shortcut runs (no console window)")
    la.add_argument("--no-browser", action="store_true")
    la.add_argument("--wait", action="store_true")
    sub.add_parser("install", help="setup + desktop/start menu shortcuts")
    sub.add_parser("setup")
    sub.add_parser("whispertest")
    sub.add_parser("hwtest")
    v = sub.add_parser("vod")
    v.add_argument("source")
    v.add_argument("--from", dest="start")
    v.add_argument("--to", dest="end")
    v.add_argument("--chat")
    v.add_argument("--keep", type=int)
    v.add_argument("--no-review", action="store_true")
    v.add_argument("--layout")
    c = sub.add_parser("clips")
    c.add_argument("--hours", type=int, default=24)
    c.add_argument("--top", type=int, default=8)
    c.add_argument("--no-review", action="store_true")
    c.add_argument("--layout")
    u = sub.add_parser("upload")
    u.add_argument("--dry-run", action="store_true")
    sub.add_parser("auto")
    ib = sub.add_parser("inbox", help="make Shorts from videos waiting in the auto-clip folder")
    ib.add_argument("--one", action="store_true", help="just the oldest waiting video")
    rr = sub.add_parser("rerender", help="re-cut a Short with new start/end (seconds in the stream file)")
    rr.add_argument("job")
    rr.add_argument("id")
    rr.add_argument("start", type=float)
    rr.add_argument("end", type=float)
    rr.add_argument("--layout")
    rr.add_argument("--framing", help="this Short's own framing as JSON, or none to go back to the layout")
    rr.add_argument("--sections", help="this Short's sections as JSON (else the saved ones)")
    sf = sub.add_parser("syncfix", help="convert a Short's (or a search's) stream to H.264")
    sf.add_argument("job")
    sf.add_argument("id", nargs="?")
    sf.add_argument("--search", action="store_true", help="job is a search id")
    ex = sub.add_parser("export", help="export raw horizontal clips for Premiere")
    ex.add_argument("job", nargs="?")
    ex.add_argument("id", nargs="?")
    ex.add_argument("--all", action="store_true", help="every approved Short")
    se = sub.add_parser("search", help="find every time words are said in a stream")
    se.add_argument("source")
    se.add_argument("--words", required=True, help='comma-separated, e.g. "drive, use a blinker"')
    se.add_argument("--from", dest="start")
    se.add_argument("--to", dest="end")
    se.add_argument("--no-chat", action="store_true")
    se.add_argument("--exact", action="store_true", help="only exact word forms")
    se.add_argument("--layout")
    se.add_argument("--sound-only", action="store_true", help="download just the sound; video only for matches you use")
    fs = sub.add_parser("fromsearch", help="make a Short (or Premiere export) from a search match")
    fs.add_argument("sid")
    fs.add_argument("idx", type=int)
    fs.add_argument("--export", action="store_true")
    fs.add_argument("--layout")
    lv = sub.add_parser("live", help="record a stream while it's live (video + chat)")
    lv.add_argument("url", nargs="?")
    lv.add_argument("--from-start", action="store_true", help="record from the very start of the stream")
    lv.add_argument("--wait", action="store_true", help="wait for him to go live (checks every 5 minutes)")
    lv.add_argument("--then-make", action="store_true", help="make Shorts as soon as the stream ends")
    lv.add_argument("--recover", action="store_true", help="save a recording that stopped unexpectedly")
    ca = sub.add_parser("compadd", help="copy a keyword-search match into a compilation")
    ca.add_argument("comp")
    ca.add_argument("sid")
    ca.add_argument("idx", type=int)
    cs = sub.add_parser("coladd", help="put a Review Short into a collection")
    cs.add_argument("comp")
    cs.add_argument("job")
    cs.add_argument("clip")
    ce = sub.add_parser("compexport", help="export a compilation (one 16:9 video, or a Premiere folder)")
    ce.add_argument("comp")
    ce.add_argument("--premiere", action="store_true")
    fr = sub.add_parser("frame", help="grab one frame from a stream for the Layout screen")
    fr.add_argument("source")
    fr.add_argument("--at", default="1:00:00")
    a = ap.parse_args(argv)

    if a.cmd == "launch":
        _log_to_file()
    if a.cmd == "install":
        from .setup_app import run_setup
        from .shortcuts import make_shortcuts
        run_setup()
        made = make_shortcuts()
        print("\nShortcuts created: " + (", ".join(made) if made else "none (not on Windows)"))
        return 0
    if a.cmd == "setup":
        from .setup_app import run_setup
        return run_setup()
    if a.cmd == "whispertest":
        from .setup_app import whisper_gpu_selftest
        return whisper_gpu_selftest()

    from .util import load_config, need
    cfg = load_config()
    need("ffmpeg", "Close this and open Peanut Clipper again - it will reinstall ffmpeg.")

    if a.cmd == "hwtest":
        from .setup_app import hardware_test
        print(hardware_test(force=True))
    elif a.cmd == "launch":
        from .app import serve_app
        serve_app(cfg, 8765, not a.no_browser, wait=a.wait)
    elif a.cmd == "app":
        from .app import serve_app
        serve_app(cfg, a.port, not a.no_browser)
    elif a.cmd == "vod":
        from .pipeline import process_vod
        process_vod(a.source, cfg, parse_hms(a.start), parse_hms(a.end), a.chat, a.keep, a.layout)
    elif a.cmd == "clips":
        from .pipeline import process_twitch_clips
        process_twitch_clips(cfg, a.hours, a.top, a.layout)
    elif a.cmd == "upload":
        from .upload import upload_approved
        upload_approved(cfg, a.dry_run)
    elif a.cmd == "auto":
        from .auto import run_auto
        run_auto(cfg)
    elif a.cmd == "inbox":
        from . import inbox
        if a.one:
            inbox.run_one(cfg)
        else:
            inbox.run_all(cfg)
    elif a.cmd == "rerender":
        from .library import rerender
        rerender(cfg, a.job, a.id, a.start, a.end, a.layout, a.framing, a.sections)
    elif a.cmd == "syncfix":
        if a.search:
            from .search import syncfix_search
            syncfix_search(cfg, a.job)
        else:
            from .library import syncfix
            syncfix(cfg, a.job, a.id)
    elif a.cmd == "export":
        from .library import clips, export_raw
        todo = [(c["job"], c["id"]) for c in clips(cfg, "approved")] if a.all else [(a.job, a.id)]
        for i, (job, cid) in enumerate(todo, 1):
            print(f"@@ {int(100 * (i - 1) / max(1, len(todo)))} Exporting {i} of {len(todo)}", flush=True)
            export_raw(cfg, job, cid)
        print(f"@@ 100 Exported {len(todo)} clip(s)", flush=True)
    elif a.cmd == "search":
        from .search import run_search
        run_search(cfg, a.source, a.words, parse_hms(a.start), parse_hms(a.end), not a.no_chat, not a.exact,
                   a.layout, a.sound_only)
    elif a.cmd == "fromsearch":
        from .search import clip_from_match
        st = cfg["settings"]
        clip_from_match(cfg, a.sid, a.idx, a.export, st.get("search_lead_sec", 10), st.get("search_tail_sec", 8),
                        a.layout)
    elif a.cmd == "live":
        from . import live
        if a.recover:
            live.recover(cfg)
        else:
            live.record(cfg, a.url or cfg["settings"]["channel_url"], a.from_start, a.wait, a.then_make)
    elif a.cmd == "compadd":
        from .compile import add_moment
        add_moment(cfg, a.comp, a.sid, a.idx)
    elif a.cmd == "coladd":
        from .compile import add_short
        add_short(cfg, a.comp, a.job, a.clip)
    elif a.cmd == "compexport":
        from .compile import export_premiere, export_video
        (export_premiere if a.premiere else export_video)(cfg, a.comp)
    elif a.cmd == "frame":
        from .app import grab_frame
        grab_frame(cfg, a.source, parse_hms(a.at))
    return 0


if __name__ == "__main__":
    sys.exit(main())
