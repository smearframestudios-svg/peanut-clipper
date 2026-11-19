# Peanut Clipper

## Install

Download **`Install Peanut Clipper.bat`** from this page (click it, then the download button) and double-click it.
It installs into `Documents\PeanutClipper` and puts a **Peanut Clipper** icon on your Desktop and in the Start menu.
(If you put the installer inside an existing PeanutClipper folder, it upgrades that one instead.)

## Start it

Click the **Peanut Clipper** icon. The app opens in your browser. Use **Quit** in the top corner to close it.

## Updates

When a new version is out you'll see **Update available** at the top of the app. Click it, then **Update now**.
Your settings, banners, layout, YouTube login and Shorts are kept.

**The first install** spends about 10–20 minutes installing everything. It downloads about 2–3 GB (your graphics card's libraries, ffmpeg and the speech model) and tests your RTX 2080. After that, the app starts in a few seconds.

**If Windows shows "Windows protected your PC",** click **More info**, then **Run anyway**.

## Use it

| Tab | What it's for |
|---|---|
| **Make Shorts** | Paste a finished stream link and click **Make Shorts**. A progress bar shows how it's going. |
| **Review** | Click **Edit** to move a Short's start or end while seeing the whole stream around it, then click **Update Short**. Approve or Reject each Short; rejected ones are deleted. |
| **Approved** | **Export for Premiere** saves the raw horizontal clip (full quality, 60 fps, 3 extra seconds on each side) to your folder, ready to drop into your template. You can also upload a Short straight to YouTube. |
| **Settings** | Auto mode, how many Shorts per stream, captions, auto-delete, graphics card, Twitch. |
| **Layout & Banners** | Drag boxes so Shorts show the peanut on top and gameplay underneath, and add your banners as transparent PNGs. |

## Auto mode

Turn it on in **Settings**. Every night it:
1. checks his YouTube streams page,
2. downloads the newest finished stream,
3. makes Shorts from it,
4. deletes the download.

In the morning, open the app and go to **Review**. The app doesn't need to be open for this, and your PC can be asleep. It needs at least 30 GB of free disk space.

## Good to know

- **Jobs run at low priority,** so games and other programs always come first.
- **Auto-delete is on by default.** A downloaded stream is kept until every Short from it has been rejected, uploaded or exported (or for 3 days), so you can re-cut Shorts until then. Rejected, uploaded and exported Shorts are deleted too.
- **Your data stays in the app folder:** settings, layout and YouTube login are saved in the `data` folder.
- **Something not working?** Run `Troubleshoot - start with log window.bat` to see what the app is doing, or check `data\app.log`.
- **To uninstall,** delete the PeanutClipper folder and the Desktop/Start Menu shortcuts. If you turned on auto mode, also open Task Scheduler and delete the task called "Peanut Clipper Nightly".
