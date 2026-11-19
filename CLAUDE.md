# Peanut Clipper - notes for Claude

Windows desktop app (local web UI) that turns TheBurntPeanut stream VODs into Shorts for the
owner's fan channel @BurntPeanutXD. The owner is not a programmer: they install with
`Install Peanut Clipper.bat`, open it from the Desktop icon, and update with the in-app
**Update** button, which pulls `main` from this repo.

## Shipping a change (every time)
1. Make the change; keep the owner's data untouched (see below).
2. Bump `VERSION` (x.y.z) and add a `## x.y.z` section at the top of `CHANGELOG.md` written in
   plain, non-technical words - the app shows it to the owner as "What's new".
3. Test what you can headless (python3 -m clipper ..., playwright for the UI), then push to `main`.
   The owner then just clicks "Update now" in the app.
4. If `requirements.txt` changes, the updater re-runs `clipper setup`, which installs it.

## Never touched by updates (owner's data)
`.venv/` packages, `bin/` (ffmpeg, ffprobe, deno), `data/` (settings.json, layout.json,
overlays/, client_secret.json, token.json, hardware.json, processed.json, logs), `work/`
(downloaded streams), `output/` (Shorts + clips.json), `exports/`. New settings go in
`DEFAULT_SETTINGS` in `clipper/util.py` so existing installs pick up defaults.

## Layout
- `clipper/app.py` server + job runner (jobs run as low-priority subprocesses: `python -m clipper <cmd>`),
  `clipper/app_page.py` the whole UI (one HTML string).
- `pipeline.py` find moments -> `score.py` (chat/audio/names), `transcribe.py` (faster-whisper),
  `render.py` (ffmpeg 1080x1920, banners, NVENC), `library.py` (review state, re-cut, Premiere export,
  auto-delete), `upload.py` (YouTube API), `auto.py` (nightly scheduled task), `updater.py`, `setup_app.py`.
- Progress lines printed as `@@ <pct> <label>` drive the progress bar.

## Owner preferences
- Edits Shorts in Premiere Pro (vertical 1080x1920, 60 fps template with their own banners).
- Previews must not autoplay; approved items leave the review list; no duplicate files left in folders.
- PC: i7-9700KF, RTX 2080 (NVENC + CUDA Whisper), Windows 10.
