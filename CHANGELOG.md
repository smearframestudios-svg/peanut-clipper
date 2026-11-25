# What's new

## 1.16.0
- New editor on the Compilations tab, for your long videos and compilations. It has a player, a timeline of parts, and the settings of the part you picked.
- Timeline: drag parts to reorder, drag the yellow edges to trim, right-click to remove. Split at playhead (or the S key), Delete part, and Undo (Ctrl+Z) for the last 40 changes.
- Each part: its own title, the way it goes into the next part (Cut, Flash or Fade), text on screen for the first few seconds, and zoom (Full, Peanut cam or Gameplay, from your default layout's boxes). The player shows the zoom and text before you export.
- + Add: scrub the whole stream and mark a start and end to add a new part (long videos made on Make Shorts).
- Intro, outro and a music bed: upload a clip or a song once and pick it for any video. The music fades in and out, with its own volume.
- Chapters for YouTube: made from the part titles. Copy them from the editor; they're also saved next to the exported video.
- Export 1920x1080 includes all of it. Export for Premiere still gives every part on its own cut.

## 1.15.0
- Long video (16:9): the Make Shorts box now has Make: Shorts / Long video / Both. Long video picks the strongest moments of a stream or your own video until it reaches the length you pick (8, 10, 15 or 20 minutes), keeps them in stream order, and puts them in Compilations as a 1920x1080, 60 fps video.
- Both: makes the Shorts and the long video from the same stream in one go (it only downloads once).
- Edit it: when it's done, press Open it in Compilations to trim, reorder or remove moments, then export one MP4 or a Premiere project. A bigger editor is coming next.
- Fixed: two quick clicks on settings could undo each other.

## 1.14.0
- One box for links and videos: the Make Shorts box now takes a stream link or your own video. Drop a video on it (or press Choose file) and it uploads right away. Press Make Shorts when you're ready; pressing it while the upload is still going starts as soon as it's done. This replaces the separate "From your own video" box.
- Auto-clip folder: a new card on Make Shorts. Turn it on, and any video you put in that folder gets made into Shorts on its own, while the app is open and in the nightly auto run. They show up in Review like any other Shorts.
- Finished videos: by default they move to a "Done" folder inside it. You can have them deleted instead, or left where they are (they won't be clipped twice).
- Layout for the folder: pick which layout the folder's videos use.
- If a video can't be clipped: the card says why, with a Try again button, and nothing is left behind.

## 1.13.0
- Upload your own video: a new "From your own video" box on Make Shorts. Drop a video in (or press Choose file) and the app finds the best moments and makes Shorts, just like with a stream link.
- Make Shorts as soon as it's in: on by default. If something else is running, it starts right after that job finishes.
- Only use part of the video: pick a from/to time, same as for streams.
- Your original is safe: the app works on its own copy. The copy shows in Settings > Storage as "Your video" and is cleaned up like downloads once its Shorts are done.
- Any format: MP4, MOV, MKV, WEBM and more. Videos that would play out of sync are converted once, like YouTube streams.

## 1.12.1
- Listen and Preview: the player now opens right under the match you clicked, so the page no longer jumps back up to the top of the list.

## 1.12.0
- Storage: Settings now shows how much space Peanut Clipper uses (downloads, the app's Shorts, exports, compilations), how much is free, and the biggest items - each with its own Delete button.
- Clean up now: deletes everything your Auto-delete rules allow, after showing you the list.
- Auto-delete fixed: downloads that no Short was ever made from (cancelled runs, unused live recordings, stream parts) now get deleted after your "after this many days" setting too. Before, they stayed forever.
- New rules: the app's copy of Shorts exported to Premiere (after 3 days, if "Delete once they're on YouTube" is off) and old keyword searches (after 14 days). Shorts still waiting in Review or Approved are never deleted.
- Auto-delete now also runs every night with the nightly auto mode, before it downloads anything.

## 1.11.0
- Sound-only keyword search: a new box on keyword search (on by default) downloads just the sound and chat - about 0.7 GB for a 12-hour stream instead of ~30 GB - and finds your words much faster.
- Video only when you use it: Make Short, Export for Premiere or Add to compilation on a match downloads just that part of the video (about 2 minutes either side, usually 10-30 seconds to get).
- Listen: matches from a sound-only search play the sound so you can check them before using them.
- If the whole stream is already on your PC (from Make Shorts), the search uses it and nothing extra is downloaded.
- Untick the box to download the whole video like before.

## 1.10.0
- Title Cards: a new tab that makes big outlined thumbnail-style text (white, yellow and red lines, red box, red swoosh, rough red brush) as a see-through 1080x1920 picture for the top of a Short.
- From the Short's title: press "Title card" on any Short in Review (or pick one in the list) and it splits the title into lines and styles them for you. Change any line's words, colour, size or extra.
- Shuffle styles: tries new colours, boxes and swooshes on your lines, keeping your words.
- Live preview over a checkerboard or over the Short itself, with the safe zones if you want them. Top / Middle / Bottom keeps the text clear of YouTube's buttons.
- Save PNG puts the full-size picture in your Export folder\Title cards (Change to pick another folder). Copy puts the preview on the clipboard.
- This update installs one extra part the first time (for drawing the pictures) - it happens by itself during Update now.

## 1.9.2
- YouTube safe zones: tick "Safe zones" on the Layouts & Banners preview, the trim editor's live preview or the framing preview to see where YouTube's Shorts buttons cover the video (top bar, the like/comment/share buttons on the right, and the avatar/subscribe/title area at the bottom). Keep faces, captions and banners inside the dashed box.
- It's only a guide on the preview - it never shows up in your Shorts. Your choice is remembered.

## 1.9.1
- Screenshot folder: pick where screenshots go in Settings (Premiere export section). Leave it empty to keep using your Export folder\Screenshots.
- Browse buttons: the Export folder and the Screenshot folder each have Browse... (the normal Windows folder picker) and Open.
- Change folder: every "Screenshot saved" message now has a Change folder link next to Open the folder.
- Fix: messages shown while the trim editor is open (like "Screenshot saved") can be clicked again - they used to sit behind the editor.
- The tab names stay on one line on smaller windows.

## 1.9.0
- Collections: a new tab for saving Shorts for a montage later. Press "+ Collection" on any Short in Review and pick a collection (or make a new one).
- Stays in Review: adding a Short to a collection doesn't approve or reject it - you can still use it as a Short too. The button then says which collection it's in.
- Safe from auto-delete: each collection keeps its own copy of the Short (and of the original stream moment, while the stream is still on your PC).
- Montage shape: export it vertical 9:16 (as the Shorts look) or horizontal 16:9 (the original stream view).
- Arrange: drag to reorder, Up/Down, Shuffle, Oldest first, Preview, Play all, and an optional length goal.
- Between clips: Cut, Quick flash or Crossfade, and clip numbers on screen if you want them.
- Export montage makes one finished video. Export for Premiere gives each clip as its own file plus a ready-made sequence (File, Import, the .xml).

## 1.8.0
- Stream time on every Short: Review and Approved cards now show where the Short came from in the stream (like 1:42:07 - 1:42:41), with "Open stream there" (opens YouTube at that exact second) and "Copy time".
- History: a new tab with every Short you upload, export or reject - its stream time, the stream's name and date, and a small picture. It stays even after the video files are deleted, so you can always go back and grab a screenshot.
- Find it fast: search History by title or words said, or show only Uploaded, Exported or Rejected. Uploaded ones have a "Watch the Short" link.
- Screenshot from History: while the stream is still on your PC, pick any time and save a full-size picture of the stream at that moment.
- History starts with Shorts finished after this update (older deleted ones weren't recorded).

## 1.7.0
- Record live: a new card at the top of Make Shorts records Peanut's stream while he's live - video and chat - so you don't have to wait hours for YouTube to process it.
- Record now or wait: press Record now while he's live, or "Wait for him to go live" and it checks every 5 minutes and starts on its own.
- From the very start: if you start late, it can still grab the stream from the beginning.
- While it records: see how long it's been, the size, chat messages and free disk space. You can keep using the rest of the app, and it keeps recording even if you close Peanut Clipper.
- When he ends: the recording is saved like any downloaded stream. Make Shorts from it, keyword search it, or add moments to a compilation - no extra download.
- Make Shorts as soon as he ends: turn it on and the app starts finding moments the minute the stream is over.
- Nightly auto mode: can also check if he's live and start recording (off until you tick the box).
- Internet hiccup: if the connection drops while he's still live, it picks the recording back up by itself.

## 1.6.0
- Compilations: a new tab for long videos made of many moments, like every GTA crash. Add moments from keyword searches on as many streams as you like.
- Add to compilation: every keyword-search result has a "+ Add to compilation" button. Once a moment is in, the button says "Added (4th)" so you don't add it twice.
- Crash words: one button fills the search box with GTA crash words (crash, wreck, my car, flip, oh no...).
- Safe from auto-delete: each moment is copied out of its stream the moment you add it, so old streams can be cleaned up without breaking your compilation.
- Goal bar: set a goal (8 minutes to start) and see how much more you need.
- Arrange: drag the number to reorder, or use Up/Down, Shuffle or Oldest first. Nudge each moment's start and end by a second. Preview one, or Play all.
- Between moments: Cut, Quick flash, or Crossfade. Moment numbers (#1, #2...) on screen can be turned on.
- Export video (16:9): one finished 1920x1080, 60 fps video in your exports folder.
- Export for Premiere: every moment as its own file plus a ready-made sequence. In Premiere: File, Import, pick the .xml - every moment is already cut in order, with extra seconds on each end to drag out.

## 1.5.0
- Sections: in the trim editor, press C (or Ctrl+K) to cut the Short at the playhead, like the razor in Premiere. Click a part on the new Sections bar to pick how it looks.
- Close-up on Peanut: make any part a full-screen close-up of Peanut's reaction or joke. Drag the pink box to choose exactly what fills the screen.
- Gameplay only: make any part show just the game, full screen.
- Banner per part: put the banner in its layout spot, at the bottom, at the top, or turn it off - for just that part.
- Live preview: the editor shows the Short as it will look at the playhead, so you see each part before you press Update Short.
- Screenshots: press Ctrl+Shift+E (or the Screenshot button) to save the frame at the playhead as a full-size picture - as it looks in the Short, or the full stream frame. They go in your exports folder under Screenshots.
- Remove a cut: right-click it, or use "Remove cut before this part". Your cuts are saved as you go.

## 1.4.2
- Fixed "The process cannot access the file": re-cutting a Short no longer stops when Windows has the old version open (a preview playing, or Premiere). The new version is saved, and the old one is deleted as soon as it's free (after the next job or when the app starts).
- Previews don't lock files: videos in the app no longer keep files locked while paused.
- Editor lets go first: the editor releases the current Short before re-cutting it.

## 1.4.1
- Markers in the trim editor: press M (or "+ Marker at playhead") to drop a blue marker where the video is.
- Snap to markers: dragging the start or end handle, or the whole selection, snaps onto a marker when you get close. Untick "Snap to markers" to drag freely.
- Jump between markers: use the Marker buttons, or click a marker on the timeline. Right-click a marker to remove it, or use "Clear markers".
- Saved with the Short: markers are still there the next time you open it.

## 1.4.0
- Framing for one Short: in the trim editor, open "Framing for this Short" to change where Peanut sits and how much of the game shows, for just that Short.
- Peanut box and Gameplay box: drag a box to move it, drag on the frame to redraw it, and use Zoom to show more or less. The frame is wherever the stream video is paused.
- Peanut area height: slide to choose how much of the Short is Peanut and how much is gameplay. You can also switch style (Peanut over gameplay, Gameplay only, Whole stream).
- Live preview: a small vertical preview with your banners updates as you drag.
- Use for this Short: re-cuts only this Short with that framing. Your layouts stay the same.
- Save as new layout: keeps this framing as a layout you can pick for future streams.
- Reset to layout: goes back to the layout's framing (press Update Short to re-cut).

## 1.3.5
- Slide the whole selection: in the trim editor, grab the yellow selected area and drag it left or right. Both ends move together and the length stays the same. The handles still change the start and end on their own.

## 1.3.4
- You pick how much to convert: Settings, Trim editor, "Minutes to convert for editing" (4, 6, 10, 20 or 30 min, centred on the Short). The default is 6 minutes, so the editor is ready even faster.
- Need more room later: raise the minutes in Settings and open the Short again. Only then does it convert the bigger part.
- Clearer wait time: the progress bar says "under a minute left" near the end.

## 1.3.3
- Editor opens fast: when a stream comes in a format your graphics card can't play smoothly (AV1), the app now converts only the half hour around the Short you're editing, which takes a minute or two instead of an hour or more for the whole stream.
- Real progress: converting shows a moving percentage and about how many minutes are left, so it never looks stuck.
- Re-cutting works from that converted part too, so Update Short doesn't wait for the whole stream either.

## 1.3.2
- Update while a job runs: pressing "Update now" during a job no longer stops you. It updates by itself as soon as the job finishes.
- Easier to read: in "What's new", the first words of each change are bold.

## 1.3.1
- Edit while a job runs: no more "Something is already running". You can edit a Short (Update Short), export, or cut a keyword match while a stream is still being made. It waits in line and starts by itself when the current job finishes.
- Waiting line shown: the progress bar says how many jobs are waiting.
- Approve and Reject keep working while a job runs, like before.

## 1.3.0
- Saved layouts: make as many layouts as you want (e.g. "GTA", "ARC Raiders", "Gameplay only") on the Layouts & Banners screen. Your current layout is kept as "Main".
- Three styles per layout: Peanut over gameplay, Gameplay only (one box fills the whole Short), or Whole stream.
- Move a box by dragging inside it, and use the Zoom slider to frame tighter. Changes save by themselves.
- Pick which banners go on each layout.
- Choose the layout when you make Shorts (top of Make Shorts), and switch any single Short to a different layout in the trim editor, then Update Short.

## 1.2.3
- Premiere-friendly files: exports and Shorts now use the most compatible H.264 settings, a steady frame rate and standard 48 kHz stereo audio, so Premiere imports them without "unsupported compression type" errors.

## 1.2.2
- Fixed audio going out of sync in the trim editor and keyword previews. YouTube often sends streams in a format (AV1/VP9) your graphics card can't play smoothly, so the picture fell behind the sound.
- New downloads now always use the smooth-playing H.264 format.
- Streams you already downloaded get converted once (a few minutes on your graphics card) the first time you edit or preview them. The editor opens by itself when it's done.

## 1.2.1
- Fixed black windows flashing on screen while the app is open (it got worse with nightly auto mode on). Everything the app runs in the background is now hidden.

## 1.2.0
- Find by keywords: on Make Shorts, search a stream for words or phrases like "drive, use a blinker". You get every moment he says them (and when chat spams them), with the sentence around it.
- Each match has Preview, Make Short (opens straight in the trim editor) and Export for Premiere.
- Saved keywords (Settings): words to look for in every stream you clip, including the nightly run. Matches become extra Shorts.
- "Match similar words" finds driving/drives/driver when you search drive.

## 1.1.0
- Peanut Clipper is now a real app: Desktop and Start Menu icon, no black window, and a Quit button.
- Updates itself from GitHub: you'll see "Update available" at the top. Click it, then Update now.
- The progress bar now shows real progress when you use "Only use part of the stream".

## 1.0.0
- Trim editor: move a Short's start/end while seeing the whole stream around it.
- Export for Premiere: raw horizontal clips at full quality and the stream's own frame rate.
- Banners: add transparent PNG banners that go on every Short.
- Nightly auto mode, GPU speed, low priority, auto-delete.
