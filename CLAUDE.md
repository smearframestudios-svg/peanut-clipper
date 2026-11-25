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
`.venv/` packages, `bin/` (ffmpeg, ffprobe, deno, ort-dml = the cut-out job's own DirectML onnxruntime), `data/` (settings.json, layout.json, editor_media/ (intro/outro/music for the editor), models/ (cut-out ONNX models),
overlays/, client_secret.json, token.json, hardware.json, processed.json, logs), `work/`
(downloaded streams), `output/` (Shorts + clips.json), `exports/`, `compilations/` (each compilation's moments). New settings go in
`DEFAULT_SETTINGS` in `clipper/util.py` so existing installs pick up defaults.

## Layout
- `clipper/app.py` server + job runner (jobs run as low-priority subprocesses: `python -m clipper <cmd>`),
  `clipper/app_page.py` the whole UI (one HTML string).
- `pipeline.py` find moments -> `score.py` (chat/audio/names), `transcribe.py` (faster-whisper),
  `render.py` (ffmpeg 1080x1920, banners, NVENC), `search.py` (keyword search over a full
  cached transcript + chat, Shorts/exports from matches, saved keywords; --sound-only = download.download_audio, then
  search.match_video fetches a ±2 min video piece per used match via download.download_part, shift = piece start), `library.py` (review state, re-cut, sections, screenshots, Premiere export,
  auto-delete, stream_info = a Short's time/link in the stream, permanent History in data/history.json + data/history/ thumbs), `compile.py` (compilations: moments copied out of searches, 16:9 export, Premiere XML; collections = same store with
  kind "collection": Review Shorts copied in (vfile + horizontal file with handles), vertical or horizontal montage),
  `titlecard.py` (Title Cards tab: Pillow renderer, bundled clipper/fonts/BarlowCondensed-BlackItalic.ttf (OFL), /api/titlecard/preview|draft|save),
  `storage.py` (Settings > Storage scan + auto-delete rules; library.cleanup_sources now calls storage.auto_clean; runs at start, after decide/upload/export, nightly),
  video files (the Make Shorts box takes a link OR a file): app.save_upload streams the file into
  work/_downloads/upload-<name>-u<time>/source.<ext> (inbox.new_upload_folder: title.txt + an `uploaded` marker), then a normal `vod` job on that path
  (pipeline treats the folder like a download: fix_sync, cache, source_dir); "remove" = /api/video_upload_discard,
  Compilations editor (#edTl timeline, #edInsp, ED state in app_page): compile.edit actions split/moment(title,text,tr,zoom)/media + undo
  (compilations/<id>/history.json, 40 steps; _gc deletes files only when no step uses them), + Add menu: add_range (from this stream, `compaddrange` job, needs c.source_file), add_file (clip from the PC: /api/comp_upload -> compilations/<id>/_in/,
  `compaddfile` job, tall clips via _blur_wide), add_short (a Review Short, `coladd` job with --after; compilations get a blurred 16:9 file when the stream is gone); Review cards also have
  "Add to editor" (edButton/markEd, CMPMEM from /api/comps members = compile.memberships(kind)),
  export_video: intro/outro (_norm_piece), per-part zoom crop (_zoom_filter from the default layout) + text PNG (_text_png) + tr, xfade joins on settb=AVTB,
  music bed pass, chapters() -> '<name> - chapters.txt',
  `roto.py` (Cut-out tab: RVM + U2-Net human ONNX models from GitHub into data/models, run in the `roto` job with its own DirectML onnxruntime from bin/ort-dml
  (never import that in other processes - faster-whisper has the plain onnxruntime); Cutter.frame = matte, tracked component from the click (scipy),
  head-only via shell colour + convex hull, leave-out boxes with time ranges; resolve(spec) short/part/upload; outputs ProRes 4444 .mov / green mp4 / PNGs in exports/Cut-outs),
  `longvid.py` (Make: Long video / Both on the Make Shorts box: pipeline.fetch_source + check_video shared with process_vod, Detector with longer/closer
  moments and min_score 0, pick() best until long_minutes, saved as a compilation via compile.copy_range; data/last_longvid.json for the page),
  `inbox.py` (Auto-clip folder card: settings watch_enabled/watch_folder/watch_after move|delete|keep/watch_layout; app.inbox_watcher starts
  `python -m clipper inbox --one` when idle, auto.run_auto calls inbox.run_all; state in data/inbox.json, per-file claims in data/inbox_claims/),
  `live.py` (Record live: separate background process, state in data/live.json + heartbeat, stop via data/live.stop;
  saves to work/_downloads/<id>/source.mp4 + chat.live_chat.json so every other feature just works), `upload.py` (YouTube API), `auto.py` (nightly scheduled task), `updater.py`, `setup_app.py`.
- Progress lines printed as `@@ <pct> <label>` drive the progress bar.

## Layouts
Saved in `data/layouts.json` ({default, layouts:[{id,name,mode stack|single|blurfit,avatar,gameplay,top_height,banners}]}).
`util.apply_layout(cfg, id)` sets `cfg["layout"]` for the renderer; each clip records its `layout` id.

## Owner preferences
- Edits Shorts in Premiere Pro (vertical 1080x1920, 60 fps template with their own banners).
- Previews must not autoplay; approved items leave the review list; no duplicate files left in folders.
- PC: i7-9700KF, RTX 2080 (NVENC + CUDA Whisper), Windows 10.
