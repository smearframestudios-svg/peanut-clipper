PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Peanut Clipper</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--bg:#111214;--panel:#1a1b1f;--panel2:#22242a;--line:#2d3038;--text:#f2f2f3;--mute:#9a9ca5;
--acc:#ffc93c;--acc2:#e0a800;--ok:#2fb36d;--no:#e05252;--blue:#4aa3ff}
*{box-sizing:border-box}html,body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 "Segoe UI",system-ui,sans-serif}
header{display:flex;align-items:center;gap:22px;padding:0 28px;height:64px;border-bottom:1px solid var(--line);background:#0c0d0f;position:sticky;top:0;z-index:5}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:18px;letter-spacing:.2px}
.brand .dot{width:26px;height:26px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#e8b56a,#a8662a);box-shadow:0 0 0 2px #0c0d0f,0 0 0 3px #a8662a55}
nav{display:flex;gap:4px;height:100%}
nav button{background:none;border:0;color:var(--mute);font:inherit;font-weight:600;padding:0 14px;cursor:pointer;border-bottom:3px solid transparent;height:100%}
nav button.on{color:var(--text);border-bottom-color:var(--acc)}
.badge{display:inline-block;min-width:20px;padding:0 6px;margin-left:6px;border-radius:99px;background:var(--acc);color:#111;font-size:12px;font-weight:800;text-align:center}
.badge:empty{display:none}
.hw{margin-left:auto;display:flex;gap:8px}
.pill{font-size:12px;padding:3px 10px;border-radius:99px;background:var(--panel2);color:var(--mute);border:1px solid var(--line)}
.pill.good{color:#9ee6bd;border-color:#2fb36d55}
button.pill{cursor:pointer;font:inherit;font-size:12px}button.pill:hover{color:var(--text)}
.pill.upd{background:var(--acc);color:#111;border-color:var(--acc);font-weight:800}
.cover{position:fixed;inset:0;background:#0d0e10f2;z-index:50;display:none;align-items:center;justify-content:center;flex-direction:column;gap:14px;text-align:center}
.cover.on{display:flex}.cover h2{margin:0}.spin{width:42px;height:42px;border:4px solid #333;border-top-color:var(--acc);border-radius:50%;animation:sp 1s linear infinite}
@keyframes sp{to{transform:rotate(360deg)}}
pre.notes{white-space:pre-wrap;background:#0f1012;border:1px solid var(--line);border-radius:9px;padding:12px;font:13px/1.5 "Segoe UI",sans-serif;color:#d6d7db;max-height:240px;overflow:auto}
main{max-width:1180px;margin:0 auto;padding:28px}
section{display:none}section.on{display:block}
h2{margin:0 0 4px;font-size:22px}p.sub{margin:0 0 22px;color:var(--mute)}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:22px;margin-bottom:18px}
.card h3{margin:0 0 12px;font-size:16px}
.row{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
input[type=text],input[type=time],input[type=number],input[type=password]{background:#0f1012;border:1px solid var(--line);color:var(--text);border-radius:9px;padding:11px 13px;font:inherit}
input.big{flex:1;min-width:280px;font-size:16px}
input.small{width:120px}
.btn{border:0;border-radius:10px;padding:12px 20px;font:inherit;font-weight:700;cursor:pointer;background:var(--panel2);color:var(--text);border:1px solid var(--line)}
.btn.main{background:var(--acc);color:#111;border-color:var(--acc)}.btn.main:hover{background:var(--acc2)}
.btn.ok{background:var(--ok);border-color:var(--ok);color:#fff}.btn.no{background:var(--no);border-color:var(--no);color:#fff}
.btn:disabled{opacity:.45;cursor:not-allowed}
.link{background:none;border:0;color:var(--blue);cursor:pointer;font:inherit;padding:0}
.mute{color:var(--mute)}.tiny{font-size:13px}
.bar{height:12px;border-radius:99px;background:#0f1012;border:1px solid var(--line);overflow:hidden;margin:12px 0 8px}
.bar>i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--acc2),var(--acc));transition:width .6s}
.bar.err>i{background:var(--no)}.bar.done>i{background:var(--ok)}
pre.log{background:#0b0c0e;border:1px solid var(--line);border-radius:9px;padding:12px;max-height:260px;overflow:auto;font:12px/1.45 Consolas,monospace;color:#c9cbd1;white-space:pre-wrap;margin:10px 0 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:18px}
.clip{background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}
.clip video{width:100%;aspect-ratio:9/16;background:#000;display:block}
.clip .b{padding:12px;display:flex;flex-direction:column;gap:9px;flex:1}
.clip input{width:100%;font-weight:700;font-size:14px;padding:9px}
.chips{display:flex;flex-wrap:wrap;gap:5px}.chip{font-size:12px;padding:2px 8px;border-radius:99px;background:var(--panel2);color:#d6d7db}
.chip.s{background:var(--acc);color:#111;font-weight:800}
.clip .act{display:flex;gap:8px;margin-top:auto}.clip .act .btn{flex:1;padding:10px}
.empty{padding:70px 20px;text-align:center;color:var(--mute);border:1px dashed var(--line);border-radius:14px}
.plan{display:flex;flex-direction:column;gap:8px;margin:12px 0}
.plan .it{display:flex;gap:12px;align-items:center;background:var(--panel2);border-radius:10px;padding:8px}
.plan img{width:40px;height:71px;object-fit:cover;border-radius:6px;background:#000}
.plan .when{margin-left:auto;color:var(--acc);font-weight:700;white-space:nowrap}
.set{display:grid;grid-template-columns:260px 1fr;gap:14px 20px;align-items:center}
.set label.k{color:var(--mute)}
.toggle{display:flex;align-items:center;gap:10px;cursor:pointer}
.toggle input{width:18px;height:18px;accent-color:var(--acc)}
ol.steps{margin:6px 0 14px;padding-left:20px;color:#d6d7db}ol.steps li{margin:4px 0}
.stage{position:relative;user-select:none;flex:1;min-width:0}.stage img{width:100%;display:block;border-radius:8px}
.box{position:absolute;border:3px solid;pointer-events:none}.box.av{border-color:#ff4fb3;background:#ff4fb322}.box.gp{border-color:#3fa9ff;background:#3fa9ff22}
.cal{display:flex;gap:24px;align-items:flex-start}.cal .side{width:290px;display:flex;flex-direction:column;gap:12px}
canvas#prev{width:270px;height:480px;border-radius:12px;border:1px solid var(--line);background:#000}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.seg button{background:var(--panel2);color:var(--mute);border:0;padding:9px 14px;font:inherit;font-weight:600;cursor:pointer;border-right:1px solid var(--line)}
.seg button:last-child{border-right:0}.seg button.on{background:var(--acc);color:#111}
.stage{min-height:200px;background:#0c0d0f;border-radius:8px}.nofr{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--mute)}
.toast{position:fixed;right:24px;bottom:24px;background:var(--panel2);border:1px solid var(--line);border-left:4px solid var(--acc);padding:14px 18px;border-radius:10px;display:none;max-width:420px;z-index:9}
a{color:var(--blue)}
.clip .act .btn.ed{flex:0 0 auto;background:var(--panel2)}
.modal{position:fixed;inset:0;background:#000c;display:none;z-index:20;align-items:center;justify-content:center;padding:24px}
.modal.on{display:flex}
.ed-win{background:var(--panel);border:1px solid var(--line);border-radius:16px;width:min(1400px,100%);max-height:100%;overflow:auto;padding:20px 22px}
.ed-top{display:flex;align-items:center;gap:12px;margin-bottom:14px}.ed-top h3{margin:0;font-size:17px}
.ed-body{display:flex;gap:20px;align-items:flex-start}
.ed-main{flex:1;min-width:0}
.ed-main video{width:100%;background:#000;border-radius:10px;display:block;max-height:52vh}
.ed-side{width:230px;flex:none}.ed-side video{width:100%;aspect-ratio:9/16;background:#000;border-radius:10px}
.tl{position:relative;height:64px;margin:14px 0 6px;background:#0c0d0f;border:1px solid var(--line);border-radius:10px;cursor:pointer;user-select:none;overflow:hidden}
.tl .tick{position:absolute;top:0;bottom:0;width:1px;background:#2a2d34}
.tl .tick span{position:absolute;top:2px;left:4px;font-size:11px;color:#6d717b;white-space:nowrap}
.tl .orig{position:absolute;top:44px;height:6px;background:#ffffff22;border-radius:3px}
.tl .sel{position:absolute;top:18px;bottom:8px;background:#ffc93c33;border:2px solid var(--acc);border-radius:6px}
.tl .h{position:absolute;top:12px;bottom:2px;width:14px;margin-left:-7px;background:var(--acc);border-radius:4px;cursor:ew-resize}
.tl .h::after{content:"";position:absolute;left:5px;top:16px;bottom:16px;width:4px;border-left:2px solid #111;border-right:2px solid #111}
.tl .ph{position:absolute;top:0;bottom:0;width:2px;background:#fff;pointer-events:none}
.ed-ctrl{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-top:6px}
.ed-ctrl .grp{display:flex;align-items:center;gap:6px}.ed-ctrl .btn{padding:7px 11px;font-size:13px}
.ed-ctrl .lbl{font-weight:700;min-width:84px}
.ed-foot{display:flex;align-items:center;gap:12px;margin-top:18px;border-top:1px solid var(--line);padding-top:14px}
.ov{display:flex;align-items:center;gap:12px;background:var(--panel2);border-radius:10px;padding:10px;margin-bottom:8px}
.ov img{width:54px;height:96px;object-fit:contain;background:repeating-conic-gradient(#333 0 25%,#222 0 50%) 0 0/12px 12px;border-radius:6px}
.ov .nm{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
select{background:#0f1012;border:1px solid var(--line);color:var(--text);border-radius:8px;padding:8px}
.plan .it .btn{padding:7px 12px;font-size:13px}
.kw-res{margin-top:16px}.kw-player{display:none;margin:12px 0}.kw-player video{width:100%;max-height:46vh;background:#000;border-radius:10px}
.mt{display:flex;gap:14px;align-items:flex-start;padding:12px;border-radius:10px;background:var(--panel2);margin-bottom:8px}
.mt .tm{font:700 14px Consolas,monospace;color:var(--acc);min-width:74px;padding-top:2px}
.mt .tx{flex:1;min-width:0;color:#d6d7db;font-size:14px}.mt .tx mark{background:var(--acc);color:#111;border-radius:3px;padding:0 2px;font-weight:700}
.mt .bt{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}.mt .btn{padding:7px 11px;font-size:13px}
.mt .made{font-size:12px;color:#9ee6bd}
</style></head><body>
<header>
  <div class="brand"><span class="dot"></span>Peanut Clipper</div>
  <nav>
    <button data-t="make" class="on">Make Shorts</button>
    <button data-t="review">Review<span class="badge" id="nPending"></span></button>
    <button data-t="upload">Approved<span class="badge" id="nApproved"></span></button>
    <button data-t="settings">Settings</button>
    <button data-t="layout">Layouts &amp; Banners</button>
  </nav>
  <div class="hw"><button class="pill upd" id="pUpd" style="display:none">Update available</button><span class="pill" id="pGpu">CPU</span><span class="pill" id="pAuto">Auto: off</span>
    <button class="pill" id="quit" title="Close Peanut Clipper">Quit</button></div>
</header>
<main>

<section id="make" class="on">
  <h2>Make Shorts</h2><p class="sub">Paste a finished stream and the app finds the best moments, cuts them into Shorts, and puts them in Review.</p>
  <div class="row" style="margin:-8px 0 16px"><span class="mute">Layout for new Shorts</span><select id="mkLayout" style="min-width:220px"></select>
    <button class="link" onclick="show('layout')">edit layouts</button></div>
  <div class="card">
    <h3>From a stream</h3>
    <div class="row">
      <input class="big" type="text" id="url" placeholder="Paste a YouTube stream link (from his channel's Live tab)">
      <button class="btn main" id="go">Make Shorts</button>
    </div>
    <div class="row" style="margin-top:12px">
      <label class="toggle tiny"><input type="checkbox" id="part"> Only use part of the stream</label>
      <span id="partBox" style="display:none" class="row tiny">from <input type="text" class="small" id="from" value="1:00:00"> to <input type="text" class="small" id="to" value="2:00:00"></span>
    </div>
  </div>
  <div class="card">
    <h3>Find by keywords</h3>
    <p class="tiny mute" style="margin:-4px 0 12px">Finds every time Peanut says these words (and when chat spams them). Separate words or phrases with commas.</p>
    <div class="row">
      <input class="big" type="text" id="kwUrl" placeholder="Stream link (leave empty to use the one above)">
    </div>
    <div class="row" style="margin-top:10px">
      <input class="big" type="text" id="kwWords" placeholder='e.g.  drive, use a blinker, red light'>
      <button class="btn main" id="kwGo">Search</button>
    </div>
    <div class="row tiny" style="margin-top:10px;gap:18px">
      <label class="toggle"><input type="checkbox" id="kwChat" checked> Also search chat</label>
      <label class="toggle"><input type="checkbox" id="kwSimilar" checked> Match similar words (drive &rarr; driving)</label>
      <label class="toggle"><input type="checkbox" id="kwPart"> Only part of the stream</label>
      <span id="kwPartBox" style="display:none" class="row">from <input type="text" class="small" id="kwFrom" value="1:00:00"> to <input type="text" class="small" id="kwTo" value="2:00:00"></span>
    </div>
    <p class="tiny mute" id="kwCpu" style="display:none;margin:10px 0 0">Heads up: speech is running on the CPU, so searching a full stream can take an hour or more. Try "Only part of the stream" first.</p>
    <div class="kw-res" id="kwRes" style="display:none">
      <div class="row"><b id="kwHead"></b><span style="margin-left:auto" class="tiny mute">Earlier searches</span><select id="kwPick"></select></div>
      <div class="kw-player" id="kwPlayer"><video id="kwVid" controls preload="none"></video></div>
      <div id="kwList" style="margin-top:12px"></div>
    </div>
  </div>
  <div class="card" id="jobCard" style="display:none">
    <div class="row"><h3 style="margin:0" id="jobTitle">Working...</h3><span style="margin-left:auto" class="mute" id="jobPct"></span></div>
    <div class="bar" id="bar"><i></i></div>
    <div class="row"><span id="jobLabel"></span>
      <span style="margin-left:auto" class="row"><button class="link" id="logBtn">Show details</button>
      <button class="btn" id="cancel" style="padding:8px 14px">Cancel</button></span></div>
    <pre class="log" id="log" style="display:none"></pre>
  </div>
  <div class="card">
    <h3>Other ways</h3>
    <div class="row">
      <button class="btn" id="goTwitch">Shorts from today's top Twitch clips</button>
      <button class="btn" id="goAuto">Check his channel for a new stream now</button>
    </div>
    <p class="tiny mute" id="autoInfo" style="margin:12px 0 0"></p>
  </div>
</section>

<section id="review">
  <h2>Review</h2><p class="sub">Watch each Short. Click <b>Edit</b> to move the start or end (see the whole stream around it), fix the title, then Approve or Reject.</p>
  <div class="grid" id="grid"></div>
</section>

<section id="upload">
  <h2>Approved</h2><p class="sub">Send each approved Short to Premiere to finish it yourself, or upload it to YouTube as it is.</p>
  <div class="card">
    <div class="row"><h3 style="margin:0">Export for Premiere</h3><span class="mute tiny" style="margin-left:auto">Raw horizontal clip, full quality, original frame rate, with a few extra seconds on each side.</span></div>
    <p class="tiny mute" style="margin:8px 0 12px">Saves to: <b id="expFolder"></b> &middot; <button class="link" onclick="show('settings')">change</button></p>
    <div class="row"><button class="btn main" id="goExportAll">Export all approved for Premiere</button><span class="tiny mute">Or use the Export button on a single Short below.</span></div>
  </div>
  <div class="card" id="ytSetup">
    <h3>Connect YouTube (one time)</h3>
    <ol class="steps">
      <li>Open <a href="https://console.cloud.google.com/apis/library/youtube.googleapis.com" target="_blank">Google Cloud: YouTube Data API v3</a>, create a project if asked, and click <b>Enable</b>.</li>
      <li>Go to <a href="https://console.cloud.google.com/auth/audience" target="_blank">Audience</a>: choose External, then add your Google email under <b>Test users</b>.</li>
      <li>Go to <a href="https://console.cloud.google.com/auth/clients" target="_blank">Clients</a> &rarr; <b>Create client</b> &rarr; type <b>Desktop app</b> &rarr; Create &rarr; <b>Download JSON</b>.</li>
      <li>Pick that downloaded file here:</li>
    </ol>
    <input type="file" id="secret" accept=".json,application/json"> <span id="secretMsg" class="tiny"></span>
  </div>
  <div class="card">
    <div class="row"><h3 style="margin:0">Approved Shorts</h3><span class="mute tiny" id="ytState" style="margin-left:auto"></span></div>
    <div class="plan" id="plan"></div>
    <div class="row"><button class="btn main" id="goUpload">Upload all to YouTube &amp; schedule</button>
    <span class="tiny mute">The first time, a Google window opens: pick the <b>BurntPeanutXD</b> channel.</span></div>
  </div>
</section>

<section id="settings">
  <h2>Settings</h2><p class="sub">Changes apply to the next Shorts you make.</p>
  <div class="card"><h3>App version &amp; updates</h3>
    <div class="row"><span>Installed: <b id="vCur"></b></span><span class="mute" id="vState"></span>
      <span style="margin-left:auto" class="row"><button class="btn" id="vCheck">Check for updates</button><button class="btn main" id="vUpdate" style="display:none">Update now</button></span></div>
    <pre class="notes" id="vNotes" style="display:none"></pre>
    <p class="tiny mute" style="margin:10px 0 0">Updates only replace the app itself. Your settings, layout, banners, YouTube login, downloads and Shorts are kept.</p>
  </div>
  <div class="card"><h3>Nightly auto mode</h3>
    <div class="set">
      <label class="k">Turn on</label><label class="toggle"><input type="checkbox" id="s_auto_enabled"> Every night, make Shorts from his newest finished stream</label>
      <label class="k">Time</label><div><input type="time" id="s_auto_time"> <span class="tiny mute">Your PC can be asleep - it wakes up for it. If it's off, it runs next time you turn it on.</span></div>
      <label class="k">His YouTube streams page</label><input type="text" class="big" id="s_channel_url">
      <label class="k">Also do top Twitch clips</label><label class="toggle"><input type="checkbox" id="s_auto_twitch_clips"> needs the Twitch keys below</label>
    </div>
  </div>
  <div class="card"><h3>Shorts</h3>
    <div class="set">
      <label class="k">Shorts per stream</label><input type="number" min="1" max="40" class="small" id="s_shorts_per_stream">
      <label class="k">Captions</label><label class="toggle"><input type="checkbox" id="s_captions"> Burn word-by-word captions into the video</label>
      <label class="k">Posting times (LA time)</label><input type="text" id="s_schedule_times" placeholder="11:45, 16:30, 20:15">
    </div>
  </div>
  <div class="card"><h3>Saved keywords</h3>
    <div class="set">
      <label class="k">Words to look for in every stream</label><input type="text" class="big" id="s_saved_keywords" placeholder="e.g. use a blinker, red light">
      <label class="k">Max extra Shorts per stream</label><input type="number" min="1" max="20" class="small" id="s_saved_keywords_max">
      <label class="k">Seconds before / after a match</label><div><input type="number" min="0" max="120" class="small" id="s_search_lead_sec"> / <input type="number" min="0" max="120" class="small" id="s_search_tail_sec"></div>
    </div>
    <p class="tiny mute" style="margin:12px 0 0">When set, every stream you clip (and the nightly run) also listens to the whole stream for these words and adds Shorts for them. Adds a few minutes per stream on your graphics card.</p>
  </div>
  <div class="card"><h3>Premiere export</h3>
    <div class="set">
      <label class="k">Export folder</label><input type="text" class="big" id="s_export_folder" placeholder="e.g. C:\Users\Batman\Freelance\Smear Frame Studios\Frame Drip X\BurntPeanut XD\RAW CLIPS">
      <label class="k">Extra seconds each side</label><input type="number" min="0" max="30" class="small" id="s_export_handles_sec">
      <label class="k">Also copy the vertical Short</label><label class="toggle"><input type="checkbox" id="s_export_vertical_too"> Put the app's vertical version next to the raw clip</label>
      <label class="k">Frame rate of the app's Shorts</label><select id="s_output_fps"><option value="60">60 fps</option><option value="30">30 fps</option></select>
    </div>
  </div>
  <div class="card"><h3>Auto-delete</h3>
    <div class="set">
      <label class="k">Downloaded streams</label><label class="toggle"><input type="checkbox" id="s_delete_source"> Delete once every Short from it is rejected, uploaded or exported</label>
      <label class="k">...or after this many days</label><div><input type="number" min="1" max="30" class="small" id="s_keep_source_days"> <span class="tiny mute">the full stream is kept until then so you can re-cut Shorts</span></div>
      <label class="k">Rejected Shorts</label><label class="toggle"><input type="checkbox" id="s_delete_rejected"> Delete when I click Reject</label>
      <label class="k">Uploaded Shorts</label><label class="toggle"><input type="checkbox" id="s_delete_uploaded"> Delete once they're on YouTube</label>
    </div>
  </div>
  <div class="card"><h3>Trim editor</h3>
    <div class="set">
      <label class="k">Minutes to convert for editing</label><div><select id="s_edit_window_min"><option value="4">4 min</option><option value="6">6 min</option><option value="10">10 min</option><option value="20">20 min</option><option value="30">30 min</option></select> <span class="tiny mute">Only for streams your graphics card can't play smoothly (AV1). Centred on the Short; more minutes = more room to widen it, but a longer wait.</span></div>
    </div>
  </div>
  <div class="card"><h3>Speed</h3>
    <div class="set">
      <label class="k">Use my graphics card</label><label class="toggle"><input type="checkbox" id="s_use_gpu"> Faster, and keeps your CPU free</label>
      <label class="k">Status</label><div><span id="hwInfo"></span> <button class="link" id="hwTest">Test again</button></div>
    </div>
    <p class="tiny mute" style="margin:12px 0 0">Jobs always run at low priority, so games and other programs come first.</p>
  </div>
  <div class="card"><h3>Twitch (optional)</h3>
    <div class="set">
      <label class="k">Client ID</label><input type="text" id="s_twitch_client_id">
      <label class="k">Client Secret</label><input type="password" id="s_twitch_client_secret">
    </div>
    <p class="tiny mute" style="margin:12px 0 0">Free at <a href="https://dev.twitch.tv/console/apps" target="_blank">dev.twitch.tv/console/apps</a> &rarr; Register Your Application (Category: Other, redirect URL http://localhost).</p>
  </div>
  <div class="row"><button class="btn main" id="save">Save settings</button><span id="saveMsg" class="mute"></span></div>
</section>

<section id="layout">
  <h2>Layouts &amp; Banners</h2><p class="sub">Save a layout for each kind of stream (his cam sits in different spots in different games). Pick one when you make Shorts, or switch a single Short in the editor. Changes save by themselves.</p>
  <div class="card">
    <div class="row"><b>Layout</b><select id="lySel" style="min-width:220px"></select><span class="pill good" id="lyDef">default</span>
      <span style="margin-left:auto" class="row"><button class="btn" id="lyNew">+ New</button><button class="btn" id="lyDup">Duplicate</button><button class="btn" id="lyRen">Rename</button><button class="btn" id="lyMkDef">Make default</button><button class="btn no" id="lyDel">Delete</button></span></div>
  </div>
  <div class="card"><h3>Frame to design on</h3>
    <div class="row"><input class="big" type="text" id="fUrl" placeholder="Paste a stream link (the kind of stream this layout is for)">
      <span class="tiny mute">at</span><input type="text" class="small" id="fAt" value="1:00:00">
      <button class="btn main" id="goFrame">Grab frame</button></div>
  </div>
  <div class="card" id="calCard">
    <div class="row" style="margin-bottom:14px"><h3 style="margin:0" id="lyTitle">Layout</h3>
      <span style="margin-left:auto" class="seg" id="lyMode"><button data-m="stack">Peanut over gameplay</button><button data-m="single">Gameplay only</button><button data-m="blurfit">Whole stream</button></span></div>
    <div class="cal">
      <div class="stage" id="stage"><img id="cimg" draggable="false"><div class="nofr" id="noFrame">Grab a frame above to draw the boxes</div>
        <div class="box av" id="b_avatar"></div><div class="box gp" id="b_gameplay"></div></div>
      <div class="side">
        <div id="whichBox">
          <label class="toggle"><input type="radio" name="which" value="avatar" checked> <b style="color:#ff4fb3">Peanut box</b> <span class="tiny mute">(top)</span></label>
          <label class="toggle"><input type="radio" name="which" value="gameplay"> <b style="color:#3fa9ff" id="gpLabel">Gameplay box</b> <span class="tiny mute" id="gpHint">(bottom)</span></label>
          <p class="tiny mute" style="margin:6px 0 0">Drag on the frame to draw the selected box. Drag inside it to move it.</p>
          <label class="tiny mute">Zoom <input type="range" id="zoom" min="5" max="100" step="1" style="width:100%"></label>
        </div>
        <label class="tiny mute" id="thWrap">Peanut panel height <input type="range" id="th" min="480" max="1300" step="10" style="width:100%"></label>
        <canvas id="prev" width="540" height="960"></canvas>
        <div><div class="tiny mute" style="margin-bottom:4px">Banners on this layout</div><div id="lyBanners" class="tiny"></div></div>
        <span id="layMsg" class="tiny mute"></span>
      </div>
    </div>
  </div>
  <div class="card"><h3>Banner files</h3>
    <p class="tiny mute" style="margin:0 0 12px">Add your banners as <b>transparent PNGs</b> (or a video with transparency for animated ones). Easiest: in Premiere, turn off every track except your banners, export one frame of the 1080&times;1920 sequence as a PNG with transparency, and choose <b>Full frame</b>. Tick which banners each layout uses above.</p>
    <div id="ovList"></div>
    <div class="row"><input type="file" id="ovFile" accept=".png,.webp,.mov,.webm,.mp4"><span id="ovMsg" class="tiny mute"></span></div>
  </div>
</section>

<div class="modal" id="ed"><div class="ed-win">
  <div class="ed-top"><h3 id="edTitle">Edit Short</h3><span class="mute tiny" id="edLen"></span><button class="btn" style="margin-left:auto" id="edClose">Close</button></div>
  <div class="ed-body">
    <div class="ed-main">
      <video id="edSrc" preload="metadata" controls></video>
      <div class="tl" id="tl"><div class="orig" id="tlOrig"></div><div class="sel" id="tlSel"></div><div class="h" id="hIn"></div><div class="h" id="hOut"></div><div class="ph" id="tlPh"></div></div>
      <div class="ed-ctrl">
        <div class="grp"><span class="lbl">Start <span id="vIn" class="mute"></span></span>
          <button class="btn" data-n="in,-5">-5s</button><button class="btn" data-n="in,-1">-1s</button><button class="btn" data-n="in,ph">Set at playhead</button><button class="btn" data-n="in,1">+1s</button><button class="btn" data-n="in,5">+5s</button></div>
        <div class="grp"><span class="lbl">End <span id="vOut" class="mute"></span></span>
          <button class="btn" data-n="out,-5">-5s</button><button class="btn" data-n="out,-1">-1s</button><button class="btn" data-n="out,ph">Set at playhead</button><button class="btn" data-n="out,1">+1s</button><button class="btn" data-n="out,5">+5s</button></div>
      </div>
      <div class="row" style="margin-top:12px"><button class="btn" id="edPlaySel">&#9654; Play selection</button><button class="btn" id="edPlayPre">&#9654; Play 15s before it</button>
        <button class="btn" id="edWider">Show more of the stream</button><button class="btn" id="edReset">Reset</button></div>
    </div>
    <div class="ed-side"><div class="tiny mute" style="margin-bottom:6px">Current Short</div><video id="edShort" controls preload="none"></video></div>
  </div>
  <div class="ed-foot"><span class="tiny mute" id="edNote">Drag the yellow handles, or click the bar to jump there. Shorts can be up to 3 minutes.</span>
    <span style="margin-left:auto" class="row"><span class="tiny mute">Layout</span><select id="edLayout"></select>
    <button class="btn main" id="edSave">Update Short</button></span></div>
</div></div>
</main>
<div class="toast" id="toast"></div>
<div class="cover" id="cover"><div class="spin"></div><h2 id="coverT">Updating...</h2><div class="mute" id="coverM"></div></div>

<script>
const $=id=>document.getElementById(id);
let S=null, lastJobKey=null, logOpen=false;
function esc(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function toast(msg){const t=$('toast');t.innerHTML=msg;t.style.display='block';clearTimeout(t._h);t._h=setTimeout(()=>t.style.display='none',6000)}
async function api(path,body){
  const r=await fetch(path,body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:typeof body==='string'?body:JSON.stringify(body)});
  let j={};try{j=await r.json()}catch(e){}
  if(!r.ok){toast(esc(j.error||'Something went wrong'));throw new Error(j.error)}
  return j;
}
// tabs
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>show(b.dataset.t));
function show(t){document.querySelectorAll('nav button').forEach(x=>x.classList.toggle('on',x.dataset.t===t));
  document.querySelectorAll('section').forEach(s=>s.classList.toggle('on',s.id===t));
  if(t==='review')loadClips(); if(t==='upload')loadPlan(); if(t==='settings')fillSettings(); if(t==='layout')initLayout();}

// ---------- state polling ----------
let down=0, quitting=false, reloadWhenBack=false;
async function poll(){
  try{const r=await fetch('/api/state',{cache:'no-store'});S=await r.json();
    if(reloadWhenBack){location.reload();return}down=0}
  catch(e){down++;if(!quitting&&down>2){cover('Reconnecting...','If you closed Peanut Clipper, open it again from the Desktop icon.');reloadWhenBack=true}return}
  drawUpdate(S.update);
  const c=S.counts;$('nPending').textContent=c.pending||'';$('nApproved').textContent=c.approved||'';
  const g=S.hw.gpu_speech||S.hw.gpu_video, on=S.settings.use_gpu&&g;
  $('pGpu').textContent=on?'GPU: on':'CPU';$('pGpu').classList.toggle('good',!!on);
  $('pAuto').textContent=S.settings.auto_enabled?('Auto: '+fmtTime(S.settings.auto_time)):'Auto: off';$('pAuto').classList.toggle('good',!!S.settings.auto_enabled);
  const last=S.auto.last;$('autoInfo').textContent=(S.settings.auto_enabled?`Auto mode runs every night at ${fmtTime(S.settings.auto_time)}.`:'Auto mode is off (turn it on in Settings).')+(last?` Last run: ${last.time.replace('T',' ')}${last.made?' - made new Shorts':' - nothing new'}.`:'');
  drawJob(S.job);
}
function fmtTime(t){if(!t)return'';let[h,m]=t.split(':').map(Number);const ap=h>=12?'PM':'AM';h=h%12||12;return `${h}:${String(m).padStart(2,'0')} ${ap}`}
function drawJob(j){
  const card=$('jobCard');if(!j.kind){card.style.display='none';return}
  card.style.display='block';
  const titles={syncfix:'Converting the stream',search:'Searching for keywords',fromsearch:'Cutting a match',rerender:'Re-cutting a Short',export:'Exporting for Premiere',vod:'Making Shorts',clips:'Twitch top clips',upload:'Uploading',auto:'Auto mode',frame:'Grabbing a frame',hwtest:'Graphics card test'};
  $('jobTitle').textContent=(titles[j.kind]||'Working')+(j.running?'...':'');
  $('jobPct').textContent=j.running?j.pct+'%':'';
  $('bar').className='bar'+(j.ok===false?' err':(j.ok?' done':''));$('bar').firstElementChild.style.width=(j.ok?100:j.pct)+'%';
  $('jobLabel').textContent=j.label+(j.queued?` (${j.queued} waiting in line)`:'');$('cancel').style.display=j.running?'':'none';
  ['go','kwGo','goTwitch','goAuto','goUpload','goFrame','hwTest'].forEach(id=>$(id).disabled=j.running);
  if(logOpen){$('log').textContent=j.log.join('\n');}
  const key=j.kind+':'+j.ok;
  if(!j.running&&j.ok!==null&&lastJobKey&&lastJobKey!==key){
    if(j.ok&&['vod','clips','auto'].includes(j.kind)){toast(`<b>${esc(j.label)}</b><br><button class="link" onclick="show('review')">Go to Review</button>`)}
    if(j.ok&&j.kind==='frame'){initLayout(true)}
    if(j.ok&&j.kind==='upload'){loadPlan()}
    if(j.ok&&j.kind==='export'){toast('<b>Exported for Premiere.</b><br><span class="tiny">'+esc(S.settings.export_folder||S.default_export)+'</span>');loadPlan()}
    if(j.ok&&j.kind==='search'){loadSearches(true)}
    if(j.kind==='fromsearch'){if(KW)openSearch(KW.sid,true);
      if(j.ok&&S.last_made&&!S.last_made.export){api('/api/clips').then(cs=>{const c=cs.find(x=>x.job===S.last_made.job&&x.id===S.last_made.id);if(c)openEditor(c)})}
      if(j.ok&&S.last_made&&S.last_made.export)toast('<b>Exported for Premiere.</b><br><span class="tiny">'+esc(S.settings.export_folder||S.default_export)+'</span>')}
    if(j.kind==='syncfix'){if(j.ok&&pendingEdit){const c=pendingEdit;pendingEdit=null;openEditor(c)}
      if(j.ok&&pendingPreview!==null&&KW){const i=pendingPreview;pendingPreview=null;openSearch(KW.sid).then(()=>{const b=document.querySelector(`[data-a=play][data-i="${i}"]`);if(b)b.click()})}}
    if(j.kind==='rerender'){const wasSaving=edSaving;edSaving=false;$('edSave').disabled=false;$('edSave').textContent='Update Short';
      if(j.ok){toast('Short updated.');if(wasSaving)closeEditor();loadClips()}}
    if(!j.ok){toast('<b>Stopped:</b> '+esc(j.label)+'<br><span class="tiny">Click "Show details" on the Make Shorts tab for the full log.</span>')}
  }
  lastJobKey=j.running?'running':key;
}
$('logBtn').onclick=()=>{logOpen=!logOpen;$('log').style.display=logOpen?'block':'none';$('logBtn').textContent=logOpen?'Hide details':'Show details';if(S)drawJob(S.job)};
$('cancel').onclick=()=>api('/api/cancel',{}).then(poll);
$('part').onchange=e=>$('partBox').style.display=e.target.checked?'inline-flex':'none';
$('go').onclick=async()=>{const body={kind:'vod',url:$('url').value,layout:$('mkLayout').value};if($('part').checked){body.from=$('from').value;body.to=$('to').value}
  await api('/api/run',body);lastJobKey='running';poll()};
$('goTwitch').onclick=async()=>{await api('/api/run',{kind:'clips',layout:$('mkLayout').value});lastJobKey='running';poll()};
$('goAuto').onclick=async()=>{await api('/api/run',{kind:'auto'});lastJobKey='running';poll()};

// ---------- updates / quit ----------
function cover(t,m){$('coverT').textContent=t;$('coverM').textContent=m||'';$('cover').classList.add('on')}
// "What's new": **bold** shows bold, and the few words before a colon on each line are bold too
function notesHtml(t){return esc(t.replace(/^## /gm,'Version ')).split('\n').map(l=>{
  l=l.replace(/\*\*(.+?)\*\*/g,'<b>$1</b>');
  return /<b>/.test(l)?l:l.replace(/^(\s*[-•]\s*)([^:<]{1,40}?:)(\s)/,(m,a,b,c)=>b.trim().split(/\s+/).length<=5?a+'<b>'+b+'</b>'+c:m)}).join('\n')}
function drawUpdate(u){
  $('pUpd').style.display=u.available&&!u.busy?'':'none';
  $('vCur').textContent=u.current||'';
  $('vState').textContent=u.busy?u.msg:u.after_job?'Updates by itself when the current job finishes':(u.available?`Version ${u.latest} is available`:(u.latest?'You have the latest version':(u.error?'Couldn\'t reach GitHub - check your internet':'')));
  $('vUpdate').style.display=u.available&&!u.busy&&!u.after_job?'':'none';
  $('vNotes').style.display=u.available&&u.notes?'block':'none';$('vNotes').innerHTML=notesHtml(u.notes||'');
  if(u.busy){cover('Updating Peanut Clipper...',u.msg);reloadWhenBack=true}
  else if(u.msg&&u.msg.startsWith('Update failed')){$('cover').classList.remove('on');reloadWhenBack=false;toast(esc(u.msg))}
}
$('pUpd').onclick=()=>show('settings');
$('vCheck').onclick=async()=>{await api('/api/check_update',{});$('vState').textContent='Checking...';setTimeout(poll,2500)};
$('vUpdate').onclick=async()=>{const r=await api('/api/update',{});
  if(r.after_job){toast('<b>Update in line:</b> it updates by itself when the current job finishes.');poll();return}
  cover('Updating Peanut Clipper...','Downloading...');reloadWhenBack=true};
$('quit').onclick=async()=>{if(S&&S.job&&S.job.running&&!confirm('A job is still running. Quit anyway? It will be stopped.'))return;
  quitting=true;await fetch('/api/quit',{method:'POST',body:'{}'}).catch(()=>{});
  cover('Peanut Clipper is closed','You can close this tab. Open it again from the Desktop icon.');document.querySelector('.spin').style.display='none'};

// ---------- keyword search ----------
let KW=null, pendingPreview=null;
$('kwPart').onchange=e=>$('kwPartBox').style.display=e.target.checked?'inline-flex':'none';
$('kwGo').onclick=async()=>{const url=($('kwUrl').value||$('url').value).trim();
  const body={kind:'search',url,words:$('kwWords').value,chat:$('kwChat').checked,exact:!$('kwSimilar').checked,layout:$('mkLayout').value};
  if($('kwPart').checked){body.from=$('kwFrom').value;body.to=$('kwTo').value}
  await api('/api/run',body);lastJobKey='running';poll()};
async function loadSearches(openNewest){
  const list=await api('/api/searches');const sel=$('kwPick');
  sel.innerHTML=list.map(x=>`<option value="${x.sid}">${esc(x.words)} (${x.count}) - ${x.created.replace('T',' ').slice(0,16)}</option>`).join('');
  if(!list.length)return;if(openNewest||!KW)openSearch(list[0].sid);
}
$('kwPick').onchange=()=>openSearch($('kwPick').value);
const T=t=>{t=Math.max(0,Math.floor(t));return Math.floor(t/3600)+':'+String(Math.floor(t%3600/60)).padStart(2,'0')+':'+String(t%60).padStart(2,'0')};
async function openSearch(sid,keepPlayer){
  KW=await api('/api/search?sid='+encodeURIComponent(sid));$('kwRes').style.display='block';$('kwPick').value=sid;
  $('kwHead').textContent=`${KW.matches.length} match${KW.matches.length===1?'':'es'} for: ${KW.queries.join(', ')}`;
  if(!keepPlayer){$('kwPlayer').style.display='none';$('kwVid').pause()}
  const box=$('kwList');
  if(!KW.matches.length){box.innerHTML='<div class="mute">No matches. Try fewer or shorter words, or turn on "Match similar words".</div>';return}
  box.innerHTML=KW.matches.map(m=>`<div class="mt"><div class="tm">${T(m.t+KW.offset)}</div>
    <div class="tx"><div class="chips" style="margin-bottom:4px">${m.queries.map(q=>`<span class="chip">${m.kind==='chat'?'chat: ':''}${esc(q)}</span>`).join('')}${m.made?`<span class="made">&#10003; ${m.made==='exported'?'exported':'made into a Short'}</span>`:''}</div>
    ${esc(m.text).replace(/\[\[(.+?)\]\]/g,'<mark>$1</mark>')}</div>
    <div class="bt"><button class="btn" data-a="play" data-i="${m.i}">&#9654; Preview</button><button class="btn main" data-a="short" data-i="${m.i}">Make Short</button><button class="btn" data-a="export" data-i="${m.i}">Export for Premiere</button></div></div>`).join('');
  box.querySelectorAll('[data-a]').forEach(b=>b.onclick=async()=>{const m=KW.matches.find(x=>x.i==b.dataset.i);
    if(!KW.source_available){toast('The stream for this search was deleted. Run the search again to re-download it.');return}
    if(b.dataset.a==='play'&&KW.needs_sync){pendingPreview=m.i;await api('/api/run',{kind:'syncfix',sid:KW.sid});lastJobKey='running';
      toast('Converting this stream so it plays in sync (one time, a few minutes). Preview starts by itself when it\'s done.');poll();return}
    if(b.dataset.a==='play'){const v=$('kwVid');$('kwPlayer').style.display='block';
      if(!v.src.endsWith('/search_source/'+KW.sid)){v.preload='auto';v.src='/search_source/'+KW.sid;v.load()}
      const go=()=>{v.currentTime=Math.max(0,m.t-8);v.play()};if(v.readyState>0)go();else v.addEventListener('loadedmetadata',go,{once:true});
      $('kwPlayer').scrollIntoView({behavior:'smooth',block:'center'});return}
    const r=await api('/api/run',{kind:'fromsearch',sid:KW.sid,idx:m.i,export:b.dataset.a==='export',layout:$('mkLayout').value});lastJobKey='running';if(r.queued)toast('<b>In line:</b> this match is cut when the current job finishes.');poll()});
}

// ---------- review ----------
async function loadClips(){
  const data=await api('/api/clips');const grid=$('grid');grid.innerHTML='';
  if(!data.length){grid.innerHTML='<div class="empty" style="grid-column:1/-1">Nothing waiting for review.</div>';return}
  for(const c of data){
    const el=document.createElement('div');el.className='clip';
    el.innerHTML=`<video controls preload="none" poster="/media/${c.job}/${c.poster}" src="/media/${c.job}/${c.file}"></video>
      <div class="b"><input type="text" value="${esc(c.title)}">
      <div class="chips"><span class="chip s">score ${c.score}</span><span class="chip">${c.length}s</span>${c.reasons.map(r=>`<span class="chip">${esc(r)}</span>`).join('')}</div>
      <div class="act"><button class="btn ed">&#9986; Edit</button><button class="btn ok">Approve</button><button class="btn no">Reject</button></div></div>`;
    const send=async st=>{await api('/api/decide',{job:c.job,id:c.id,status:st,title:el.querySelector('input').value});el.remove();poll();
      if(!grid.querySelector('.clip'))grid.innerHTML='<div class="empty" style="grid-column:1/-1">All done. Head to Upload to schedule the approved ones.</div>'};
    el.querySelector('.ok').onclick=()=>send('approved');el.querySelector('.no').onclick=()=>send('rejected');
    el.querySelector('.ed').onclick=()=>openEditor(c);
    grid.appendChild(el);
  }
}

// ---------- upload ----------
async function loadPlan(){
  if(!S)await poll();
  $('ytSetup').style.display=S.youtube.secret?'none':'block';
  $('ytState').textContent=S.youtube.token?'YouTube connected':(S.youtube.secret?'Google will ask you to sign in on first upload':'');
  const plan=await api('/api/plan');const box=$('plan');
  box.innerHTML=plan.length?plan.map(p=>`<div class="it"><img src="${p.poster}"><div><b>${esc(p.title)}</b><div class="tiny mute">${p.length}s &middot; YouTube slot: ${esc(p.when)}</div></div>
    <span style="margin-left:auto"></span><button class="btn" data-ex="${p.job}|${p.id}">Export for Premiere</button></div>`).join(''):'<div class="mute">No approved Shorts yet.</div>';
  box.querySelectorAll('[data-ex]').forEach(b=>b.onclick=async()=>{const[job,id]=b.dataset.ex.split('|');const r=await api('/api/run',{kind:'export',job,id});lastJobKey='running';toast(r.queued?'<b>In line:</b> exports when the current job finishes.':'Exporting for Premiere...');poll()});
  $('expFolder').textContent=S.settings.export_folder||S.default_export;
  const busy=S.job&&S.job.running;
  $('goUpload').disabled=!plan.length||!S.youtube.secret||busy;$('goExportAll').disabled=!plan.length||busy;
}
$('secret').onchange=async e=>{const f=e.target.files[0];if(!f)return;
  try{await api('/api/client_secret',await f.text());$('secretMsg').textContent='Saved.';await poll();loadPlan()}catch(err){$('secretMsg').textContent=''}};
$('goExportAll').onclick=async()=>{const r=await api('/api/run',{kind:'export'});lastJobKey='running';toast(r.queued?'<b>In line:</b> exports when the current job finishes.':'Exporting for Premiere...');poll()};
$('goUpload').onclick=async()=>{await api('/api/run',{kind:'upload'});lastJobKey='running';show('make');poll()};

// ---------- settings ----------
const keys=['saved_keywords','saved_keywords_max','search_lead_sec','search_tail_sec','keep_source_days','edit_window_min','export_folder','export_handles_sec','export_vertical_too','output_fps','auto_enabled','auto_time','channel_url','auto_twitch_clips','shorts_per_stream','captions','delete_source','delete_rejected','delete_uploaded','use_gpu','twitch_client_id','twitch_client_secret','schedule_times'];
async function fillSettings(){
  if(!S)await poll();const st=S.settings;
  for(const k of keys){const el=$('s_'+k);if(!el)continue;
    if(el.type==='checkbox')el.checked=!!st[k];else if(k==='schedule_times'||k==='saved_keywords')el.value=(st[k]||[]).join(', ');else el.value=st[k]??''}
  $('hwInfo').innerHTML=`Speech: <b>${S.hw.gpu_speech?'graphics card':'CPU'}</b> &middot; Video: <b>${S.hw.gpu_video?'graphics card':'CPU'}</b>`;
}
$('save').onclick=async()=>{const body={};
  for(const k of keys){const el=$('s_'+k);if(!el)continue;
    if(el.type==='checkbox')body[k]=el.checked;else if(el.type==='number'||k==='output_fps'||k==='edit_window_min')body[k]=parseInt(el.value||'0');
    else if(k==='saved_keywords')body[k]=el.value.split(',').map(s=>s.trim()).filter(Boolean);
    else if(k==='schedule_times')body[k]=el.value.split(',').map(s=>s.trim()).filter(s=>/^\d{1,2}:\d{2}$/.test(s)).map(s=>s.padStart(5,'0'));else body[k]=el.value.trim()}
  const r=await api('/api/settings',body);$('saveMsg').textContent=r.message;await poll();fillSettings()};
$('hwTest').onclick=async()=>{await api('/api/run',{kind:'hwtest'});lastJobKey='running';show('make');poll()};

// ---------- layouts ----------
let LY=null, L=null, lyTimer=null;
const clone=o=>JSON.parse(JSON.stringify(o));
const newId=()=>'l'+Date.now().toString(36);
async function initLayout(fresh){
  if(!S||fresh)await poll();
  if(!LY||fresh===true)LY=clone(S.layouts);
  if(!L||!LY.layouts.find(x=>x.id===L.id))L=LY.layouts.find(x=>x.id===LY.default)||LY.layouts[0];
  else L=LY.layouts.find(x=>x.id===L.id);
  $('lySel').innerHTML=LY.layouts.map(l=>`<option value="${l.id}">${esc(l.name)}${l.id===LY.default?' (default)':''}</option>`).join('');
  $('lySel').value=L.id;$('lyDef').style.display=L.id===LY.default?'':'none';$('lyTitle').textContent=L.name;
  document.querySelectorAll('#lyMode button').forEach(b=>b.classList.toggle('on',b.dataset.m===L.mode));
  $('th').value=L.top_height;
  const hasFrame=S.has_frame;$('noFrame').style.display=hasFrame?'none':'flex';
  if(hasFrame&&(!$('cimg').src||fresh))$('cimg').src='/calib.jpg?'+Date.now();
  if(!hasFrame)$('cimg').removeAttribute('src');
  const m=L.mode;$('whichBox').style.display=m==='blurfit'?'none':'block';$('thWrap').style.display=m==='stack'?'block':'none';
  document.querySelector('[name=which][value=avatar]').parentElement.style.display=m==='stack'?'':'none';
  if(m==='single')document.querySelector('[name=which][value=gameplay]').checked=true;
  $('gpLabel').textContent=m==='single'?'Frame box':'Gameplay box';$('gpHint').textContent=m==='single'?'(fills the whole Short)':'(bottom)';
  renderLayoutBanners();syncZoom();drawCal();
  updateLayoutMenus();
}
function updateLayoutMenus(){
  if(!S)return;const src=LY||S.layouts;
  const opts=src.layouts.map(l=>`<option value="${l.id}">${esc(l.name)}${l.id===src.default?' (default)':''}</option>`).join('');
  for(const id of ['mkLayout','edLayout']){const el=$(id);if(!el)continue;const v=el.value;el.innerHTML=opts;
    el.value=src.layouts.some(l=>l.id===v)?v:src.default}
}
function saveLY(msg){clearTimeout(lyTimer);$('layMsg').textContent='Saving...';
  lyTimer=setTimeout(async()=>{await api('/api/layouts',LY);$('layMsg').textContent=msg||'Saved.';S.layouts=clone(LY);updateLayoutMenus()},500)}
$('lySel').onchange=()=>{L=LY.layouts.find(x=>x.id===$('lySel').value);initLayout()};
document.querySelectorAll('#lyMode button').forEach(b=>b.onclick=()=>{L.mode=b.dataset.m;initLayout();saveLY()});
$('lyNew').onclick=()=>{const name=prompt('Name for the new layout (e.g. "GTA", "ARC Raiders"):');if(!name)return;
  L={id:newId(),name:name.trim().slice(0,40),mode:'stack',top_height:760,banners:null,
     avatar:{x:.7,y:.5,w:.3,h:.5},gameplay:{x:.15,y:0,w:.7,h:1}};LY.layouts.push(L);initLayout();saveLY('Created "'+L.name+'".')};
$('lyDup').onclick=()=>{const c=clone(L);c.id=newId();c.name=(L.name+' copy').slice(0,40);LY.layouts.push(c);L=c;initLayout();saveLY('Duplicated.')};
$('lyRen').onclick=()=>{const name=prompt('New name:',L.name);if(!name)return;L.name=name.trim().slice(0,40);initLayout();saveLY('Renamed.')};
$('lyMkDef').onclick=()=>{LY.default=L.id;initLayout();saveLY('"'+L.name+'" is now the default.')};
$('lyDel').onclick=()=>{if(LY.layouts.length<2){toast('You need at least one layout.');return}
  if(!confirm('Delete the layout "'+L.name+'"? Shorts that used it switch to the default next time you update them.'))return;
  LY.layouts=LY.layouts.filter(x=>x.id!==L.id);if(LY.default===L.id)LY.default=LY.layouts[0].id;L=null;initLayout();saveLY('Deleted.')};
$('goFrame').onclick=async()=>{await api('/api/run',{kind:'frame',url:$('fUrl').value,at:$('fAt').value});lastJobKey='running';toast('Grabbing a frame... it appears here when it\'s ready.');poll()};
function renderLayoutBanners(){
  const list=(S&&S.settings.overlays)||[];const box=$('lyBanners');
  if(!list.length){box.innerHTML='<span class="mute">No banner files yet (add them below).</span>';return}
  const on=f=>L.banners==null?(list.find(o=>o.file===f).enabled!==false):L.banners.includes(f);
  box.innerHTML=list.map(o=>`<label class="toggle" style="margin:3px 0"><input type="checkbox" data-f="${esc(o.file)}" ${on(o.file)?'checked':''}> ${esc(o.file)}</label>`).join('');
  box.querySelectorAll('input').forEach(c=>c.onchange=()=>{L.banners=[...box.querySelectorAll('input:checked')].map(x=>x.dataset.f);drawCal();saveLY()});
}
const sel=()=>document.querySelector('[name=which]:checked').value;
document.querySelectorAll('[name=which]').forEach(r=>r.onchange=()=>syncZoom());
function syncZoom(){if(!L)return;const b=L[sel()];$('zoom').value=Math.round(b.w*100)}
$('zoom').oninput=()=>{const k=sel(),b=L[k],cx=b.x+b.w/2,cy=b.y+b.h/2,ar=b.h/b.w;
  let w=Math.min(1,+$('zoom').value/100),h=Math.min(1,w*ar);w=h/ar;
  L[k]={w,h,x:Math.min(1-w,Math.max(0,cx-w/2)),y:Math.min(1-h,Math.max(0,cy-h/2))};drawCal()};
$('zoom').onchange=()=>saveLY();$('th').oninput=()=>{L.top_height=+$('th').value;drawCal()};$('th').onchange=()=>saveLY();
function drawCal(){
  if(!L)return;const m=L.mode;
  for(const k of ['avatar','gameplay']){const b=L[k],e=$('b_'+k);
    const show=S&&S.has_frame&&(k==='gameplay'?m!=='blurfit':m==='stack');e.style.display=show?'block':'none';
    e.style.left=b.x*100+'%';e.style.top=b.y*100+'%';e.style.width=b.w*100+'%';e.style.height=b.h*100+'%'}
  const img=$('cimg'),c=$('prev'),x=c.getContext('2d'),W=img.naturalWidth,H=img.naturalHeight;
  x.fillStyle='#1a1b1f';x.fillRect(0,0,540,960);x.filter='none';
  const cover=(b,dy,dh)=>{let sx=b.x*W,sy=b.y*H,sw=b.w*W,sh=b.h*H;const r=540/dh;
    if(sw/sh>r){const nw=sh*r;sx+=(sw-nw)/2;sw=nw}else{const nh=sw/r;sy+=(sh-nh)/2;sh=nh}
    x.drawImage(img,sx,sy,sw,sh,0,dy,540,dh)};
  const top=L.top_height/1920*960;
  if(W&&img.src){
    if(m==='stack'){cover(L.avatar,0,top);cover(L.gameplay,top,960-top)}
    else if(m==='single'){cover(L.gameplay,0,960)}
    else{x.filter='blur(12px) brightness(0.8)';cover({x:0,y:0,w:1,h:1},0,960);x.filter='none';const h=540*H/W;x.drawImage(img,0,(960-h)/2,540,h)}
  }else{x.fillStyle='#6d717b';x.font='20px Segoe UI';x.textAlign='center';x.fillText('Preview appears here',270,480)}
  const seam=m==='stack'?top:m==='single'?480:(W?(960-540*H/W)/2:480);
  const list=(S&&S.settings.overlays)||[];
  for(const o of list){const on=L.banners==null?o.enabled!==false:L.banners.includes(o.file);
    if(!on||!/\.(png|webp|jpe?g)$/i.test(o.file))continue;
    let im=ovImgs[o.file];if(!im){im=ovImgs[o.file]=new Image();im.onload=()=>drawCal();im.src='/overlay/'+encodeURIComponent(o.file);continue}
    if(!im.complete||!im.naturalWidth)continue;
    if(o.position==='full'){x.drawImage(im,0,0,540,960);continue}
    const h=540*im.naturalHeight/im.naturalWidth,off=(o.offset||0)/2;
    x.drawImage(im,0,(o.position==='top'?0:o.position==='bottom'?960-h:seam-h/2)+off,540,h)}
}
$('cimg').onload=()=>drawCal();
let drag=null;const stage=$('stage');
const pos=e=>{const r=stage.getBoundingClientRect();return[Math.min(1,Math.max(0,(e.clientX-r.left)/r.width)),Math.min(1,Math.max(0,(e.clientY-r.top)/r.height))]};
stage.onmousedown=e=>{if(!S||!S.has_frame||L.mode==='blurfit')return;e.preventDefault();const p=pos(e),k=sel(),b=L[k];
  if(p[0]>=b.x&&p[0]<=b.x+b.w&&p[1]>=b.y&&p[1]<=b.y+b.h)drag={move:true,k,dx:p[0]-b.x,dy:p[1]-b.y};else drag={move:false,k,s:p}};
window.addEventListener('mousemove',e=>{if(!drag)return;const p=pos(e),b=L[drag.k];
  if(drag.move){b.x=Math.min(1-b.w,Math.max(0,p[0]-drag.dx));b.y=Math.min(1-b.h,Math.max(0,p[1]-drag.dy))}
  else L[drag.k]={x:Math.min(drag.s[0],p[0]),y:Math.min(drag.s[1],p[1]),w:Math.max(.03,Math.abs(p[0]-drag.s[0])),h:Math.max(.03,Math.abs(p[1]-drag.s[1]))};
  drawCal()});
window.addEventListener('mouseup',()=>{if(drag){drag=null;syncZoom();saveLY()}});

// ---------- trim editor ----------
let E=null, edSaving=false, tlDrag=null, pendingEdit=null;
const fmt=t=>{t=Math.max(0,t);const h=Math.floor(t/3600),m=Math.floor(t%3600/60),s=(t%60).toFixed(1);return (h?h+':'+String(m).padStart(2,'0'):m)+':'+String(s).padStart(4,'0')};
async function openEditor(c){
  const info=await api(`/api/clip_info?job=${encodeURIComponent(c.job)}&id=${encodeURIComponent(c.id)}`);
  if(!info.available){toast('The full stream for this Short was already deleted, so it can\'t be re-cut. (Settings &rarr; Auto-delete controls how long streams are kept.)');return}
  if(info.needs_sync){pendingEdit=c;await api('/api/run',{kind:'syncfix',job:c.job,id:c.id});lastJobKey='running';
    toast('<b>Getting the editor ready:</b> converting a few minutes around this Short (change how many in Settings). The editor opens by itself.');poll();return}
  // off = where the editor's video starts in the stream (only part of an AV1 stream is converted); E.* times are video times
  const off=info.offset||0;
  E={job:c.job,id:c.id,off,dur:info.duration,a:info.start-off,b:info.end-off,oa:info.start-off,ob:info.end-off,pad:60};
  setView();updateLayoutMenus();
  const src=(LY||S.layouts);$('edLayout').value=src.layouts.some(l=>l.id===info.layout)?info.layout:src.default;
  $('edTitle').textContent=c.title;$('edSrc').src=`/source/${c.job}/${c.id}`;
  $('edShort').src=`/media/${c.job}/${info.file}`;$('edShort').poster=`/media/${c.job}/${info.poster}`;
  $('ed').classList.add('on');
  $('edSrc').addEventListener('loadedmetadata',()=>{$('edSrc').currentTime=E.a},{once:true});
  drawTL();
}
function closeEditor(){$('ed').classList.remove('on');$('edSrc').pause();$('edSrc').removeAttribute('src');$('edSrc').load();$('edShort').pause();E=null}
$('edClose').onclick=closeEditor;
function setView(){E.vs=Math.max(0,Math.min(E.a,E.oa)-E.pad);E.ve=Math.min(E.dur,Math.max(E.b,E.ob)+E.pad)}
const X=t=>(t-E.vs)/(E.ve-E.vs)*100;
function drawTL(){
  if(!E)return;const tl=$('tl');tl.querySelectorAll('.tick').forEach(x=>x.remove());
  const span=E.ve-E.vs,step=span>400?60:span>150?30:span>60?10:5;
  for(let t=Math.ceil((E.vs+E.off)/step)*step-E.off;t<E.ve;t+=step){const d=document.createElement('div');d.className='tick';d.style.left=X(t)+'%';d.innerHTML=`<span>${fmt(t+E.off).replace(/\.\d$/,'')}</span>`;tl.prepend(d)}
  $('tlOrig').style.left=X(E.oa)+'%';$('tlOrig').style.width=(X(E.ob)-X(E.oa))+'%';
  $('tlSel').style.left=X(E.a)+'%';$('tlSel').style.width=(X(E.b)-X(E.a))+'%';
  $('hIn').style.left=X(E.a)+'%';$('hOut').style.left=X(E.b)+'%';
  const ph=$('edSrc').currentTime||E.a;$('tlPh').style.left=X(ph)+'%';
  $('vIn').textContent=fmt(E.a+E.off);$('vOut').textContent=fmt(E.b+E.off);
  const len=E.b-E.a;$('edLen').textContent=`${len.toFixed(1)}s long`+(Math.abs(E.a-E.oa)>.05||Math.abs(E.b-E.ob)>.05?' (changed)':'');
  $('edLen').style.color=len>180?'var(--no)':'';
}
function clampAB(){E.a=Math.max(0,Math.min(E.a,E.b-3));E.b=Math.min(E.dur,Math.max(E.b,E.a+3));
  if(E.a<E.vs||E.b>E.ve)setView();drawTL()}
document.querySelectorAll('[data-n]').forEach(b=>b.onclick=()=>{if(!E)return;const[w,v]=b.dataset.n.split(',');const ph=$('edSrc').currentTime;
  if(w==='in')E.a=v==='ph'?ph:E.a+(+v);else E.b=v==='ph'?ph:E.b+(+v);clampAB();$('edSrc').currentTime=w==='in'?E.a:Math.max(E.a,E.b-3)});
const tAt=e=>{const r=$('tl').getBoundingClientRect();return E.vs+(Math.min(1,Math.max(0,(e.clientX-r.left)/r.width)))*(E.ve-E.vs)};
$('hIn').onmousedown=e=>{tlDrag='in';e.stopPropagation();e.preventDefault()};
$('hOut').onmousedown=e=>{tlDrag='out';e.stopPropagation();e.preventDefault()};
$('tl').onmousedown=e=>{if(!E)return;$('edSrc').currentTime=tAt(e);drawTL()};
window.addEventListener('mousemove',e=>{if(!tlDrag||!E)return;const t=tAt(e);if(tlDrag==='in')E.a=t;else E.b=t;
  E.a=Math.max(0,Math.min(E.a,E.b-3));E.b=Math.min(E.dur,Math.max(E.b,E.a+3));$('edSrc').currentTime=tlDrag==='in'?E.a:E.b;drawTL()});
window.addEventListener('mouseup',()=>{if(tlDrag){tlDrag=null;if(E&&(E.a<E.vs+1||E.b>E.ve-1)){setView();drawTL()}}});
let stopAt=null;
$('edSrc').addEventListener('timeupdate',()=>{if(!E)return;if(stopAt!==null&&$('edSrc').currentTime>=stopAt){$('edSrc').pause();stopAt=null}drawTL()});
$('edPlaySel').onclick=()=>{$('edSrc').currentTime=E.a;stopAt=E.b;$('edSrc').play()};
$('edPlayPre').onclick=()=>{$('edSrc').currentTime=Math.max(0,E.a-15);stopAt=E.a+2;$('edSrc').play()};
$('edWider').onclick=()=>{E.pad=Math.min(E.pad*2.5,1800);setView();drawTL()};
$('edReset').onclick=()=>{E.a=E.oa;E.b=E.ob;E.pad=60;setView();drawTL();$('edSrc').currentTime=E.a};
$('edSave').onclick=async()=>{if(!E||edSaving)return;
  if(E.b-E.a>180&&!confirm('This is over 3 minutes, which is longer than YouTube allows for a Short. Make it anyway?'))return;
  edSaving=true;$('edSave').disabled=true;$('edSave').textContent='Updating...';$('edSrc').pause();
  try{const r=await api('/api/run',{kind:'rerender',job:E.job,id:E.id,start:E.a+E.off,end:E.b+E.off,layout:$('edLayout').value});
    if(r.queued){edSaving=false;$('edSave').disabled=false;$('edSave').textContent='Update Short';closeEditor();toast('<b>In line:</b> this Short updates when the current job finishes.');poll();return}
    lastJobKey='running';poll()}catch(e){edSaving=false;$('edSave').disabled=false;$('edSave').textContent='Update Short'}};

// ---------- banner files ----------
const ovImgs={};
function renderOverlays(){
  const list=(S&&S.settings.overlays)||[];const box=$('ovList');
  box.innerHTML=list.length?'':'<p class="tiny mute">No banners yet.</p>';
  list.forEach((o,i)=>{const isImg=/\.(png|webp|jpe?g)$/i.test(o.file);const d=document.createElement('div');d.className='ov';
    d.innerHTML=`${isImg?`<img src="/overlay/${encodeURIComponent(o.file)}">`:'<span class="pill">video</span>'}<span class="nm">${esc(o.file)}</span>
      <select>${[['full','Full frame (1080x1920)'],['top','Top'],['seam','Between peanut & gameplay'],['bottom','Bottom']].map(([v,t])=>`<option value="${v}" ${o.position===v?'selected':''}>${t}</option>`).join('')}</select>
      <label class="tiny mute">nudge px <input type="number" class="small" style="width:80px" value="${o.offset||0}"></label>
      <button class="btn no" style="padding:7px 12px">Remove</button>`;
    const [sel]=d.getElementsByTagName('select');const [num]=d.getElementsByTagName('input');
    sel.onchange=()=>{o.position=sel.value;saveOv(list)};num.onchange=()=>{o.offset=parseInt(num.value||'0');saveOv(list)};
    d.querySelector('.no').onclick=()=>{list.splice(i,1);
      for(const l of (LY||S.layouts).layouts)if(l.banners)l.banners=l.banners.filter(f=>f!==o.file);saveOv(list)};
    box.appendChild(d)});
  if(L){renderLayoutBanners();drawCal()}
}
async function saveOv(list){await api('/api/overlays',{overlays:list});if(LY)await api('/api/layouts',LY);await poll();renderOverlays()}
$('ovFile').onchange=async e=>{const f=e.target.files[0];if(!f)return;$('ovMsg').textContent='Uploading...';
  const r=await fetch('/api/overlay_upload?name='+encodeURIComponent(f.name),{method:'POST',body:f});
  $('ovMsg').textContent=r.ok?'Added.':'Upload failed.';e.target.value='';await poll();renderOverlays()};
const _show=show;show=function(t){_show(t);if(t==='layout')setTimeout(renderOverlays,300)};

poll().then(()=>{if(S){$('kwCpu').style.display=S.hw.gpu_speech&&S.settings.use_gpu?'none':'block';updateLayoutMenus()}});loadSearches();setInterval(poll,1500);
</script></body></html>"""
