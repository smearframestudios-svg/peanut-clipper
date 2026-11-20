# What's new

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
