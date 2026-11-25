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
nav button{background:none;border:0;color:var(--mute);font:inherit;font-weight:600;padding:0 14px;white-space:nowrap;cursor:pointer;border-bottom:3px solid transparent;height:100%}
@media(max-width:1500px){header{gap:12px;padding:0 16px}nav{gap:0}nav button{padding:0 9px;font-size:14px}}
@media(max-width:1250px){nav{overflow-x:auto;scrollbar-width:none}}
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
.clip .act{flex-wrap:wrap}.clip .act .colwrap{flex-basis:100%}.clip .act .colbtn{width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.empty{padding:70px 20px;text-align:center;color:var(--mute);border:1px dashed var(--line);border-radius:14px}
.plan{display:flex;flex-direction:column;gap:8px;margin:12px 0}
.plan .it{display:flex;gap:12px;align-items:center;background:var(--panel2);border-radius:10px;padding:8px}
.plan img{width:40px;height:71px;object-fit:cover;border-radius:6px;background:#000}
.plan .when{margin-left:auto;color:var(--acc);font-weight:700;white-space:nowrap}
.set{display:grid;grid-template-columns:260px 1fr;gap:14px 20px;align-items:center}
.set label.k{color:var(--mute)}
.toggle{display:flex;align-items:center;gap:10px;cursor:pointer}
#srcCard.over{border-color:var(--acc);background:#1f2026}
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
.toast{position:fixed;right:24px;bottom:24px;background:var(--panel2);border:1px solid var(--line);border-left:4px solid var(--acc);padding:14px 18px;border-radius:10px;display:none;max-width:420px;z-index:40}
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
.tl .sel{cursor:grab}.tl.moving,.tl.moving .sel{cursor:grabbing}
.tl{position:relative;height:64px;margin:14px 0 6px;background:#0c0d0f;border:1px solid var(--line);border-radius:10px;cursor:pointer;user-select:none;overflow:hidden}
.tl .tick{position:absolute;top:0;bottom:0;width:1px;background:#2a2d34}
.tl .tick span{position:absolute;top:2px;left:4px;font-size:11px;color:#6d717b;white-space:nowrap}
.tl .orig{position:absolute;top:44px;height:6px;background:#ffffff22;border-radius:3px}
.tl .sel{position:absolute;top:18px;bottom:8px;background:#ffc93c33;border:2px solid var(--acc);border-radius:6px}
.tl .h{position:absolute;top:12px;bottom:2px;width:14px;margin-left:-7px;background:var(--acc);border-radius:4px;cursor:ew-resize}
.tl .h::after{content:"";position:absolute;left:5px;top:16px;bottom:16px;width:4px;border-left:2px solid #111;border-right:2px solid #111}
.tl .mk{position:absolute;top:0;bottom:0;width:12px;margin-left:-6px;cursor:pointer;z-index:2}
.tl .mk::before{content:"";position:absolute;left:5px;top:0;bottom:0;width:2px;background:#3fa9ff}
.tl .mk::after{content:"";position:absolute;left:1px;top:0;border:5px solid transparent;border-top:7px solid #3fa9ff}
.tl .mk.hit::before,.tl .mk.hit::after{filter:brightness(1.6)}
.tl .ph{position:absolute;top:0;bottom:0;width:2px;background:#fff;pointer-events:none}
.ed-ctrl{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-top:6px}
.ed-ctrl .grp{display:flex;align-items:center;gap:6px}.ed-ctrl .btn{padding:7px 11px;font-size:13px}
.ed-ctrl .lbl{font-weight:700;min-width:84px}
.fr-wrap{margin-top:14px;border-top:1px solid var(--line);padding-top:12px}
.fr{display:flex;gap:16px;align-items:flex-start;margin-top:10px}
.fr-stage{position:relative;flex:1;min-width:0;user-select:none;cursor:crosshair}.fr-stage canvas{width:100%;display:block;border-radius:8px;background:#0c0d0f}
.fr-side{width:300px;flex:none;display:flex;flex-direction:column;gap:8px}
.fr-prev{display:flex;justify-content:center}.fr-prev canvas{width:150px;border-radius:8px;background:#000}
.sec-tl{position:relative;height:34px;margin:2px 0 6px;background:#0c0d0f;border:1px solid var(--line);border-radius:8px;user-select:none;overflow:hidden}
.sec-tl .pc{position:absolute;top:3px;bottom:3px;border-radius:5px;cursor:pointer;font-size:11px;font-weight:700;color:#111;padding:0 6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:28px;border:2px solid transparent}
.sec-tl .pc.normal{background:#3a3d46;color:#cfd1d6}.sec-tl .pc.closeup{background:#ff4fb3}.sec-tl .pc.gameplay{background:#3fa9ff}
.sec-tl .pc.on{border-color:#fff;box-shadow:0 0 0 2px var(--acc)}
.sec-tl .pc.nob{background-image:repeating-linear-gradient(45deg,#0003 0 6px,transparent 6px 12px)}
.sec-tl .cut{position:absolute;top:0;bottom:0;width:10px;margin-left:-5px;cursor:pointer;z-index:2}
.sec-tl .cut::before{content:"";position:absolute;left:4px;top:0;bottom:0;width:2px;background:#fff}
.sec-tl .sph{position:absolute;top:0;bottom:0;width:2px;background:#fff8;pointer-events:none}
.sec-tools{margin-top:12px;padding-top:12px;border-top:1px solid var(--line)}
.sec-tools .seg button{padding:7px 11px;font-size:13px}.sec-tools .btn{padding:7px 11px;font-size:13px}
.sec-box{display:flex;gap:14px;align-items:flex-start;margin-top:10px}
.sec-box .fr-stage{max-width:560px}
.ed-side .live{width:100%;aspect-ratio:9/16;border-radius:10px;background:#000;display:block}
.ed-side .btn{padding:7px 10px;font-size:13px;width:100%;margin-top:6px}
.cmp-head{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.ed-grid{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(280px,1fr);gap:16px}
.ed-player{position:relative;background:#000;border-radius:10px;overflow:hidden;aspect-ratio:16/9}
.ed-player video{position:absolute;inset:0;width:100%;height:100%;transform-origin:0 0}
.ed-ov{position:absolute;left:50%;bottom:9%;transform:translateX(-50%);background:rgba(10,10,12,.6);color:#fff;font:italic 900 clamp(16px,2.6vw,34px)/1.1 "Segoe UI",sans-serif;padding:6px 18px;border-radius:8px;display:none;max-width:84%;text-align:center;text-shadow:0 0 3px #000,0 0 3px #000}
.ed-empty{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#5a5d66;font-size:14px;pointer-events:none}
.ed-insp{background:var(--panel2);border-radius:12px;padding:14px;font-size:14px}
.ed-insp .k{color:var(--mute);font-size:12px;margin:10px 0 4px}.ed-insp input[type=text]{width:100%}
.ed-tl{position:relative;display:flex;gap:4px;margin-top:14px;padding:4px 0 8px;overflow-x:auto}
.blk{position:relative;flex:1 1 0;min-width:46px;height:66px;background:#2a2c33 center/cover;border:2px solid #3a3d46;border-radius:8px;cursor:grab;overflow:hidden;user-select:none}
.blk .lb{position:absolute;left:0;right:0;bottom:0;padding:1px 6px;font-size:11px;background:rgba(0,0,0,.7);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.blk .tg{position:absolute;top:3px;right:12px;font-size:10px;background:rgba(0,0,0,.7);border-radius:4px;padding:0 4px;color:var(--acc)}
.blk.sel{border-color:var(--acc)}.blk.over{outline:2px dashed var(--acc);outline-offset:2px}.blk.drag{opacity:.4}
.blk .h{position:absolute;top:0;bottom:0;width:9px;background:var(--acc);cursor:ew-resize;display:none;z-index:2}
.blk.sel .h{display:block}.blk .h.l{left:0}.blk .h.r{right:0}
.blk.add{flex:0 0 74px;border-style:dashed;display:flex;align-items:center;justify-content:center;color:var(--mute);cursor:pointer;background:none;font-weight:700}
.ed-ph{position:absolute;top:2px;bottom:6px;width:2px;background:#fff;pointer-events:none;box-shadow:0 0 0 1px #000;z-index:3}
.ed-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px}
.ed-add{background:var(--panel2);border-radius:12px;padding:14px;margin-top:12px}.ed-add video{width:100%;max-height:360px;background:#000;border-radius:8px;margin-top:8px}
.mono{font:700 14px Consolas,monospace}.btn.sm{padding:6px 10px;font-size:12px}

.cmp-bar{height:12px;flex:1;min-width:200px;background:#0f1012;border:1px solid var(--line);border-radius:99px;overflow:hidden}
.cmp-bar>i{display:block;height:100%;background:var(--acc)}.cmp-bar.done>i{background:var(--ok)}
.mo{display:flex;gap:12px;align-items:center;background:var(--panel2);border-radius:10px;padding:8px;margin-bottom:8px;border:2px solid transparent}
.mo.drag{opacity:.4}.mo.over{border-color:var(--acc)}.mo.on{border-color:var(--blue)}
.mo .num{font:700 14px Consolas,monospace;color:var(--mute);width:26px;text-align:right;cursor:grab}
.mo img{width:96px;height:54px;object-fit:cover;border-radius:6px;background:#000;flex:none}
.mo .tt{flex:1;min-width:0}.mo .tt b{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mo .btn{padding:6px 9px;font-size:12px}.mo .grp{display:flex;gap:4px;align-items:center}
.mo .grp .k{font-size:12px;color:var(--mute);margin-right:2px}
.cmp-player video{width:100%;max-height:48vh;background:#000;border-radius:10px;display:block}
.btn.added{color:#9ee6bd;border-color:#2fb36d}
.live-st{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:12px}
.live-st div{background:var(--panel2);border-radius:10px;padding:10px 12px}.live-st span{font-size:12px;color:var(--mute)}
.live-st b{display:block;font:700 18px Consolas,monospace;color:var(--acc)}
.rec-dot{width:12px;height:12px;border-radius:50%;background:#e5484d;display:inline-block;animation:recp 1.4s infinite}
@keyframes recp{50%{opacity:.35}}@media(prefers-reduced-motion:reduce){.rec-dot{animation:none}}
.btn.rec{background:#e5484d;border-color:#e5484d;color:#fff}
@media(max-width:700px){.live-st{grid-template-columns:repeat(2,minmax(0,1fr))}}
.tc{font:700 13px Consolas,monospace;color:var(--acc)}
.st-line{margin:8px 0 4px}.st-acts{display:flex;gap:6px;flex-wrap:wrap}.st-acts .btn{padding:5px 9px;font-size:12px;text-decoration:none}
.hrow{display:flex;gap:12px;align-items:center;background:var(--panel2);border-radius:10px;padding:8px;margin-bottom:8px}
.hrow img,.hrow .noimg{width:44px;height:78px;object-fit:cover;border-radius:6px;background:#000;flex:none}
.hrow .tt{flex:1;min-width:0}.hrow .tt b{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;display:inline-block;vertical-align:bottom}
.pill{font-size:11px;border-radius:99px;padding:2px 8px;margin-left:6px;white-space:nowrap}
.pill.uploaded{background:#183a29;color:#9ee6bd}.pill.exported{background:#1d2c44;color:#9cc4ff}.pill.rejected{background:#3a1d1f;color:#ffb3b6}
.colwrap{position:relative;display:inline-block}
.colmenu{position:absolute;bottom:calc(100% + 6px);right:0;z-index:30;min-width:220px;background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:6px;box-shadow:0 10px 30px #0008}
.colmenu button{display:block;width:100%;text-align:left;background:none;border:0;color:var(--text);padding:8px 10px;border-radius:7px;font:inherit;font-size:13px;cursor:pointer}
.colmenu button:hover{background:var(--line)}.colmenu button.in{color:#9ee6bd}.colmenu .new{color:var(--mute)}
.mo img.v{width:34px;height:60px}
.tc-wrap{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:20px;align-items:start}
@media(max-width:1000px){.tc-wrap{grid-template-columns:1fr}}
.tc-line{background:var(--panel2);border-radius:10px;padding:10px;margin-bottom:8px}
.tc-line .row{gap:6px}.tc-line input[type=text]{flex:1;min-width:160px;font-weight:800;text-transform:uppercase}
.tc-line .seg button{padding:5px 9px;font-size:12px}.tc-line .mini{padding:5px 8px;font-size:12px}
.tc-stage{position:relative;width:100%;aspect-ratio:9/16;border-radius:12px;overflow:hidden;background:repeating-conic-gradient(#2a2c31 0 25%,#1f2125 0 50%) 0 0/22px 22px;background-size:cover}
.tc-stage.chk{background:repeating-conic-gradient(#2a2c31 0 25%,#1f2125 0 50%) 0 0/22px 22px}
.tc-stage img,.tc-stage canvas{position:absolute;inset:0;width:100%;height:100%}
.tc-busy{position:absolute;right:8px;top:8px;font-size:11px;color:var(--mute);background:#000a;padding:2px 8px;border-radius:99px;display:none}
.st-bar{display:flex;height:16px;border-radius:99px;overflow:hidden;margin:12px 0 6px;background:var(--panel2)}
.st-bar span{display:block;height:100%}
.st-item{display:grid;grid-template-columns:minmax(0,1fr) 90px 80px;gap:10px;align-items:center;background:var(--panel2);border-radius:8px;padding:8px 10px;margin-top:6px}
.st-item .sz{font:700 13px Consolas,monospace;color:var(--acc);text-align:right}.st-item .btn{padding:5px 10px;font-size:12px}
.ed-foot{display:flex;align-items:center;gap:12px;margin-top:18px;border-top:1px solid var(--line);padding-top:14px}
.ov{display:flex;align-items:center;gap:12px;background:var(--panel2);border-radius:10px;padding:10px;margin-bottom:8px}
.ov img{width:54px;height:96px;object-fit:contain;background:repeating-conic-gradient(#333 0 25%,#222 0 50%) 0 0/12px 12px;border-radius:6px}
.ov .nm{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
select{background:#0f1012;border:1px solid var(--line);color:var(--text);border-radius:8px;padding:8px}
.plan .it .btn{padding:7px 12px;font-size:13px}
.kw-res{margin-top:16px}.kw-player{display:none;margin:12px 0}.kw-player.aud video{height:54px;max-height:54px;background:transparent}.mt+.kw-player{margin:0 0 12px}.kw-player video{width:100%;max-height:46vh;background:#000;border-radius:10px}
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
    <button data-t="comps">Compilations</button>
    <button data-t="cols">Collections</button>
    <button data-t="titles">Title Cards</button>
    <button data-t="history">History</button>
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
  <div class="card" id="liveCard">
    <div id="liveIdle">
      <div class="row"><h3 style="margin:0">Record live</h3><span class="tiny mute">Record Peanut's stream while he's live - no waiting for YouTube.</span></div>
      <div class="row" style="margin-top:10px"><input class="big" type="text" id="liveUrl" placeholder="Leave empty to use his channel (from Settings) - or paste a live link"></div>
      <div class="row tiny" style="margin-top:10px;gap:18px">
        <label class="toggle"><input type="checkbox" id="liveFromStart"> Record from the very start of the stream</label>
        <label class="toggle"><input type="checkbox" id="liveThenMake"> Make Shorts as soon as he ends</label>
        <label class="toggle"><input type="checkbox" id="liveInAuto"> Also check in the nightly auto mode</label></div>
      <div class="row" style="margin-top:12px"><button class="btn main" id="liveNow">Record now</button><button class="btn" id="liveWait">Wait for him to go live</button>
        <span class="tiny mute" id="liveMsg"></span></div>
    </div>
    <div id="liveRec" style="display:none">
      <div class="row"><span class="rec-dot" id="liveDot"></span><h3 style="margin:0" id="liveHead">Recording live</h3><span class="mute" id="liveTitle"></span>
        <button class="btn rec" id="liveStop" style="margin-left:auto">Stop recording</button></div>
      <div class="live-st" id="liveStats"><div><span>Recorded</span><b id="lvTime">0:00:00</b></div><div><span>Size</span><b id="lvSize">0 MB</b></div>
        <div><span>Chat messages</span><b id="lvChat">0</b></div><div><span>Free disk</span><b id="lvFree">-</b></div></div>
      <div class="tiny mute" style="margin-top:10px" id="liveNote">Keep the PC on and online. You can use the rest of the app while it records.</div>
    </div>
    <div id="liveDone" style="display:none">
      <div class="row"><h3 style="margin:0" id="lvDoneHead">Recording saved</h3><span class="mute" id="lvDoneInfo"></span></div>
      <div class="row" style="margin-top:10px"><button class="btn main" id="lvMake">Make Shorts from it</button><button class="btn" id="lvSearch">Keyword search it</button>
        <button class="btn" id="lvAgain">Record another</button><span class="tiny mute" id="lvMakeNote"></span></div>
      <div id="lvMakeBar" style="display:none;margin-top:10px"><div class="bar"><i id="lvMakeFill"></i></div></div>
    </div>
  </div>
  <div class="card" id="srcCard">
    <h3>From a stream or your own video</h3>
    <div class="row">
      <input class="big" type="text" id="url" placeholder="Paste a stream link, or drop a video file here">
      <button class="btn" id="upPick">Choose file</button>
      <button class="btn main" id="go">Make Shorts</button>
      <input type="file" id="upFile" accept="video/*,.mp4,.mov,.mkv,.webm,.m4v,.avi,.ts,.flv,.wmv,.mts" style="display:none">
    </div>
    <div class="row tiny" style="margin-top:12px;gap:10px"><span class="mute">Make</span>
      <span class="seg" id="mkMode"><button data-v="shorts">Shorts</button><button data-v="long">Long video (16:9)</button><button data-v="both">Both</button></span>
      <span id="mkLenBox" class="row tiny" style="gap:10px;margin-left:8px"><span class="mute">Length</span>
        <span class="seg" id="mkLen"><button data-v="8">8 min</button><button data-v="10">10</button><button data-v="15">15</button><button data-v="20">20</button></span></span></div>
    <div class="tiny mute" id="mkLenNote" style="margin-top:6px">Picks the strongest moments (chat spikes, loud parts, what's said) until it reaches the length, keeps them in stream order, and opens them in Compilations to trim, reorder and export (1920x1080, or for Premiere).</div>
    <div id="upPicked" class="row tiny" style="display:none;margin-top:10px"><span class="mute">Picked:</span> <b id="upName"></b> <span class="mute" id="upState"></span>
      <button class="link" id="upRemove">remove</button></div>
    <div id="upBarWrap" style="display:none;margin-top:6px"><div class="bar"><i id="upFill"></i></div></div>
    <div class="row" style="margin-top:12px">
      <label class="toggle tiny"><input type="checkbox" id="part"> Only use part of the stream or video</label>
      <span id="partBox" style="display:none" class="row tiny">from <input type="text" class="small" id="from" value="1:00:00"> to <input type="text" class="small" id="to" value="2:00:00"></span>
    </div>
    <p class="tiny mute" style="margin:10px 0 0">A video file is copied into the app, so your original never gets moved or deleted, and the copy is cleaned up with the other downloads (Settings &gt; Storage). Tip: for your own videos the <b>single</b> or <b>blurfit</b> layout usually looks better than the face-cam stack.</p>
  </div>
  <div class="card" id="inbCard">
    <div class="row"><h3 style="margin:0">Auto-clip folder</h3>
      <label class="toggle tiny" style="margin-left:auto"><input type="checkbox" id="inbOn"> On</label></div>
    <p class="tiny mute" style="margin:6px 0 10px">Any video you put in this folder gets made into Shorts on its own (while the app is open, and in the nightly auto run). Shorts show up in Review.</p>
    <div class="row"><input class="big" type="text" id="inbFolder" spellcheck="false"><button class="btn" id="inbBrowse">Browse</button><button class="btn" id="inbOpen">Open</button></div>
    <div class="tiny mute" id="inbStat" style="margin-top:10px"></div>
    <div id="inbFailed" class="tiny" style="margin-top:6px"></div>
    <div class="row tiny" style="margin-top:10px;gap:18px">
      <label class="toggle"><input type="checkbox" id="inbMove"> Move finished videos to a "Done" subfolder</label>
      <label class="toggle"><input type="checkbox" id="inbDel"> Delete them when done</label>
      <span class="row tiny"><span class="mute">Layout</span><select id="inbLayout" style="min-width:180px"></select></span></div>
  </div>
  <div class="card">
    <h3>Find by keywords</h3>
    <p class="tiny mute" style="margin:-4px 0 12px">Finds every time Peanut says these words (and when chat spams them). Separate words or phrases with commas.</p>
    <div class="row">
      <input class="big" type="text" id="kwUrl" placeholder="Stream link (leave empty to use the one above)">
    </div>
    <div class="row" style="margin-top:10px">
      <input class="big" type="text" id="kwWords" placeholder='e.g.  drive, use a blinker, red light'>
      <button class="btn" id="kwCrash" title="Fill in GTA crash words">Crash words</button>
      <button class="btn main" id="kwGo">Search</button>
    </div>
    <div class="row tiny" style="margin-top:10px;gap:18px">
      <label class="toggle"><input type="checkbox" id="kwChat" checked> Also search chat</label>
      <label class="toggle"><input type="checkbox" id="kwSimilar" checked> Match similar words (drive &rarr; driving)</label>
      <label class="toggle" title="About 0.7 GB for 12 hours instead of ~30 GB. Video for a match is downloaded only when you use it."><input type="checkbox" id="kwSound" checked> <b>Search the sound only (small download)</b></label>
      <label class="toggle"><input type="checkbox" id="kwPart"> Only part of the stream</label>
      <span id="kwPartBox" style="display:none" class="row">from <input type="text" class="small" id="kwFrom" value="1:00:00"> to <input type="text" class="small" id="kwTo" value="2:00:00"></span>
    </div>
    <p class="tiny mute" id="kwCpu" style="display:none;margin:10px 0 0">Heads up: speech is running on the CPU, so searching a full stream can take an hour or more. Try "Only part of the stream" first.</p>
    <div class="kw-res" id="kwRes" style="display:none">
      <div class="row"><b id="kwHead"></b><span style="margin-left:auto" class="tiny mute">Earlier searches</span><select id="kwPick"></select></div>
      <div class="row tiny" style="margin-top:8px"><span class="mute">+ Add to compilation puts moments into:</span><select id="kwComp"></select><span class="mute" id="kwCompLen"></span></div>
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

<section id="comps">
  <h2>Compilations</h2><p class="sub">Long 16:9 videos: the ones Make Shorts builds (Long video), and ones you put together from keyword searches (like every GTA crash). Edit them here, then export.</p>
  <div class="card">
    <div class="cmp-head"><select id="cmpPick"></select><button class="btn" id="cmpNew">New compilation</button>
      <button class="btn" id="cmpRen">Rename</button><button class="btn no" id="cmpDel">Delete</button>
      <span style="margin-left:auto" class="tiny mute">Goal (minutes) <input type="number" class="small" id="cmpGoal" min="1" max="240" step="1" style="width:80px"></span></div>
    <div class="cmp-head" style="margin-top:14px"><b id="cmpLen" style="font:700 18px Consolas,monospace;color:var(--acc)"></b>
      <div class="cmp-bar" id="cmpBar"><i></i></div><span class="tiny mute" id="cmpLeft"></span></div>
  </div>
  <div class="card" id="cmpBody">
    <div class="ed-grid">
      <div>
        <div class="ed-player" id="edPlayer"><video id="cmpVid" preload="none" playsinline></video><div class="ed-ov" id="edOv"></div>
          <div class="ed-empty" id="edEmpty">Press Play, or click a part of the timeline</div></div>
        <div class="ed-row"><button class="btn main" id="edPlay">&#9654; Play</button><span class="mono" id="edTime">0:00 / 0:00</span>
          <button class="btn" id="edSplit" title="Cut the part under the playhead in two (S)">Split at playhead</button>
          <button class="btn" id="edDel">Delete part</button><button class="btn" id="edUndo">Undo</button></div>
      </div>
      <div class="ed-insp" id="edInsp"></div>
    </div>
    <div class="ed-tl" id="edTl"></div>
    <div class="row tiny mute" style="justify-content:space-between"><span>Drag parts to reorder &middot; drag the yellow edges to trim &middot; right-click to remove</span>
      <span>+ Add: scrub the whole stream and mark a new part</span></div>
    <div id="edAdd" class="ed-add" style="display:none">
      <div class="row"><b>Add a part from the stream</b><span class="tiny mute" id="edAddWhere"></span><button class="link" id="edAddX" style="margin-left:auto">Close</button></div>
      <video id="edSrc" controls preload="none" playsinline></video>
      <div class="ed-row"><button class="btn" id="edMarkA">Mark start</button><button class="btn" id="edMarkB">Mark end</button>
        <span class="mono" id="edMarks">Start - &middot; End -</span><button class="btn main" id="edAddGo" style="margin-left:auto">Add this part</button></div>
    </div>
    <div class="ed-row" style="margin-top:14px"><span class="tiny mute">Between parts (unless a part says otherwise)</span>
      <span class="seg" id="cmpTr"><button data-v="cut">Cut</button><button data-v="flash">Flash</button><button data-v="fade">Fade</button></span>
      <span class="tiny mute" style="margin-left:12px">Numbers on screen</span>
      <span class="seg" id="cmpNum"><button data-v="1">On</button><button data-v="0">Off</button></span>
      <span style="margin-left:auto" class="row"><button class="btn" id="cmpShuffle">Shuffle</button><button class="btn" id="cmpOldest">Oldest first</button></span></div>
  </div>
  <div class="card">
    <div class="ed-row" style="margin-top:0"><span class="tiny mute">Intro</span><select id="edIntro"></select>
      <span class="tiny mute">Outro</span><select id="edOutro"></select>
      <span class="tiny mute">Music bed</span><select id="edMusic"></select>
      <span class="row tiny" id="edVolBox"><input type="range" id="edVol" min="0" max="60" step="1" style="width:110px"><span class="mono" id="edVolV"></span></span>
      <button class="btn" id="edMediaUp">Upload clip or music</button><input type="file" id="edMediaFile" accept="video/*,audio/*,.mp3,.wav,.m4a,.mp4,.mov" style="display:none"></div>
    <div class="ed-row"><button class="btn" id="edChap">Chapters for YouTube</button>
      <span style="margin-left:auto" class="row"><button class="btn" id="cmpPrem">Export for Premiere</button><button class="btn main" id="cmpExport">Export 1920x1080</button></span></div>
    <div id="edChapBox" style="display:none;margin-top:10px"><textarea id="edChapTxt" rows="7" style="width:100%;font:13px Consolas,monospace" readonly></textarea>
      <div class="row tiny mute" style="margin-top:6px">From each part's title (edit titles on the right). Also saved next to the exported video. <button class="btn" id="edChapCopy" style="margin-left:auto">Copy</button></div></div>
    <p class="tiny mute" style="margin:10px 0 0">Your edits are saved as you go. Premiere = every part as its own file + a ready-made sequence (File &rarr; Import &rarr; the .xml); zoom, text, intro/outro and music are in the 1920x1080 export.</p>
  </div>
</section>

<section id="cols">
  <h2>Collections</h2><p class="sub">Shorts you set aside from Review for a montage later. Each one keeps its own copy, so deleting the Short is fine.</p>
  <div class="card">
    <div class="cmp-head"><select id="colPick"></select><button class="btn" id="colNew">New collection</button>
      <button class="btn" id="colRen">Rename</button><button class="btn no" id="colDel">Delete</button>
      <span style="margin-left:auto" class="tiny mute">Goal (minutes, optional) <input type="number" class="small" id="colGoal" min="1" max="240" step="1" style="width:80px"></span></div>
    <div class="cmp-head" style="margin-top:14px"><b id="colLen" style="font:700 18px Consolas,monospace;color:var(--acc)"></b>
      <div class="cmp-bar" id="colBar"><i></i></div><span class="tiny mute" id="colLeft"></span></div>
  </div>
  <div class="card">
    <div class="cmp-player" id="colPlayer" style="display:none;margin-bottom:12px"><video id="colVid" controls preload="none"></video>
      <div class="row tiny mute" style="margin-top:6px"><span id="colNow"></span><button class="btn" id="colStop" style="margin-left:auto;padding:6px 10px">Stop</button></div></div>
    <div class="row" style="margin-bottom:10px"><b id="colCount"></b><span class="tiny mute">Drag the number to reorder.</span>
      <span style="margin-left:auto" class="row"><button class="btn" id="colPlayAll">&#9654; Play all</button><button class="btn" id="colShuffle">Shuffle</button><button class="btn" id="colOldest">Oldest first</button></span></div>
    <div id="colList"></div>
  </div>
  <div class="card">
    <div class="row"><span class="tiny mute" style="min-width:120px">Montage shape</span>
      <span class="seg" id="colShape"><button data-v="vertical">Vertical 9:16 (as the Shorts look)</button><button data-v="horizontal">Horizontal 16:9 (original stream view)</button></span></div>
    <div class="row" style="margin-top:10px"><span class="tiny mute" style="min-width:120px">Between clips</span>
      <span class="seg" id="colTr"><button data-v="cut">Cut</button><button data-v="flash">Quick flash</button><button data-v="fade">Crossfade</button></span>
      <span class="tiny mute" style="margin-left:18px">Clip numbers</span>
      <span class="seg" id="colNum"><button data-v="1">On</button><button data-v="0">Off</button></span></div>
    <div class="row" style="margin-top:14px"><button class="btn main" id="colExport">Export montage</button><button class="btn" id="colPrem">Export for Premiere</button>
      <span class="tiny mute">Premiere = each clip as its own file + a ready-made sequence (XML). In Premiere: File &rarr; Import &rarr; the .xml.</span></div>
  </div>
</section>

<section id="titles">
  <h2>Title Cards</h2><p class="sub">Big outlined text for the top of a Short, saved as a see-through picture (1080x1920 PNG) you drop on your Premiere timeline.</p>
  <div class="tc-wrap">
    <div>
      <div class="card">
        <div class="row"><select id="tcShort" style="max-width:340px"></select>
          <button class="btn" id="tcFrom">From the Short's title</button><button class="btn" id="tcShuffle">Shuffle styles</button>
          <button class="btn" id="tcAdd">+ Line</button><button class="btn" id="tcClear">Clear</button></div>
        <div id="tcLines" style="margin-top:12px"></div>
      </div>
      <div class="card">
        <div class="row"><span class="tiny mute" style="min-width:110px">Red brush behind the top lines</span><span class="seg" id="tcBrush"><button data-v="1">On</button><button data-v="0">Off</button></span>
          <span class="tiny mute" style="margin-left:14px">Where</span><span class="seg" id="tcPos"><button data-v="top">Top</button><button data-v="middle">Middle</button><button data-v="bottom">Bottom</button></span></div>
        <div class="row" style="margin-top:10px"><span class="tiny mute" style="min-width:110px">Slant</span><input type="range" id="tcSlant" min="0" max="0.15" step="0.01" style="width:180px">
          <span class="tiny mute" style="margin-left:14px">Line spacing</span><input type="range" id="tcGap" min="-0.25" max="0.1" step="0.01" style="width:180px"></div>
        <div class="row" style="margin-top:10px"><span class="tiny mute" style="min-width:110px">Preview behind it</span><span class="seg" id="tcBg"><button data-v="chk">Checkerboard</button><button data-v="short">The Short</button></span>
          <label class="toggle tiny" style="margin-left:14px"><input type="checkbox" class="safeTog"> Safe zones</label></div>
        <div class="row" style="margin-top:14px"><button class="btn main" id="tcSave">Save PNG (transparent)</button><button class="btn" id="tcCopy">Copy</button>
          <span class="tiny mute">Saves to <span id="tcFolder"></span> &nbsp;<button class="link" onclick="pickFolder('title_folder')">Change</button> &nbsp;<button class="link" onclick="openSetFolder('title_folder')">Open</button></span></div>
      </div>
    </div>
    <div><div class="tc-stage chk" id="tcStage"><img id="tcImg" alt=""><canvas id="tcSafe" width="540" height="960"></canvas><span class="tc-busy" id="tcBusy">updating...</span></div></div>
  </div>
</section>

<section id="history">
  <h2>History</h2><p class="sub">Every Short you've uploaded, exported or rejected - with where it came from in the stream. Kept even after the video files are deleted.</p>
  <div class="card">
    <div class="row"><input class="big" type="text" id="hSearch" placeholder="Search titles or words said..." style="flex:1">
      <span class="seg" id="hFilter"><button data-v="" class="on">All</button><button data-v="uploaded">Uploaded</button><button data-v="exported">Exported</button><button data-v="rejected">Rejected</button></span></div>
    <div class="tiny mute" style="margin:10px 0 12px">"Screenshot" shows while the stream is still on your PC (before auto-delete). After that, "Open stream there" opens it at that exact second so you can pause and grab it.</div>
    <div id="hList"></div>
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
      <label class="k">Export folder</label><div class="row" style="flex-wrap:nowrap"><input type="text" class="big" id="s_export_folder" style="flex:1" placeholder="e.g. C:\Users\Batman\Freelance\Smear Frame Studios\Frame Drip X\BurntPeanut XD\RAW CLIPS"><button class="btn" type="button" onclick="pickFolder('export_folder')">Browse...</button><button class="btn" type="button" onclick="openSetFolder('export_folder')">Open</button></div>
      <label class="k">Screenshot folder</label><div><div class="row" style="flex-wrap:nowrap"><input type="text" class="big" id="s_screenshot_folder" style="flex:1" placeholder="Empty = the Export folder\Screenshots"><button class="btn" type="button" onclick="pickFolder('screenshot_folder')">Browse...</button><button class="btn" type="button" onclick="openSetFolder('screenshot_folder')">Open</button></div>
        <div class="tiny mute" style="margin-top:4px">Leave empty to keep using the Export folder\Screenshots. Browse opens the normal Windows folder picker.</div></div>
      <label class="k">Extra seconds each side</label><input type="number" min="0" max="30" class="small" id="s_export_handles_sec">
      <label class="k">Also copy the vertical Short</label><label class="toggle"><input type="checkbox" id="s_export_vertical_too"> Put the app's vertical version next to the raw clip</label>
      <label class="k">Frame rate of the app's Shorts</label><select id="s_output_fps"><option value="60">60 fps</option><option value="30">30 fps</option></select>
    </div>
  </div>
  <div class="card" id="storageCard"><div class="row"><h3 style="margin:0">Storage</h3><span class="tiny mute" id="stRoot"></span>
      <span style="margin-left:auto" class="row"><b id="stTotal" style="font:700 18px Consolas,monospace;color:var(--acc)"></b><span class="tiny mute" id="stFree"></span>
      <button class="btn" id="stRefresh" style="padding:6px 10px">Refresh</button></span></div>
    <div class="st-bar" id="stBar"></div><div class="row tiny mute" id="stLegend"></div>
    <div style="margin-top:12px"><b>Biggest items</b></div><div id="stItems"><div class="tiny mute">Open Settings to see what's using space.</div></div>
    <div class="row" style="margin-top:12px"><button class="btn main" id="stClean">Clean up now</button>
      <span class="tiny mute">Deletes everything the Auto-delete rules below allow (you see the list first). Never touches Exports or Compilations.</span></div>
  </div>
  <div class="card"><h3>Auto-delete</h3>
    <div class="set">
      <label class="k">Downloaded streams</label><label class="toggle"><input type="checkbox" id="s_delete_source"> Delete once every Short from it is done</label>
      <label class="k">...or after this many days</label><div><input type="number" min="1" max="30" class="small" id="s_keep_source_days"> <span class="tiny mute">also downloads with no Shorts, unused live recordings and stream parts</span></div>
      <label class="k">Shorts exported to Premiere</label><div><label class="toggle"><input type="checkbox" id="s_delete_exported"> Delete the app's copy after</label> <input type="number" min="0" max="60" class="small" id="s_delete_exported_days"> <span class="tiny mute">days - your Premiere export stays</span></div>
      <label class="k">Keyword searches</label><div><label class="toggle"><input type="checkbox" id="s_delete_searches"> Remove after</label> <input type="number" min="1" max="90" class="small" id="s_search_keep_days"> <span class="tiny mute">days - History and compilations keep their own copies</span></div>
      <label class="k">Rejected Shorts</label><label class="toggle"><input type="checkbox" id="s_delete_rejected"> Delete when I click Reject</label>
      <label class="k">Uploaded Shorts</label><label class="toggle"><input type="checkbox" id="s_delete_uploaded"> Delete once they're on YouTube (and once exported to Premiere)</label>
      <div></div><div class="tiny mute">Shorts still in Review or Approved are never deleted automatically. Auto-delete runs when the app opens, after Reject / upload / export, and every night.</div>
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
        <label class="toggle tiny"><input type="checkbox" class="safeTog"> Show YouTube safe zones (where the Shorts buttons cover the video)</label>
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
      <div class="row" style="margin-top:10px"><button class="btn" id="mkAdd">+ Marker at playhead <span class="tiny mute">(M)</span></button>
        <button class="btn" id="mkPrev">&#9664; Marker</button><button class="btn" id="mkNext">Marker &#9654;</button>
        <label class="toggle"><input type="checkbox" id="mkSnap" checked> Snap to markers</label>
        <button class="btn" id="mkClear">Clear markers</button>
        <span class="tiny mute"><b>Markers:</b> click one to jump there, right-click to remove it.</span></div>
      <div class="sec-tools">
        <div class="row"><b>Sections</b><span class="tiny mute">Cut the Short into parts, then pick how each part looks - like a razor cut in Premiere.</span></div>
        <div class="sec-tl" id="secTl"></div>
        <div class="row"><button class="btn" id="secCut">&#9986; Cut at playhead <span class="tiny mute">(C)</span></button>
          <button class="btn" id="secJoin">Remove cut before this part</button>
          <button class="btn" id="secClear">Remove all cuts</button>
          <span class="tiny mute"><b>Part:</b> <span id="secWhich">click a part on the bar</span></span></div>
        <div class="row" style="margin-top:8px"><span class="tiny mute" style="min-width:52px">Look</span>
          <span class="seg" id="secLook"><button data-v="normal">Normal (layout)</button><button data-v="closeup">Close-up on Peanut</button><button data-v="gameplay">Gameplay only</button></span>
          <span class="tiny mute" style="margin-left:10px">Banner</span>
          <span class="seg" id="secBan"><button data-v="layout">Layout spot</button><button data-v="bottom">Bottom</button><button data-v="top">Top</button><button data-v="off">Off</button></span></div>
        <div class="sec-box" id="secBoxWrap" style="display:none">
          <div class="fr-stage" id="secStage"><canvas id="secCan" width="960" height="540"></canvas><div class="box av" id="secBox"></div></div>
          <div style="width:260px" class="tiny mute"><b id="secBoxT">Close-up area</b><br><b>Move:</b> drag inside the box. <b>Redraw:</b> drag on the frame.
            <label style="display:block;margin-top:8px"><b>Zoom:</b> smaller = closer <input type="range" id="secZoom" min="5" max="100" step="1" style="width:100%"></label>
            <button class="btn" id="secBoxReset" style="margin-top:6px">Reset area</button>
            <button class="btn" id="secBoxAll" style="margin-top:6px">Use this area for every part with this look</button></div>
        </div>
      </div>
      <div class="fr-wrap">
        <button class="btn" id="frToggle">Framing for this Short &#9662;</button> <span class="tiny mute" id="frState"></span>
        <div id="frPanel" style="display:none">
          <div class="row" style="margin-top:10px"><span class="seg" id="frMode"><button data-m="stack">Peanut over gameplay</button><button data-m="single">Gameplay only</button><button data-m="blurfit">Whole stream</button></span></div>
          <div class="fr">
            <div class="fr-stage" id="frStage"><canvas id="frCan" width="960" height="540"></canvas>
              <div class="box av" id="f_avatar"></div><div class="box gp" id="f_gameplay"></div></div>
            <div class="fr-side">
              <div id="frWhich"><label class="toggle"><input type="radio" name="frw" value="avatar" checked> <b style="color:#ff4fb3">Peanut box</b></label>
                <label class="toggle"><input type="radio" name="frw" value="gameplay"> <b style="color:#3fa9ff">Gameplay box</b></label>
                <p class="tiny mute" style="margin:4px 0 0"><b>Move:</b> drag inside the box. <b>Redraw:</b> drag on the frame. The frame is wherever the stream video above is paused.</p></div>
              <label class="tiny mute" id="frZoomWrap"><b>Zoom:</b> smaller box = closer in <input type="range" id="frZoom" min="5" max="100" step="1" style="width:100%"></label>
              <label class="tiny mute" id="frThWrap"><b>Peanut area height:</b> <span id="frThV"></span> <input type="range" id="frTh" min="480" max="1300" step="10" style="width:100%"></label>
              <div class="fr-prev"><canvas id="frPrev" width="270" height="480"></canvas>
                <label class="toggle tiny" style="margin-top:6px"><input type="checkbox" class="safeTog"> Safe zones</label></div>
              <div class="row"><button class="btn main" id="frUse">Use for this Short</button><button class="btn" id="frSaveLy">Save as new layout</button><button class="btn" id="frReset">Reset to layout</button></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="ed-side"><div class="tiny mute" style="margin-bottom:6px">Live preview <span id="liveWhat"></span></div>
      <label class="toggle tiny" style="margin-bottom:6px"><input type="checkbox" class="safeTog"> Safe zones</label><canvas class="live" id="live" width="540" height="960"></canvas>
      <button class="btn" id="shotShort">&#128247; Screenshot (Short) <span class="tiny mute">Ctrl+Shift+E</span></button>
      <button class="btn" id="shotStream">&#128247; Screenshot (full stream frame)</button>
      <div class="tiny mute" style="margin:14px 0 6px">Current Short</div><video id="edShort" controls preload="none"></video></div>
  </div>
  <div class="ed-foot"><span class="tiny mute" id="edNote">Drag the yellow handles, or click the bar to jump there. Shorts can be up to 3 minutes.</span>
    <span style="margin-left:auto" class="row"><span class="tiny mute">Layout</span><select id="edLayout"></select>
    <button class="btn main" id="edSave">Update Short</button></span></div>
</div></div>
</main>
<div class="toast" id="toast"></div>
<div class="cover" id="cover"><div class="spin"></div><h2 id="coverT">Updating...</h2><div class="mute" id="coverM"></div></div>

<script>
const SAFE_M={top:300,bottom:480,right:165,left:65};let SAFE=false;try{SAFE=localStorage.getItem('pc_safe')==='1'}catch(e){}
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
  if(t==='review')loadClips(); if(t==='comps')loadComps(); if(t==='cols')loadCols(); if(t==='history')loadHistory(); if(t==='titles')loadTitles(); if(t==='settings')loadStorage(); if(t==='upload')loadPlan(); if(t==='settings')fillSettings(); if(t==='layout')initLayout();}

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
  const titles={syncfix:'Converting the stream',compadd:'Adding to the compilation',compaddrange:'Adding a part',compexport:'Exporting',coladd:'Adding to the collection',search:'Searching for keywords',fromsearch:'Cutting a match',rerender:'Re-cutting a Short',export:'Exporting for Premiere',vod:'Making Shorts',longvid:'Making a long video',inbox:'Auto-clip folder',clips:'Twitch top clips',upload:'Uploading',auto:'Auto mode',frame:'Grabbing a frame',hwtest:'Graphics card test'};
  $('jobTitle').textContent=(titles[j.kind]||'Working')+(j.running?'...':'');
  $('jobPct').textContent=j.running?j.pct+'%':'';
  $('bar').className='bar'+(j.ok===false?' err':(j.ok?' done':''));$('bar').firstElementChild.style.width=(j.ok?100:j.pct)+'%';
  $('jobLabel').textContent=j.label+(j.queued?` (${j.queued} waiting in line)`:'');$('cancel').style.display=j.running?'':'none';
  ['go','kwGo','goTwitch','goAuto','goUpload','goFrame','hwTest'].forEach(id=>$(id).disabled=j.running);
  if(logOpen){$('log').textContent=j.log.join('\n');}
  const key=j.kind+':'+j.ok;
  if(!j.running&&j.ok!==null&&lastJobKey&&lastJobKey!==key){
    if(j.ok&&['vod','clips','auto','inbox'].includes(j.kind)){toast(`<b>${esc(j.label)}</b><br><button class="link" onclick="show('review')">Go to Review</button>`)}
    if(j.ok&&j.kind==='longvid'){toast(`<b>${esc(j.label)}</b><br><button class="link" onclick="openLastLong()">Open it in Compilations</button>`);loadComps()}
    if(j.ok&&j.kind==='frame'){initLayout(true)}
    if(j.ok&&j.kind==='upload'){loadPlan()}
    if(j.ok&&j.kind==='export'){toast('<b>Exported for Premiere.</b><br><span class="tiny">'+esc(S.settings.export_folder||S.default_export)+'</span>');loadPlan()}
    if(j.ok&&j.kind==='search'){loadSearches(true)}
    if(j.kind==='compaddrange'){loadComps();if(j.ok)toast('<b>'+esc(j.label)+'</b>')}
    if(j.kind==='compadd'){addingNow={};loadComps();if(j.ok)toast('<b>'+esc(j.label)+'</b>')}
    if(j.kind==='coladd'){colAdding={};loadCols();if(j.ok)toast('<b>'+esc(j.label)+'</b>')}
    if(j.ok&&j.kind==='compexport'){loadComps();loadCols();const f=S.settings.export_folder||S.default_export;
      toast('<b>'+esc(j.label)+'</b><br><span class="tiny">'+esc(f)+'</span><br><button class="link" onclick="api(\'/api/open_folder\',{path:'+esc(JSON.stringify(f)).replace(/'/g,'&#39;')+'})">Open the folder</button>')}
    if(j.kind==='fromsearch'){if(KW)openSearch(KW.sid,true);
      if(j.ok&&S.last_made&&!S.last_made.export){api('/api/clips').then(cs=>{const c=cs.find(x=>x.job===S.last_made.job&&x.id===S.last_made.id);if(c)openEditor(c)})}
      if(j.ok&&S.last_made&&S.last_made.export)toast('<b>Exported for Premiere.</b><br><span class="tiny">'+esc(S.settings.export_folder||S.default_export)+'</span>')}
    if(j.kind==='syncfix'){if(j.ok&&pendingEdit){const c=pendingEdit;pendingEdit=null;openEditor(c)}
      if(j.ok&&pendingPreview!==null&&KW){const i=pendingPreview;pendingPreview=null;openSearch(KW.sid).then(()=>{const b=document.querySelector(`[data-a=play][data-i="${i}"]`);if(b)b.click()})}}
    if(j.kind==='rerender'){const wasSaving=edSaving;edSaving=false;$('edSave').disabled=false;$('edSave').textContent='Update Short';
      if(j.ok){toast('Short updated.');if(wasSaving)closeEditor();loadClips()}
      else if(E&&E.shortSrc&&!$('edShort').getAttribute('src'))$('edShort').src=E.shortSrc}
    if(!j.ok){toast('<b>Stopped:</b> '+esc(j.label)+'<br><span class="tiny">Click "Show details" on the Make Shorts tab for the full log.</span>')}
  }
  lastJobKey=j.running?'running':key;
}
$('logBtn').onclick=()=>{logOpen=!logOpen;$('log').style.display=logOpen?'block':'none';$('logBtn').textContent=logOpen?'Hide details':'Show details';if(S)drawJob(S.job)};
$('cancel').onclick=()=>api('/api/cancel',{}).then(poll);
$('part').onchange=e=>$('partBox').style.display=e.target.checked?'inline-flex':'none';
$('go').onclick=async()=>{
  if(UP.file&&!UP.path){UP.makeWhenDone=true;toast('Making Shorts starts as soon as the upload finishes.');return}
  const body={kind:'vod',url:UP.path||$('url').value,layout:$('mkLayout').value,mode:S.settings.make_mode||'shorts',minutes:S.settings.long_minutes||8};if($('part').checked){body.from=$('from').value;body.to=$('to').value}
  await api('/api/run',body);lastJobKey='running';if(UP.path){UP.path='';UP.file=null;upDraw('')}poll()};
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
  if(LV&&LV.alive&&!confirm('A live recording is running. It keeps recording in the background after you quit - open Peanut Clipper again to see it or stop it. Quit?'))return;
  quitting=true;await fetch('/api/quit',{method:'POST',body:'{}'}).catch(()=>{});
  cover('Peanut Clipper is closed','You can close this tab. Open it again from the Desktop icon.');document.querySelector('.spin').style.display='none'};

// ---------- keyword search ----------
let KW=null, pendingPreview=null, kwPlayAt=null;
$('kwPart').onchange=e=>$('kwPartBox').style.display=e.target.checked?'inline-flex':'none';
$('kwGo').onclick=async()=>{const url=($('kwUrl').value||$('url').value).trim();
  const body={kind:'search',url,words:$('kwWords').value,chat:$('kwChat').checked,exact:!$('kwSimilar').checked,layout:$('mkLayout').value,sound_only:$('kwSound').checked};
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
  $('kwHead').textContent=`${KW.matches.length} match${KW.matches.length===1?'':'es'} for: ${KW.queries.join(', ')}`+(KW.audio_only?' - sound only, video not downloaded yet (each match you use downloads just its part)':'');
  const box=$('kwList');
  if(box.contains($('kwPlayer')))box.before($('kwPlayer'));
  if(!keepPlayer){$('kwPlayer').style.display='none';$('kwVid').pause();kwPlayAt=null}
  $('kwPlayer').classList.toggle('aud',!!KW.audio_only);
  if(!KW.matches.length){box.innerHTML='<div class="mute">No matches. Try fewer or shorter words, or turn on "Match similar words".</div>';return}
  box.innerHTML=KW.matches.map(m=>`<div class="mt"><div class="tm">${T(m.t+KW.offset)}</div>
    <div class="tx"><div class="chips" style="margin-bottom:4px">${m.queries.map(q=>`<span class="chip">${m.kind==='chat'?'chat: ':''}${esc(q)}</span>`).join('')}${m.made?`<span class="made">&#10003; ${m.made==='exported'?'exported':'made into a Short'}</span>`:''}</div>
    ${esc(m.text).replace(/\[\[(.+?)\]\]/g,'<mark>$1</mark>')}</div>
    <div class="bt"><button class="btn" data-a="play" data-i="${m.i}">&#9654; ${KW.audio_only?'Listen':'Preview'}</button><button class="btn main" data-a="short" data-i="${m.i}">Make Short</button><button class="btn" data-a="export" data-i="${m.i}">Export for Premiere</button><button class="btn" data-a="comp" data-i="${m.i}">+ Add to compilation</button></div></div>`).join('');
  box.querySelectorAll('[data-a]').forEach(b=>b.onclick=async()=>{const m=KW.matches.find(x=>x.i==b.dataset.i);
    if(b.dataset.a==='comp'){addToComp(m);return}
    if(!KW.source_available){toast('The stream for this search was deleted. Run the search again to re-download it.');return}
    if(b.dataset.a==='play'&&KW.needs_sync){pendingPreview=m.i;await api('/api/run',{kind:'syncfix',sid:KW.sid});lastJobKey='running';
      toast('Converting this stream so it plays in sync (one time, a few minutes). Preview starts by itself when it\'s done.');poll();return}
    if(b.dataset.a==='play'){const v=$('kwVid');kwPlayAt=m.i;b.closest('.mt').after($('kwPlayer'));$('kwPlayer').style.display='block';
      if(!v.src.endsWith('/search_source/'+KW.sid)){v.preload='auto';v.src='/search_source/'+KW.sid;v.load()}
      const go=()=>{v.currentTime=Math.max(0,m.t-8);v.play()};if(v.readyState>0)go();else v.addEventListener('loadedmetadata',go,{once:true});
      return}
    const r=await api('/api/run',{kind:'fromsearch',sid:KW.sid,idx:m.i,export:b.dataset.a==='export',layout:$('mkLayout').value});lastJobKey='running';if(r.queued)toast('<b>In line:</b> this match is cut when the current job finishes.');poll()});
  if(kwPlayAt!==null){const r=box.querySelector(`[data-a=play][data-i="${kwPlayAt}"]`);if(r)r.closest('.mt').after($('kwPlayer'))}
  markAdded();
}

// ---------- collections (Shorts from Review, for a montage later) ----------
let COL=null,COLS=[],colCur=null,colQueue=null,colStopAt=null,COLMEM={};
try{colCur=localStorage.getItem('pc_col')}catch(e){}
function setCol(id){colCur=id;try{localStorage.setItem('pc_col',id||'')}catch(e){}}
async function loadCols(){const r=await api('/api/comps?kind=collection');COLS=r.comps;COLMEM=r.members||{};
  if(!COLS.some(c=>c.id===colCur))setCol(COLS[0]?COLS[0].id:null);
  $('colPick').innerHTML=COLS.map(c=>`<option value="${esc(c.id)}">${esc(c.name)} (${c.count})</option>`).join('')||'<option value="">No collections yet</option>';
  if(colCur)$('colPick').value=colCur;
  COL=colCur?await api('/api/comp?id='+encodeURIComponent(colCur)).catch(()=>null):null;drawCol();markCols()}
async function newCol(){const name=prompt('Name for the new collection:',`Montage ${COLS.length+1}`);if(!name)return null;
  const c=await api('/api/comp',{action:'new',name,goal:600,kind:'collection'});setCol(c.id);await loadCols();return c.id}
async function colDo(action,extra){if(!COL)return;COL=await api('/api/comp',Object.assign({id:COL.id,action},extra||{}));
  if(action==='delete'){setCol(null);await loadCols();return}await loadCols()}
const colLen=c=>c.moments.reduce((a,m)=>a+((c.shape||'vertical')==='horizontal'&&m.file?m.b-m.a:m.vdur),0);
function drawCol(){const has=!!COL;['colRen','colDel','colExport','colPrem','colShuffle','colOldest','colPlayAll','colGoal'].forEach(id=>$(id).disabled=!has);
  if(!has){$('colLen').textContent='0:00';$('colBar').firstElementChild.style.width='0';$('colLeft').textContent='';$('colCount').textContent='';
    $('colList').innerHTML='<div class="empty">Start one with <b>New collection</b>, then press <b>+ Collection</b> on any Short in Review.</div>';return}
  const len=colLen(COL),goal=COL.goal||600;$('colGoal').value=Math.round(goal/60);$('colLen').textContent=mmss(len);
  $('colBar').className='cmp-bar'+(len>=goal?' done':'');$('colBar').firstElementChild.style.width=Math.min(100,len/goal*100)+'%';
  $('colLeft').textContent=len>=goal?`Goal of ${mmss(goal)} reached`:`goal ${mmss(goal)} - about ${mmss(goal-len)} to go`;
  $('colCount').textContent=`${COL.moments.length} Short${COL.moments.length===1?'':'s'}`;
  [['colShape',COL.shape||'vertical'],['colTr',COL.transition||'cut'],['colNum',COL.numbers?'1':'0']].forEach(([id,v])=>document.querySelectorAll('#'+id+' button').forEach(b=>b.classList.toggle('on',b.dataset.v===v)));
  const list=$('colList');
  if(!COL.moments.length){list.innerHTML='<div class="empty">Nothing here yet. Press <b>+ Collection</b> on a Short in Review.</div>';return}
  const horiz=(COL.shape||'vertical')==='horizontal';
  list.innerHTML=COL.moments.map((m,k)=>`<div class="mo" draggable="true" data-mid="${m.mid}"><span class="num" title="Drag to reorder">${k+1}</span>
    <img class="v" src="/comp/${esc(COL.id)}/${esc(m.poster)}" alt="">
    <div class="tt"><b title="${esc(m.title)}">${esc(m.title)}</b><span class="tiny mute">${m.stream_date?esc(niceDate(m.stream_date))+' stream &middot; ':''}${m.stream_t!=null?'<span class="tc">'+tcode(m.stream_t)+'</span> &middot; ':''}${mmss(horiz&&m.file?m.b-m.a:m.vdur)}${horiz&&!m.file?' &middot; no horizontal copy (stream was gone) - shown with blurred sides':''}</span></div>
    <button class="btn" data-x="play">&#9654; Preview</button><button class="btn" data-x="up">Up</button><button class="btn" data-x="down">Down</button><button class="btn no" data-x="rm">Remove</button></div>`).join('');
  list.querySelectorAll('.mo').forEach(row=>{const mid=row.dataset.mid,m=()=>COL.moments.find(x=>x.mid===mid);
    row.querySelectorAll('[data-x]').forEach(b=>b.onclick=async()=>{const x=b.dataset.x,mm=m(),i=COL.moments.indexOf(mm);
      if(x==='play'){colPlay([mm]);return}
      if(x==='rm'){if(confirm('Remove this Short from the collection?'))await colDo('remove',{mid});return}
      const j=x==='up'?i-1:i+1;if(j<0||j>=COL.moments.length)return;const o=COL.moments.map(q=>q.mid);[o[i],o[j]]=[o[j],o[i]];await colDo('order',{order:o})});
    row.addEventListener('dragstart',e=>{row.classList.add('drag');e.dataTransfer.setData('text/plain',mid)});
    row.addEventListener('dragend',()=>row.classList.remove('drag'));
    row.addEventListener('dragover',e=>{e.preventDefault();row.classList.add('over')});
    row.addEventListener('dragleave',()=>row.classList.remove('over'));
    row.addEventListener('drop',async e=>{e.preventDefault();row.classList.remove('over');const from=e.dataTransfer.getData('text/plain');if(!from||from===mid)return;
      const o=COL.moments.map(q=>q.mid).filter(q=>q!==from);o.splice(o.indexOf(mid)+(COL.moments.findIndex(q=>q.mid===from)<COL.moments.findIndex(q=>q.mid===mid)?1:0),0,from);await colDo('order',{order:o})})})}
function colPlay(list){colQueue=list.slice();$('colPlayer').style.display='block';colNext();$('colPlayer').scrollIntoView({behavior:'smooth',block:'nearest'})}
function colNext(){const v=$('colVid'),m=colQueue&&colQueue.shift();document.querySelectorAll('#colList .mo').forEach(r=>r.classList.toggle('on',!!m&&r.dataset.mid===m.mid));
  if(!m){v.pause();colStopAt=null;$('colNow').textContent='';return}
  const horiz=(COL.shape||'vertical')==='horizontal'&&m.file,src=`/comp/${COL.id}/${horiz?m.file:m.vfile}`,from=horiz?m.a:0;colStopAt=horiz?m.b:m.vdur-0.05;
  $('colNow').textContent=`Clip ${COL.moments.findIndex(x=>x.mid===m.mid)+1}: ${m.title}`;
  const go=()=>{v.currentTime=from;v.play().catch(()=>{})};
  if(!v.src.endsWith(src)){v.preload='auto';v.src=src;v.addEventListener('loadedmetadata',go,{once:true});v.load()}else go()}
$('colVid').addEventListener('timeupdate',()=>{if(colStopAt!==null&&$('colVid').currentTime>=colStopAt){colStopAt=null;if(colQueue&&colQueue.length)colNext();else $('colVid').pause()}});
$('colVid').addEventListener('ended',()=>{if(colQueue&&colQueue.length)colNext()});
$('colStop').onclick=()=>{colQueue=null;colStopAt=null;$('colVid').pause();$('colPlayer').style.display='none';document.querySelectorAll('#colList .mo.on').forEach(r=>r.classList.remove('on'))};
$('colPlayAll').onclick=()=>{if(COL)colPlay(COL.moments)};
$('colPick').onchange=()=>{setCol($('colPick').value);$('colStop').click();loadCols()};
$('colNew').onclick=newCol;$('colRen').onclick=()=>{const n=prompt('New name:',COL.name);if(n)colDo('settings',{name:n})};
$('colDel').onclick=()=>{if(confirm(`Delete "${COL.name}" and its ${COL.moments.length} saved Shorts? (Montages you already exported stay.)`))colDo('delete')};
$('colGoal').onchange=()=>{const m=+$('colGoal').value;if(m>0)colDo('settings',{goal:m*60})};
$('colShuffle').onclick=()=>colDo('shuffle');$('colOldest').onclick=()=>colDo('oldest');
document.querySelectorAll('#colShape button').forEach(b=>b.onclick=()=>{$('colStop').click();colDo('settings',{shape:b.dataset.v})});
document.querySelectorAll('#colTr button').forEach(b=>b.onclick=()=>colDo('settings',{transition:b.dataset.v}));
document.querySelectorAll('#colNum button').forEach(b=>b.onclick=()=>colDo('settings',{numbers:b.dataset.v==='1'}));
async function colExport(premiere){if(!COL||!COL.moments.length){toast('Add some Shorts first.');return}
  const r=await api('/api/run',{kind:'compexport',comp:COL.id,premiere});lastJobKey='running';
  toast(r.queued?'<b>In line:</b> the export starts when the current job finishes.':'<b>Exporting...</b> progress shows on the Make Shorts tab.');poll()}
$('colExport').onclick=()=>colExport(false);$('colPrem').onclick=()=>colExport(true);
// "+ Collection" on Review cards
let colAdding={};
function colButton(c){return `<span class="colwrap"><button class="btn colbtn" data-job="${esc(c.job)}" data-id="${esc(c.id)}">+ Collection</button></span>`}
function markCols(){document.querySelectorAll('.colbtn').forEach(b=>{const key=b.dataset.job+':'+b.dataset.id,inn=COLMEM[key]||[];
  if(colAdding[key]){b.textContent='Adding...';b.classList.remove('added');b.disabled=true;return}
  b.disabled=false;b.textContent=inn.length?'In: '+inn.map(x=>x.name).join(', '):'+ Collection';b.classList.toggle('added',!!inn.length);b.title=inn.length?'Add to another collection':''})}
function closeColMenu(){document.querySelectorAll('.colmenu').forEach(m=>m.remove())}
document.addEventListener('click',async e=>{const b=e.target.closest('.colbtn');const item=e.target.closest('.colmenu button');
  if(item){const {job,id,col}=item.dataset;closeColMenu();let target=col;
    if(target==='__new'){target=await newCol();if(!target)return}
    colAdding[job+':'+id]=true;markCols();
    try{const r=await api('/api/run',{kind:'coladd',comp:target,job,id});lastJobKey='running';if(r.queued)toast('<b>In line:</b> added when the current job finishes.');poll()}
    catch(err){delete colAdding[job+':'+id];markCols()}return}
  if(!b){if(!e.target.closest('.colmenu'))closeColMenu();return}
  closeColMenu();const key=b.dataset.job+':'+b.dataset.id,inn=(COLMEM[key]||[]).map(x=>x.id);
  const menu=document.createElement('div');menu.className='colmenu';
  menu.innerHTML=COLS.map(c=>`<button data-job="${esc(b.dataset.job)}" data-id="${esc(b.dataset.id)}" data-col="${esc(c.id)}" class="${inn.includes(c.id)?'in':''}" ${inn.includes(c.id)?'disabled':''}>${esc(c.name)} (${c.count})${inn.includes(c.id)?' - added':''}</button>`).join('')+
    `<button class="new" data-job="${esc(b.dataset.job)}" data-id="${esc(b.dataset.id)}" data-col="__new">+ New collection...</button>`;
  b.parentElement.appendChild(menu)});

// ---------- where a Short came from in the stream (cards + History) ----------
const tcode=t=>{t=Math.max(0,Math.floor(t||0));const h=Math.floor(t/3600),m=Math.floor(t%3600/60),s=t%60;return (h?h+':'+String(m).padStart(2,'0'):m)+':'+String(s).padStart(2,'0')};
const fromCode=v=>{const p=String(v).trim().split(':').map(Number);if(p.some(isNaN)||!p.length)return null;return p.reduce((a,x)=>a*60+x,0)};
const niceDate=d=>{if(!d)return'';const x=new Date(d+(d.length===10?'T12:00':''));return isNaN(x)?d:x.toLocaleDateString([], {month:'short',day:'numeric'})};
function streamLine(c){if(c.stream_start==null)return'';
  const where=c.stream_title?`"${esc(c.stream_title)}"`:'';const day=c.stream_date?`${niceDate(c.stream_date)} stream`:'';
  return `<div class="st-line tiny"><span class="mute">From the stream at</span> <span class="tc">${tcode(c.stream_start)} - ${tcode(c.stream_end)}</span>
    <div class="mute">${[where,day].filter(Boolean).join(' &middot; ')}</div></div>
    <div class="st-acts">${c.stream_link?`<a class="btn" href="${esc(c.stream_link)}" target="_blank" rel="noopener">Open stream there &#8599;</a>`:''}
    <button class="btn" data-copy="${esc(tcode(c.stream_start)+' - '+tcode(c.stream_end)+(c.stream_link?'  '+c.stream_link:''))}">Copy time</button></div>`}
document.addEventListener('click',async e=>{const b=e.target.closest('[data-copy]');if(!b)return;
  try{await navigator.clipboard.writeText(b.dataset.copy);toast('<b>Copied:</b> '+esc(b.dataset.copy))}catch(err){prompt('Copy this:',b.dataset.copy)}});
let HIST=[],hFilter='';
async function loadHistory(){HIST=await api('/api/history');drawHistory()}
function drawHistory(){const q=$('hSearch').value.trim().toLowerCase();
  const rows=HIST.filter(h=>(!hFilter||h.status===hFilter)&&(!q||(h.title+' '+h.transcript+' '+(h.stream_title||'')).toLowerCase().includes(q)));
  const verb={uploaded:'Uploaded',exported:'Exported',rejected:'Rejected'};
  $('hList').innerHTML=rows.length?rows.map(h=>`<div class="hrow">${h.thumb?`<img src="/history_thumb/${esc(h.thumb)}" alt="" loading="lazy">`:'<div class="noimg"></div>'}
    <div class="tt"><b title="${esc(h.title)}">${esc(h.title)}</b><span class="pill ${h.status}">${verb[h.status]||h.status} ${niceDate((h.when||'').slice(0,10))}</span>
      <div class="tiny"><span class="tc">${tcode(h.stream_start)} - ${tcode(h.stream_end)}</span> <span class="mute">${h.stream_title?'in "'+esc(h.stream_title)+'"':''}${h.stream_date?' ('+niceDate(h.stream_date)+' stream)':''}</span></div></div>
    <div class="st-acts">${h.stream_link?`<a class="btn" href="${esc(h.stream_link)}" target="_blank" rel="noopener">Open stream there &#8599;</a>`:''}
      <button class="btn" data-copy="${esc(tcode(h.stream_start)+' - '+tcode(h.stream_end)+(h.stream_link?'  '+h.stream_link:''))}">Copy time</button>
      ${h.youtube_id?`<a class="btn" href="https://youtube.com/shorts/${esc(h.youtube_id)}" target="_blank" rel="noopener">Watch the Short &#8599;</a>`:''}
      ${h.available?`<button class="btn" data-shot="${esc(h.key)}">Screenshot</button>`:''}</div></div>`).join('')
    :`<div class="empty">${HIST.length?'Nothing matches that search.':'Shorts show up here once they\'re uploaded, exported or rejected.'}</div>`;
  $('hList').querySelectorAll('[data-shot]').forEach(b=>b.onclick=async()=>{const h=HIST.find(x=>x.key===b.dataset.shot);
    const v=prompt('Screenshot the stream at what time? (like 1:42:15)',tcode(h.stream_start));if(v==null)return;const at=fromCode(v);
    if(at==null){toast('That time didn\'t look right - use something like 1:42:15.');return}
    try{const r=await api('/api/history_shot',{key:h.key,at});
      toast(`<b>Screenshot saved:</b> ${esc(r.name)}<br><span class="tiny mute">${esc(r.folder)}</span><br><button class="link" onclick="api('/api/open_folder',{path:${esc(JSON.stringify(r.folder)).replace(/'/g,'&#39;')}})">Open the folder</button> &nbsp; <button class="link" onclick="pickFolder('screenshot_folder')">Change folder</button>`)}catch(e){}})}
$('hSearch').oninput=drawHistory;
document.querySelectorAll('#hFilter button').forEach(b=>b.onclick=()=>{hFilter=b.dataset.v;document.querySelectorAll('#hFilter button').forEach(x=>x.classList.toggle('on',x===b));drawHistory()});

// ---------- folder pickers (Settings + "Change folder" on screenshot messages) ----------
const shotFolder=()=>S.settings.screenshot_folder||((S.settings.export_folder||S.default_export)+'\\Screenshots');
async function pickFolder(key){const start=key==='screenshot_folder'?shotFolder():key==='title_folder'?tcTitleFolder():(S.settings.export_folder||S.default_export);
  const title=key==='screenshot_folder'?'Where should screenshots go?':key==='title_folder'?'Where should title cards go?':'Where should exports go?';
  toast('Pick a folder in the window that just opened (it may be behind this one).');
  const r=await api('/api/pick_folder',{start,title}).catch(()=>null);
  if(!r||!r.path){toast('No folder picked - nothing changed.');return}
  S.settings[key]=r.path;const inp=$('s_'+key);if(inp)inp.value=r.path;await api('/api/setting',{[key]:r.path});
  toast(`<b>${key==='screenshot_folder'?'Screenshots':key==='title_folder'?'Title cards':'Exports'} now go to:</b><br><span class="tiny">${esc(r.path)}</span>`);
  if($('tcFolder'))$('tcFolder').textContent=tcTitleFolder();
  if($('expFolder'))$('expFolder').textContent=S.settings.export_folder||S.default_export}
function openSetFolder(key){const v=($('s_'+key)&&$('s_'+key).value.trim())||(key==='screenshot_folder'?shotFolder():key==='title_folder'?tcTitleFolder():(S.settings.export_folder||S.default_export));
  api('/api/open_folder',{path:v})}

// ---------- YouTube Shorts safe zones (on every 9:16 preview) ----------
// On a 1080x1920 Short: top ~300 px (search/sound/menu), bottom ~480 px (avatar, subscribe, title, audio),
// right ~165 px (like/comment/share), left ~65 px are covered or crowded. The rest is safe for faces and text.
function safeZones(c){const x=c.getContext('2d'),W=c.width,H=c.height,k=W/1080,
  t=SAFE_M.top*k,b=SAFE_M.bottom*k,r=SAFE_M.right*k,l=SAFE_M.left*k;
  x.save();x.fillStyle='rgba(216,90,48,0.38)';
  x.fillRect(0,0,W,t);x.fillRect(0,H-b,W,b);x.fillRect(0,t,l,H-t-b);x.fillRect(W-r,t,r,H-t-b);
  x.strokeStyle='#5DCAA5';x.lineWidth=Math.max(1.5,3*k);x.setLineDash([10*k+4,6*k+3]);x.strokeRect(l,t,W-l-r,H-t-b);x.setLineDash([]);
  x.fillStyle='rgba(255,255,255,0.55)';                       // where YouTube's buttons sit
  for(let i=0;i<5;i++){x.beginPath();x.arc(W-r/2,t+(H-t-b)*0.45+i*(H-t-b)*0.12,Math.max(3,26*k),0,7);x.fill()}
  [W-60*k,W-130*k,W-200*k].forEach(cx=>{x.beginPath();x.arc(cx,t*0.45,Math.max(2.5,18*k),0,7);x.fill()});
  x.beginPath();x.arc(l+40*k,H-b+90*k,Math.max(3,30*k),0,7);x.fill();
  x.fillRect(l+90*k,H-b+80*k,260*k,18*k);x.fillRect(l,H-b+170*k,640*k,18*k);x.fillRect(l,H-b+230*k,420*k,18*k);
  if(W>=400){x.font=`600 ${Math.round(26*k*1.4)}px Segoe UI, sans-serif`;x.textAlign='center';x.fillStyle='#fff';
    x.shadowColor='#000';x.shadowBlur=6;x.fillText('Safe zone',l+(W-l-r)/2,t+26*k*1.6)}
  x.restore()}
document.querySelectorAll('.safeTog').forEach(t=>{t.checked=SAFE;t.onchange=()=>{SAFE=t.checked;try{localStorage.setItem('pc_safe',SAFE?'1':'0')}catch(e){}
  document.querySelectorAll('.safeTog').forEach(o=>o.checked=SAFE);
  try{drawCal()}catch(e){}try{if(E){liveDraw();frDraw()}}catch(e){}}});

// ---------- title cards ----------
let TC=null,tcTimer=null,tcReq=0,tcVariant=0,tcShorts=[],tcUrl=null;
const tcTitleFolder=()=>S.settings.title_folder||((S.settings.export_folder||S.default_export)+'\\Title cards');
try{TC=JSON.parse(localStorage.getItem('pc_tc')||'null')}catch(e){}
function tcSaveLocal(){try{localStorage.setItem('pc_tc',JSON.stringify(TC))}catch(e){}}
async function loadTitles(pick){const [rev,apv]=await Promise.all([api('/api/clips'),api('/api/plan').catch(()=>[])]);
  tcShorts=rev.map(c=>({job:c.job,id:c.id,title:c.title,poster:`/media/${c.job}/${c.poster}`,where:'Review'}))
    .concat((apv||[]).map(p=>({job:p.job,id:p.id,title:p.title,poster:p.poster,where:'Approved'})));
  $('tcShort').innerHTML='<option value="">Pick a Short (optional)</option>'+tcShorts.map((c,i)=>`<option value="${i}">${esc(c.where)}: ${esc(c.title)}</option>`).join('');
  if(pick){const i=tcShorts.findIndex(c=>c.job===pick.job&&c.id===pick.id);if(i>=0)$('tcShort').value=String(i)}
  $('tcFolder').textContent=tcTitleFolder();
  if(!TC){TC=await api('/api/titlecard/draft',{title:'Peanut was not ready for this GTA 6 mission!',variant:0})}
  if(pick){tcVariant=0;TC=await api('/api/titlecard/draft',{title:pick.title,variant:0})}
  tcBg();tcDraw()}
function openTitles(c){show('titles');loadTitles(c)}
function tcBg(){const st=$('tcStage'),i=$('tcShort').value,s=tcShorts[+i],useShort=(TC.bg||'chk')==='short'&&s;
  st.classList.toggle('chk',!useShort);st.style.backgroundImage=useShort?`url("${s.poster}")`:'';
  document.querySelectorAll('#tcBg button').forEach(b=>b.classList.toggle('on',b.dataset.v===(TC.bg||'chk')))}
function tcDraw(){const box=$('tcLines');
  box.innerHTML=TC.lines.map((l,i)=>`<div class="tc-line" data-i="${i}"><div class="row">
    <input type="text" value="${esc(l.text)}" maxlength="40" data-k="text">
    <span class="seg">${['white','yellow','red'].map(v=>`<button data-k="color" data-v="${v}" class="${l.color===v?'on':''}">${v[0].toUpperCase()+v.slice(1)}</button>`).join('')}</span>
    <button class="btn mini" data-mv="-1" title="Move up">&uarr;</button><button class="btn mini" data-mv="1" title="Move down">&darr;</button><button class="btn mini no" data-rm="1" title="Remove">&times;</button></div>
    <div class="row" style="margin-top:6px"><span class="tiny mute">Size</span><span class="seg">${['S','M','L'].map(v=>`<button data-k="size" data-v="${v}" class="${l.size===v?'on':''}">${v}</button>`).join('')}</span>
    <span class="tiny mute" style="margin-left:8px">Extra</span><span class="seg">${[['none','None'],['box','Red box'],['swoosh','Swoosh']].map(([v,n])=>`<button data-k="extra" data-v="${v}" class="${l.extra===v?'on':''}">${n}</button>`).join('')}</span></div></div>`).join('')
    ||'<div class="empty">No lines yet - press <b>+ Line</b> or <b>From the Short\'s title</b>.</div>';
  box.querySelectorAll('.tc-line').forEach(row=>{const i=+row.dataset.i;
    row.querySelector('input').oninput=e=>{TC.lines[i].text=e.target.value;tcRender()};
    row.querySelectorAll('[data-k][data-v]').forEach(b=>b.onclick=()=>{TC.lines[i][b.dataset.k]=b.dataset.v;tcDraw()});
    row.querySelectorAll('[data-mv]').forEach(b=>b.onclick=()=>{const j=i+(+b.dataset.mv);if(j<0||j>=TC.lines.length)return;[TC.lines[i],TC.lines[j]]=[TC.lines[j],TC.lines[i]];tcDraw()});
    row.querySelector('[data-rm]').onclick=()=>{TC.lines.splice(i,1);tcDraw()}});
  document.querySelectorAll('#tcBrush button').forEach(b=>b.classList.toggle('on',b.dataset.v===(TC.brush?'1':'0')));
  document.querySelectorAll('#tcPos button').forEach(b=>b.classList.toggle('on',b.dataset.v===(TC.position||'middle')));
  $('tcSlant').value=TC.slant??0.05;$('tcGap').value=TC.gap??-0.1;$('tcAdd').disabled=TC.lines.length>=8;tcRender()}
function tcRender(){tcSaveLocal();clearTimeout(tcTimer);$('tcBusy').style.display='block';tcTimer=setTimeout(async()=>{const n=++tcReq;
  try{const r=await fetch('/api/titlecard/preview',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({spec:TC})});
    if(!r.ok){const e=await r.json().catch(()=>({}));toast(esc(e.error||'Couldn\'t draw the preview.'));return}
    const b=await r.blob();if(n!==tcReq)return;if(tcUrl)URL.revokeObjectURL(tcUrl);tcUrl=URL.createObjectURL(b);$('tcImg').src=tcUrl}
  catch(e){}finally{if(n===tcReq)$('tcBusy').style.display='none'}},250);tcSafe()}
function tcSafe(){const c=$('tcSafe');c.getContext('2d').clearRect(0,0,c.width,c.height);if(SAFE)safeZones(c)}
document.querySelectorAll('.safeTog').forEach(t=>t.addEventListener('change',tcSafe));
$('tcFrom').onclick=async()=>{const s=tcShorts[+$('tcShort').value];if(!s){toast('Pick a Short in the list first.');return}
  tcVariant=0;const bg=TC.bg;TC=await api('/api/titlecard/draft',{title:s.title,variant:0});TC.bg=bg;tcDraw()};
$('tcShuffle').onclick=async()=>{const texts=TC.lines.map(l=>l.text).filter(t=>t.trim());if(!texts.length)return;   // keeps your words, new colours/extras
  tcVariant++;const bg=TC.bg,pos=TC.position,slant=TC.slant,gap=TC.gap;TC=await api('/api/titlecard/draft',{title:'',variant:tcVariant,texts});
  Object.assign(TC,{bg,position:pos,slant,gap});tcDraw()};
$('tcAdd').onclick=()=>{TC.lines.push({text:'NEW LINE',color:'white',size:'L',extra:'none'});tcDraw();const ins=$('tcLines').querySelectorAll('input');const last=ins[ins.length-1];last.focus();last.select()};
$('tcClear').onclick=()=>{if(confirm('Remove every line?')){TC.lines=[];tcDraw()}};
$('tcShort').onchange=()=>tcBg();
document.querySelectorAll('#tcBrush button').forEach(b=>b.onclick=()=>{TC.brush=b.dataset.v==='1';tcDraw()});
document.querySelectorAll('#tcPos button').forEach(b=>b.onclick=()=>{TC.position=b.dataset.v;tcDraw()});
document.querySelectorAll('#tcBg button').forEach(b=>b.onclick=()=>{TC.bg=b.dataset.v;if(b.dataset.v==='short'&&!tcShorts[+$('tcShort').value])toast('Pick a Short in the list to see it behind the text.');tcBg();tcSaveLocal()});
$('tcSlant').oninput=()=>{TC.slant=+$('tcSlant').value;tcRender()};$('tcGap').oninput=()=>{TC.gap=+$('tcGap').value;tcRender()};
$('tcSave').onclick=async()=>{try{const r=await api('/api/titlecard/save',{spec:TC});
  toast(`<b>Title card saved:</b> ${esc(r.name)}<br><span class="tiny mute">${esc(r.folder)}</span><br><button class="link" onclick="api('/api/open_folder',{path:${esc(JSON.stringify(r.folder)).replace(/'/g,'&#39;')}})">Open the folder</button> &nbsp; <button class="link" onclick="pickFolder('title_folder')">Change folder</button>`)}catch(e){}};
$('tcCopy').onclick=async()=>{try{const b=await (await fetch($('tcImg').src)).blob();await navigator.clipboard.write([new ClipboardItem({'image/png':b})]);
  toast('<b>Copied</b> - paste it where you need it (this copy is preview size; use Save for the full 1080x1920 picture).')}catch(e){toast('Copying pictures isn\'t allowed here - use Save PNG instead.')}};

// ---------- storage (Settings) ----------
const GBs=b=>b>=1e9?(b/1e9).toFixed(b>=1e11?0:1)+' GB':b>=1e6?Math.round(b/1e6)+' MB':Math.round(b/1e3)+' KB';
const ST_COL={downloads:'#e5484d',shorts:'#ffc93c',exports:'#3fa9ff',compilations:'#2fb36d'};
let STO=null;
async function loadStorage(){$('stItems').innerHTML='<div class="tiny mute">Measuring...</div>';STO=await api('/api/storage');
  $('stRoot').textContent='Peanut Clipper folder: '+STO.root;$('stTotal').textContent=GBs(STO.total);
  $('stFree').textContent=`used - ${GBs(STO.free)} free on ${STO.drive}`;
  const tot=Math.max(1,STO.total);
  $('stBar').innerHTML=STO.areas.map(a=>`<span style="width:${a.size/tot*100}%;background:${ST_COL[a.key]}" title="${esc(a.name)} ${GBs(a.size)}"></span>`).join('');
  $('stLegend').innerHTML=STO.areas.map(a=>`<span><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:${ST_COL[a.key]};margin-right:4px"></span>${esc(a.name)} ${GBs(a.size)} <button class="link" onclick="api('/api/open_folder',{path:${esc(JSON.stringify(a.path)).replace(/'/g,'&#39;')}})">open</button></span>`).join(' &nbsp; ');
  const items=STO.items.filter(i=>i.size>0);
  $('stItems').innerHTML=items.length?items.map((it,k)=>`<div class="st-item"><span><b>${esc(it.name)}</b> <span class="tiny mute">- ${esc(it.date)}${it.note?', '+esc(it.note):''}${it.busy?' (recording now)':''}</span></span>
    <span class="sz">${GBs(it.size)}</span>${it.busy?'<span></span>':`<button class="btn no" data-del="${k}">Delete</button>`}</div>`).join('')
    :'<div class="tiny mute">Nothing big in here.</div>';
  $('stItems').querySelectorAll('[data-del]').forEach(b=>b.onclick=async()=>{const it=items[+b.dataset.del];
    const warn=it.waiting||/still in Review/.test(it.note||'')?'\n\nSome Shorts from it are still waiting in Review or Approved - they won\'t be re-cuttable after this.':'';
    if(!confirm(`Delete ${it.name} (${GBs(it.size)})?${warn}`))return;
    try{await api('/api/storage/delete',{item:it});toast(`<b>Deleted:</b> ${esc(it.name)} - freed ${GBs(it.size)}`);loadStorage();if(typeof loadClips==='function')loadClips()}catch(e){}})}
$('stRefresh').onclick=loadStorage;
$('stClean').onclick=async()=>{const s=await api('/api/storage');const p=s.plan;
  if(!p.length){toast('Nothing to clean up right now - everything is within your Auto-delete rules.');return}
  const sum=p.reduce((a,i)=>a+i.size,0);
  const list=p.slice(0,15).map(i=>`- ${i.name} (${GBs(i.size)}) - ${i.why}`).join('\n')+(p.length>15?`\n...and ${p.length-15} more`:'');
  if(!confirm(`Clean up ${p.length} item${p.length===1?'':'s'} and free about ${GBs(sum)}?\n\n${list}`))return;
  const r=await api('/api/storage/clean',{});toast(`<b>Cleaned up:</b> ${r.count} item${r.count===1?'':'s'}, freed ${GBs(r.freed)}`);loadStorage()};

// ---------- record live ----------
let LV={};
const gb=b=>b>=1e9?(b/1e9).toFixed(1)+' GB':Math.round(b/1e6)+' MB';
async function liveTick(){let st;try{st=await api('/api/live')}catch(e){return}LV=st;const s=st.state||'idle';
  const rec=['checking','waiting','recording','saving'].includes(s);const done=['done','making'].includes(s)&&st.file;
  $('liveIdle').style.display=(!rec&&!done&&s!=='crashed')?'':'none';$('liveRec').style.display=(rec||s==='crashed')?'':'none';$('liveDone').style.display=done?'':'none';
  if(!rec&&!done&&s!=='crashed'){$('liveMsg').textContent=st.message||(st.last_check?'Last checked '+new Date(st.last_check*1000).toLocaleTimeString([], {hour:'numeric',minute:'2-digit'}):'')}
  if(rec||s==='crashed'){const head={checking:"Checking if he's live...",waiting:'Waiting for him to go live',recording:'Recording live',saving:'Saving the recording...',crashed:'Recording stopped unexpectedly'}[s];
    $('liveHead').textContent=head;$('liveDot').style.display=s==='recording'?'':'none';$('liveTitle').textContent=st.title?'"'+st.title+'"':'';
    $('liveStats').style.display=(s==='recording'||s==='saving'||(s==='crashed'&&st.bytes))?'':'none';
    $('lvTime').textContent=T(st.seconds||0);$('lvSize').textContent=gb(st.bytes||0);$('lvChat').textContent=(st.chat||0).toLocaleString();
    $('lvFree').textContent=st.free_gb!=null?st.free_gb+' GB':'-';$('lvFree').style.color=st.free_gb!=null&&st.free_gb<30?'var(--no)':'';
    $('liveStop').style.display=s==='saving'?'none':'';
    $('liveStop').textContent=s==='crashed'?(st.bytes?'Save what was recorded':'OK'):s==='waiting'||s==='checking'?'Stop waiting':'Stop recording';
    $('liveNote').textContent=s==='waiting'?`Checking every 5 min - not live yet${st.last_check?' (last checked '+new Date(st.last_check*1000).toLocaleTimeString([], {hour:'numeric',minute:'2-digit'})+')':''}. Keep the PC on.`
      :s==='crashed'?'The recorder stopped (was the PC asleep or turned off?). What was recorded so far can still be saved.'
      :s==='saving'?'Putting the recording together - this takes a minute or two.':'Keep the PC on and online. You can use the rest of the app while it records.'}
  if(done){$('lvDoneHead').textContent='Recording saved';
    $('lvDoneInfo').textContent=`${T(st.seconds||0)} - ${gb(st.bytes||0)} - ${(st.chat||0).toLocaleString()} chat messages`;
    const making=s==='making';$('lvMakeBar').style.display=making?'':'none';if(making)$('lvMakeFill').style.width=(st.made_pct||0)+'%';
    $('lvMakeNote').textContent=making?`"Make Shorts as soon as he ends" was on, so finding moments already started: ${st.made_label||''} (${st.made_pct||0}%)`
      :st.made===true?'Done - new Shorts are waiting in Review.':st.made===false?(st.made_label||''):st.message||'';
    $('lvMake').disabled=making}}
async function liveStart(wait){const r=await api('/api/live',{action:'start',url:$('liveUrl').value.trim(),wait,from_start:$('liveFromStart').checked,then_make:$('liveThenMake').checked}).catch(()=>null);
  if(r&&r.ok)liveTick()}
$('liveNow').onclick=()=>liveStart(false);$('liveWait').onclick=()=>liveStart(true);
$('liveStop').onclick=async()=>{const s=LV.state;
  if(s==='crashed'){await api('/api/live',{action:LV.bytes?'recover':'clear'});setTimeout(liveTick,800);return}
  if(s==='recording'&&!confirm('Stop recording? What was recorded so far is saved.'))return;
  await api('/api/live',{action:'stop'});setTimeout(liveTick,800)};
$('lvMake').onclick=()=>{upClear();$('url').value=LV.url||'';$('part').checked=false;$('partBox').style.display='none';$('go').click()};
$('lvSearch').onclick=()=>{$('kwUrl').value=LV.url||'';$('kwWords').focus();$('kwWords').scrollIntoView({behavior:'smooth',block:'center'})};
$('lvAgain').onclick=async()=>{await api('/api/live',{action:'clear'});liveTick()};
[['liveFromStart','live_from_start'],['liveThenMake','live_then_make'],['liveInAuto','live_in_auto']].forEach(([id,k])=>
  $(id).onchange=()=>{S.settings[k]=$(id).checked;api('/api/setting',{[k]:$(id).checked})});
function liveFill(){if(!S||!S.settings)return;$('liveFromStart').checked=S.settings.live_from_start!==false;
  $('liveThenMake').checked=S.settings.live_then_make!==false;$('liveInAuto').checked=!!S.settings.live_in_auto}

// ---------- a video file in the "From a stream or your own video" box ----------
const UP={file:null,xhr:null,path:'',makeWhenDone:false};
function upSize(b){return b>=2**30?(b/2**30).toFixed(1)+' GB':Math.max(1,Math.round(b/2**20))+' MB'}
function upDraw(state){$('upPicked').style.display=UP.file?'':'none';$('upBarWrap').style.display=UP.xhr?'':'none';
  if(UP.file)$('upName').textContent=`${UP.file.name} (${upSize(UP.file.size)})`;if(state!==undefined)$('upState').innerHTML=state;
  $('url').placeholder=UP.file?'Using the video below - remove it to paste a link instead':'Paste a stream link, or drop a video file here'}
function upDiscard(path){if(path)api('/api/video_upload_discard',{path}).catch(()=>{})}
function upClear(){if(UP.xhr){const x=UP.xhr;UP.xhr=null;x.abort()}upDiscard(UP.path);UP.file=null;UP.path='';UP.makeWhenDone=false;upDraw('')}
async function upStart(f){
  if(!f)return;upClear();
  try{await api('/api/video_upload_check',{name:f.name,size:f.size})}catch(e){return}
  UP.file=f;$('url').value='';$('upFill').style.width='0%';
  const x=new XMLHttpRequest();UP.xhr=x;const t0=Date.now();upDraw('uploading...');
  x.upload.onprogress=e=>{if(!e.lengthComputable||UP.xhr!==x)return;const fr=e.loaded/e.total,el=(Date.now()-t0)/1000;
    const left=fr>0.02?el/fr-el:null;const eta=left==null?'':left<60?`, about ${Math.max(1,Math.round(left))} s left`:`, about ${Math.round(left/60)} min left`;
    $('upFill').style.width=(fr*100).toFixed(1)+'%';upDraw(`uploading ${Math.floor(fr*100)}%${eta}`)};
  x.onload=()=>{if(UP.xhr!==x)return;UP.xhr=null;let j={};try{j=JSON.parse(x.responseText)}catch(e){}
    if(x.status!==200||!j.path){UP.file=null;upDraw('');toast(esc(j.error||'The upload didn\'t work. Try again.'));return}
    UP.path=j.path;upDraw('ready - press Make Shorts');if(UP.makeWhenDone){UP.makeWhenDone=false;$('go').click()}};
  x.onerror=()=>{if(UP.xhr!==x)return;UP.xhr=null;UP.file=null;upDraw('');toast('The upload stopped. Is Peanut Clipper still open? Try again.')};
  x.open('POST','/api/video_upload?name='+encodeURIComponent(f.name));x.send(f)}
$('upPick').onclick=()=>$('upFile').click();
$('upFile').onchange=e=>{upStart(e.target.files[0]);e.target.value=''};
$('upRemove').onclick=upClear;
$('url').addEventListener('input',()=>{if(UP.file&&$('url').value.trim())upClear()});
const srcCard=$('srcCard');
srcCard.addEventListener('dragover',e=>{e.preventDefault();srcCard.classList.add('over')});
srcCard.addEventListener('dragleave',e=>{if(!srcCard.contains(e.relatedTarget))srcCard.classList.remove('over')});
srcCard.addEventListener('drop',e=>{e.preventDefault();srcCard.classList.remove('over');if(e.dataTransfer.files[0])upStart(e.dataTransfer.files[0])});
window.addEventListener('dragover',e=>e.preventDefault());window.addEventListener('drop',e=>e.preventDefault());
window.addEventListener('beforeunload',e=>{if(UP.xhr){e.preventDefault();e.returnValue=''}});

// ---------- Make: Shorts / Long video / Both ----------
function mkDraw(){if(!S||!S.settings)return;const m=S.settings.make_mode||'shorts',len=String(S.settings.long_minutes||8);
  document.querySelectorAll('#mkMode button').forEach(b=>b.classList.toggle('on',b.dataset.v===m));
  document.querySelectorAll('#mkLen button').forEach(b=>b.classList.toggle('on',b.dataset.v===len));
  $('mkLenBox').style.display=m==='shorts'?'none':'';$('mkLenNote').style.display=m==='shorts'?'none':'';
  $('go').textContent=m==='long'?'Make long video':m==='both'?'Make both':'Make Shorts'}
document.querySelectorAll('#mkMode button').forEach(b=>b.onclick=()=>{S.settings.make_mode=b.dataset.v;mkDraw();api('/api/setting',{make_mode:b.dataset.v})});
document.querySelectorAll('#mkLen button').forEach(b=>b.onclick=()=>{S.settings.long_minutes=+b.dataset.v;mkDraw();api('/api/setting',{long_minutes:+b.dataset.v})});
async function openLastLong(){const r=await api('/api/last_longvid').catch(()=>null);if(!r||!r.id)return;setCur(r.id);show('comps');await loadComps()}

// ---------- auto-clip folder ----------
let INB=null;
function inbDraw(){const s=INB;if(!s)return;
  $('inbOn').checked=s.enabled;if(document.activeElement!==$('inbFolder'))$('inbFolder').value=s.folder;
  $('inbMove').checked=s.after==='move';$('inbDel').checked=s.after==='delete';
  if($('inbLayout').value!==s.layout&&document.activeElement!==$('inbLayout'))$('inbLayout').value=s.layout;
  const parts=[];
  if(!s.enabled)parts.push('Off - turn it on to start watching the folder.');
  else if(!s.exists)parts.push("That folder doesn't exist yet - press Open to make it.");
  if(s.making)parts.push(`Making Shorts from <b>${esc(s.making)}</b> now`);
  parts.push(`Waiting: ${s.waiting.length}${s.waiting.length?' ('+s.waiting.slice(0,3).map(esc).join(', ')+(s.waiting.length>3?', ...':'')+')':''}`);
  parts.push(`Done: ${s.done}`);
  if(s.last)parts.push(s.last.status==='done'?`Last one: <b>${esc(s.last.name)}</b>, ${s.last.shorts} Short${s.last.shorts===1?'':'s'} in Review`:s.last.status==='failed'?`Last one: <b>${esc(s.last.name)}</b> didn't work`:'');
  $('inbStat').innerHTML=parts.filter(Boolean).join(' · ');
  $('inbFailed').innerHTML=s.failed.map(f=>`<div><span style="color:var(--no)">Couldn't clip ${esc(f.name)}:</span> <span class="mute">${esc(f.why||'')}</span> <button class="link" data-k="${esc(f.key)}">Try again</button></div>`).join('');
  $('inbFailed').querySelectorAll('button[data-k]').forEach(b=>b.onclick=async()=>{INB=await api('/api/inbox',{action:'retry',key:b.dataset.k});inbDraw()})}
async function inbLoad(){try{const r=await fetch('/api/inbox');if(r.ok){INB=await r.json();inbDraw()}}catch(e){}}
async function inbSet(k,v){S.settings[k]=v;await api('/api/setting',{[k]:v});await inbLoad()}
$('inbOn').onchange=async()=>{await inbSet('watch_enabled',$('inbOn').checked);
  if($('inbOn').checked){try{INB=await api('/api/inbox',{action:'make_folder'});inbDraw()}catch(e){}
    toast('<b>Auto-clip folder is on.</b><br><span class="tiny">Videos you put in the folder start a few seconds after they finish copying in.</span>')}};
$('inbFolder').onchange=()=>inbSet('watch_folder',$('inbFolder').value.trim());
$('inbBrowse').onclick=async()=>{toast('Pick a folder in the window that just opened (it may be behind this one).');
  const r=await api('/api/pick_folder',{start:$('inbFolder').value,title:'Which folder should Peanut Clipper watch?'}).catch(()=>null);
  if(!r||!r.path){toast('No folder picked - nothing changed.');return}await inbSet('watch_folder',r.path)};
$('inbOpen').onclick=async()=>{try{INB=await api('/api/inbox',{action:'make_folder'});inbDraw()}catch(e){return}api('/api/open_folder',{path:INB.folder})};
$('inbMove').onchange=()=>inbSet('watch_after',$('inbMove').checked?'move':'keep');
$('inbDel').onchange=()=>{if($('inbDel').checked&&!confirm('Delete each video from the folder once its Shorts are made? (The Shorts stay in Review.)')){$('inbDel').checked=false;return}
  inbSet('watch_after',$('inbDel').checked?'delete':'keep')};
$('inbLayout').onchange=()=>inbSet('watch_layout',$('inbLayout').value);
setInterval(()=>{if(!document.hidden&&$('make').classList.contains('on'))inbLoad()},4000);inbLoad();

// ---------- compilations ----------
let CMP=null,CMPS=[],cmpCur=null,crashWords='';
try{cmpCur=localStorage.getItem('pc_comp')}catch(e){}
const mmss=t=>{t=Math.max(0,Math.round(t));return Math.floor(t/60)+':'+String(t%60).padStart(2,'0')};
const nth=n=>n+(['th','st','nd','rd'][(n%100>10&&n%100<14)?0:Math.min(n%10,4)%4]||'th');
function setCur(id){cmpCur=id;try{localStorage.setItem('pc_comp',id||'')}catch(e){}}
async function loadComps(){const r=await api('/api/comps');CMPS=r.comps;crashWords=r.crash_words;
  if(!CMPS.some(c=>c.id===cmpCur))setCur(CMPS[0]?CMPS[0].id:null);
  const opts=CMPS.map(c=>`<option value="${esc(c.id)}">${esc(c.name)} (${c.count})</option>`).join('');
  $('cmpPick').innerHTML=opts||'<option value="">No compilations yet</option>';
  $('kwComp').innerHTML=opts+'<option value="__new">+ New compilation...</option>';
  if(cmpCur){$('cmpPick').value=cmpCur;$('kwComp').value=cmpCur}
  const prev=CMP&&CMP.id;CMP=cmpCur?await api('/api/comp?id='+encodeURIComponent(cmpCur)).catch(()=>null):null;
  if(!CMP||CMP.id!==prev){ED.sel=CMP&&CMP.moments[0]?CMP.moments[0].mid:null;ED.T=0;edStop(true)}
  drawComp();if(KW)markAdded()}
async function newComp(){const name=prompt('Name for the new compilation:',`GTA crashes vol. ${CMPS.length+1}`);if(!name)return null;
  const c=await api('/api/comp',{action:'new',name,goal:480});setCur(c.id);await loadComps();return c.id}
async function cmpDo(action,extra){if(!CMP)return;const r=await api('/api/comp',Object.assign({id:CMP.id,action},extra||{}));
  if(action==='delete'){setCur(null);CMP=null;await loadComps();return}CMP=r;
  if(!CMP.moments.some(m=>m.mid===ED.sel))ED.sel=CMP.moments[0]?CMP.moments[0].mid:null;
  ED.T=Math.min(ED.T,edTotal());drawComp();refreshCompMenus()}
function refreshCompMenus(){const c=CMPS.find(x=>x.id===CMP.id);if(c){c.count=CMP.moments.length;c.name=CMP.name;
  for(const sel of [$('cmpPick'),$('kwComp')]){const o=[...sel.options].find(o=>o.value===c.id);if(o)o.textContent=`${c.name} (${c.count})`}}
  if(KW)markAdded()}

// ---------- the editor: player + inspector + timeline ----------
const ED={sel:null,T:0,playing:false,cur:-1,addA:null,addB:null,media:[]};
const edLen=m=>m.b-m.a;
function edMap(){let t=0;return(CMP?CMP.moments:[]).map((m,i)=>{const r={m,i,start:t,len:edLen(m)};t+=r.len;return r})}
function edTotal(){return CMP?CMP.moments.reduce((a,m)=>a+edLen(m),0):0}
function edAt(T){const mp=edMap();for(const r of mp)if(T<r.start+r.len-0.01)return r;return mp[mp.length-1]||null}
function edSelM(){return CMP&&CMP.moments.find(m=>m.mid===ED.sel)}
function edBoxes(){const src=(typeof LY!=='undefined'&&LY)||S.layouts;const l=(src.layouts||[]).find(x=>x.id===src.default)||(src.layouts||[])[0]||{};
  return{cam:l.avatar||{x:.7,y:.5,w:.3,h:.5},game:l.gameplay||{x:.15,y:0,w:.7,h:1}}}
function edZoomCss(zoom){if(zoom!=='cam'&&zoom!=='game')return'';const b=edBoxes()[zoom],W=1920,H=1080;
  const sa=(CMP.source_w||16)/(CMP.source_h||9);let cw,ch;if(sa>=W/H){cw=W;ch=W/sa}else{cw=H*sa;ch=H}
  const ox=(W-cw)/2,oy=(H-ch)/2;let bw=b.w*cw,bh=b.h*ch;const cx=ox+b.x*cw+bw/2,cy=oy+b.y*ch+bh/2;
  if(bw/bh<W/H)bw=bh*W/H;else bh=bw*H/W;bw=Math.min(bw,W);bh=Math.min(bh,H);
  const x0=Math.min(Math.max(0,cx-bw/2),W-bw),y0=Math.min(Math.max(0,cy-bh/2),H-bh);
  return`scale(${(W/bw).toFixed(4)}) translate(${(-x0/W*100).toFixed(3)}%,${(-y0/H*100).toFixed(3)}%)`}
function edShow(r,ft){const v=$('cmpVid');if(!r)return;const m=r.m,T=r.start+(ft-m.a);
  $('edTime').textContent=`${mmss(T)} / ${mmss(edTotal())}`;
  v.style.transform=edZoomCss(m.zoom);
  const ov=$('edOv');if(m.text&&T-r.start<4.5){ov.textContent=m.text;ov.style.display='block'}else ov.style.display='none';
  edPlayhead(T)}
function edPlayhead(T){ED.T=T;const r=edAt(T),tl=$('edTl');let ph=$('edPh');if(!ph){ph=document.createElement('div');ph.id='edPh';ph.className='ed-ph';tl.appendChild(ph)}
  if(!r){ph.style.display='none';return}const el=tl.querySelector(`.blk[data-mid="${r.m.mid}"]`);if(!el){ph.style.display='none';return}
  ph.style.display='';ph.style.left=(el.offsetLeft+Math.min(1,(T-r.start)/r.len)*el.offsetWidth-1)+'px'}
function edLoad(r,ft,play){const v=$('cmpVid'),src=`/comp/${CMP.id}/${r.m.file}`;ED.cur=r.i;$('edEmpty').style.display='none';
  const go=()=>{v.currentTime=ft;edShow(r,ft);if(play)v.play().catch(()=>{})};
  if(!v.src.endsWith(src)){v.preload='auto';v.src=src;v.addEventListener('loadedmetadata',go,{once:true});v.load()}else go()}
function edSeek(T,play){const r=edAt(T);if(!r)return;edLoad(r,r.m.a+Math.max(0,T-r.start),play)}
function edStop(reset){const v=$('cmpVid');ED.playing=false;v.pause();$('edPlay').innerHTML='&#9654; Play';if(reset){v.removeAttribute('src');v.load();$('edEmpty').style.display='';$('edOv').style.display='none'}}
$('edPlay').onclick=()=>{if(!CMP||!CMP.moments.length)return;if(ED.playing){edStop();return}
  ED.playing=true;$('edPlay').innerHTML='&#10074;&#10074; Pause';if(ED.T>=edTotal()-0.05)ED.T=0;edSeek(ED.T,true)};
$('cmpVid').addEventListener('timeupdate',()=>{if(!CMP||ED.cur<0)return;const mp=edMap(),r=mp[ED.cur];if(!r)return;const v=$('cmpVid');
  if(v.currentTime>=r.m.b-0.03){if(ED.playing&&mp[ED.cur+1]){const n=mp[ED.cur+1];edLoad(n,n.m.a,true)}else{edShow(r,r.m.b);if(ED.playing)edStop()}return}
  edShow(r,v.currentTime)});
// timeline
function drawTimeline(){const tl=$('edTl');const mp=edMap();
  tl.innerHTML=mp.map(r=>{const m=r.m,tr=m.tr||CMP.transition||'cut',tags=[m.zoom&&m.zoom!=='full'?(m.zoom==='cam'?'cam':'game'):'',m.text?'T':'',tr!=='cut'?tr:''].filter(Boolean).join(' ');
    return`<div class="blk${m.mid===ED.sel?' sel':''}" draggable="true" data-mid="${m.mid}" style="flex-grow:${r.len.toFixed(2)};background-image:url('/comp/${esc(CMP.id)}/${esc(m.poster)}')" title="${esc(m.title)} (${mmss(r.len)})">
      <span class="h l" data-h="a"></span><span class="h r" data-h="b"></span>${tags?`<span class="tg">${esc(tags)}</span>`:''}<span class="lb">${r.i+1} &middot; ${mmss(r.len)}</span></div>`}).join('')+
    `<div class="blk add" id="edAddBtn" title="Add a part from the stream">+ Add</div>`;
  tl.querySelectorAll('.blk[data-mid]').forEach(el=>{const mid=el.dataset.mid;
    el.addEventListener('click',e=>{if(e.target.classList.contains('h'))return;ED.sel=mid;const r=edMap().find(x=>x.m.mid===mid);
      const f=Math.min(1,Math.max(0,(e.clientX-el.getBoundingClientRect().left)/el.offsetWidth));const was=ED.playing;
      tl.querySelectorAll('.blk').forEach(b=>b.classList.toggle('sel',b.dataset.mid===mid));drawInsp();edSeek(r.start+f*r.len,was)});
    el.addEventListener('contextmenu',async e=>{e.preventDefault();edStop();await cmpDo('remove',{mid});toast('Part removed. <b>Undo</b> brings it back.')});
    el.addEventListener('dragstart',e=>{if(ED.dragH){e.preventDefault();return}el.classList.add('drag');e.dataTransfer.setData('text/plain',mid)});
    el.addEventListener('dragend',()=>el.classList.remove('drag'));
    el.addEventListener('dragover',e=>{e.preventDefault();el.classList.add('over')});
    el.addEventListener('dragleave',()=>el.classList.remove('over'));
    el.addEventListener('drop',async e=>{e.preventDefault();el.classList.remove('over');const from=e.dataTransfer.getData('text/plain');if(!from||from===mid)return;
      const ids=CMP.moments.map(q=>q.mid),fi=ids.indexOf(from),ti=ids.indexOf(mid);ids.splice(fi,1);ids.splice(ti,0,from);await cmpDo('order',{order:ids})});
    el.querySelectorAll('.h').forEach(h=>h.addEventListener('pointerdown',e=>edTrimStart(e,el,mid,h.dataset.h)))});
  $('edAddBtn').onclick=edAddOpen;edPlayhead(ED.T)}
function edTrimStart(e,el,mid,side){e.preventDefault();e.stopPropagation();const m=CMP.moments.find(x=>x.mid===mid);if(!m)return;
  edStop();ED.dragH=true;el.draggable=false;const x0=e.clientX,a0=m.a,b0=m.b,spp=edLen(m)/el.offsetWidth;let na=a0,nb=b0;
  const lb=el.querySelector('.lb'),idx=CMP.moments.indexOf(m)+1;
  const mv=ev=>{const d=(ev.clientX-x0)*spp;if(side==='a')na=Math.min(Math.max(0,a0+d),b0-1);else nb=Math.max(Math.min(m.dur,b0+d),a0+1);
    lb.textContent=`${idx} · ${mmss(nb-na)}`;el.style.flexGrow=(nb-na).toFixed(2);$('edTime').textContent=`${side==='a'?'Start':'End'} ${(side==='a'?na-(m.a0??a0):nb-(m.b0??b0))>=0?'+':''}${(side==='a'?na-(m.a0??a0):nb-(m.b0??b0)).toFixed(1)} s`};
  const up=async()=>{window.removeEventListener('pointermove',mv);window.removeEventListener('pointerup',up);ED.dragH=false;el.draggable=true;
    if(Math.abs(na-a0)<0.05&&Math.abs(nb-b0)<0.05){drawTimeline();return}
    if((side==='a'&&a0+0.01>=0&&na<=0.001)||(side==='b'&&nb>=m.dur-0.001))toast("That's as far as this part goes (each part keeps 5 seconds extra on each side).");
    await cmpDo('trim',{mid,a:+na.toFixed(2),b:+nb.toFixed(2)});const r=edMap().find(x=>x.m.mid===mid);if(r)edSeek(side==='a'?r.start:Math.max(r.start,r.start+r.len-3),false)};
  window.addEventListener('pointermove',mv);window.addEventListener('pointerup',up)}
// inspector (the selected part)
const sgn=v=>(v>=0?'+':'−')+Math.abs(v).toFixed(v%1?1:0)+' s';
function drawInsp(){const box=$('edInsp'),m=edSelM();
  if(!m){box.innerHTML='<div class="mute">Pick a part on the timeline.</div>';return}
  const k=CMP.moments.indexOf(m)+1,tr=m.tr||'',zoom=m.zoom||'full',st=m.stream_t!=null?` &middot; ${mmss(m.stream_t)} in the stream`:'';
  box.innerHTML=`<b>Part ${k}</b><span class="tiny mute">${st} &middot; ${mmss(edLen(m))}</span>
    <div class="k">Title (used for chapters)</div><input type="text" id="inTitle" value="${esc(m.title||'')}">
    <div class="k">Trim: start ${sgn(m.a-(m.a0??m.a))} / end ${sgn(m.b-(m.b0??m.b))}</div>
    <div class="row"><span class="tiny mute">Start</span><button class="btn sm" data-t="a,-1">-1s</button><button class="btn sm" data-t="a,1">+1s</button>
      <span class="tiny mute" style="margin-left:8px">End</span><button class="btn sm" data-t="b,-1">-1s</button><button class="btn sm" data-t="b,1">+1s</button></div>
    <div class="k">Into the next part</div><span class="seg" id="inTr"><button data-v="">Default (${esc(CMP.transition||'cut')})</button><button data-v="cut">Cut</button><button data-v="flash">Flash</button><button data-v="fade">Fade</button></span>
    <div class="k">Text on screen (first few seconds)</div><input type="text" id="inText" maxlength="120" placeholder="He really tried it" value="${esc(m.text||'')}">
    <div class="k">Zoom</div><span class="seg" id="inZoom"><button data-v="full">Full</button><button data-v="cam">Peanut cam</button><button data-v="game">Gameplay</button></span>`;
  box.querySelectorAll('#inTr button').forEach(b=>b.classList.toggle('on',b.dataset.v===tr));
  box.querySelectorAll('#inZoom button').forEach(b=>b.classList.toggle('on',b.dataset.v===zoom));
  box.querySelectorAll('#inTr button').forEach(b=>b.onclick=()=>cmpDo('moment',{mid:m.mid,tr:b.dataset.v}));
  box.querySelectorAll('#inZoom button').forEach(b=>b.onclick=async()=>{await cmpDo('moment',{mid:m.mid,zoom:b.dataset.v});edSeek(edMap().find(x=>x.m.mid===m.mid).start,false)});
  $('inTitle').onchange=()=>cmpDo('moment',{mid:m.mid,title:$('inTitle').value});
  $('inText').onchange=async()=>{await cmpDo('moment',{mid:m.mid,text:$('inText').value});edSeek(edMap().find(x=>x.m.mid===m.mid).start,false)};
  box.querySelectorAll('[data-t]').forEach(b=>b.onclick=async()=>{const[s,d]=b.dataset.t.split(','),mm=edSelM();const a=s==='a'?mm.a+(+d):mm.a,bb=s==='b'?mm.b+(+d):mm.b;
    if(a<0||bb>mm.dur){toast("That's as far as this part goes (each part keeps 5 seconds extra on each side).");return}if(bb-a<1)return;
    await cmpDo('trim',{mid:mm.mid,a,b:bb});const r=edMap().find(x=>x.m.mid===mm.mid);edSeek(s==='a'?r.start:Math.max(r.start,r.start+r.len-3),false)})}
function drawComp(){const has=!!CMP;['cmpRen','cmpDel','cmpExport','cmpPrem','cmpShuffle','cmpOldest','edPlay','edSplit','edDel','edChap'].forEach(id=>$(id).disabled=!has);
  $('cmpGoal').disabled=!has;
  if(!has){$('cmpLen').textContent='0:00';$('cmpBar').firstElementChild.style.width='0';$('cmpLeft').textContent='';$('edUndo').disabled=true;
    $('edTl').innerHTML='<div class="empty" style="flex:1">Make a long video on the Make Shorts tab (Make: Long video), or start one with <b>New compilation</b> and use <b>+ Add to compilation</b> on keyword-search results.</div>';
    $('edInsp').innerHTML='';return}
  const len=edTotal(),goal=CMP.goal||480;
  $('cmpGoal').value=Math.round(goal/60);$('cmpLen').textContent=mmss(len);
  $('cmpBar').className='cmp-bar'+(len>=goal?' done':'');$('cmpBar').firstElementChild.style.width=Math.min(100,len/goal*100)+'%';
  $('cmpLeft').textContent=len>=goal?`Goal of ${mmss(goal)} reached · ${CMP.moments.length} parts`:`goal ${mmss(goal)} - add about ${mmss(goal-len)} more · ${CMP.moments.length} parts`;
  $('edUndo').disabled=!CMP.undo;$('edUndo').textContent=CMP.undo?`Undo (${CMP.undo})`:'Undo';
  document.querySelectorAll('#cmpTr button').forEach(b=>b.classList.toggle('on',b.dataset.v===(CMP.transition||'cut')));
  document.querySelectorAll('#cmpNum button').forEach(b=>b.classList.toggle('on',b.dataset.v===(CMP.numbers?'1':'0')));
  $('edTime').textContent=`${mmss(ED.T)} / ${mmss(len)}`;
  drawTimeline();drawInsp();edMediaDraw()}
$('edSplit').onclick=async()=>{if(!CMP)return;const r=edAt(ED.T);if(!r)return;const ft=r.m.a+(ED.T-r.start);
  if(ft<r.m.a+0.5||ft>r.m.b-0.5){toast('Move the playhead inside a part first (not right at its edge).');return}
  edStop();await cmpDo('split',{mid:r.m.mid,t:+ft.toFixed(2)});ED.sel=CMP.moments[r.i+1].mid;drawComp()};
$('edDel').onclick=async()=>{const m=edSelM();if(!m)return;edStop();await cmpDo('remove',{mid:m.mid});toast('Part removed. <b>Undo</b> brings it back.')};
$('edUndo').onclick=async()=>{edStop();await cmpDo('undo')};
document.addEventListener('keydown',e=>{if(!$('comps').classList.contains('on')||/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName))return;
  if(e.key==='s'||e.key==='S'){e.preventDefault();$('edSplit').click()}
  else if(e.key===' '){e.preventDefault();$('edPlay').click()}
  else if((e.ctrlKey||e.metaKey)&&e.key==='z'){e.preventDefault();$('edUndo').click()}
  else if(e.key==='Delete'){e.preventDefault();$('edDel').click()}});
// + Add a part from the stream
function edAddOpen(){if(!CMP)return;if(!CMP.source_file){toast('+ Add works on long videos made on the Make Shorts tab. For this one, use <b>+ Add to compilation</b> on keyword-search results.');return}
  if(!CMP.source_ok){toast("The stream this was made from was already cleaned up, so new parts can't be added. Make the long video again to get it back.");return}
  edStop();ED.addA=ED.addB=null;$('edAdd').style.display='';const v=$('edSrc'),src=`/comp_source/${CMP.id}`;
  if(!v.src.endsWith(src)){v.preload='metadata';v.src=src}
  const sel=edSelM();$('edAddWhere').textContent=sel?` - goes after part ${CMP.moments.indexOf(sel)+1}`:' - goes at the end';
  if(sel&&sel.stream_t!=null)v.addEventListener('loadedmetadata',()=>{v.currentTime=Math.max(0,sel.stream_t-(CMP.source_offset||0)+edLen(sel))},{once:true});
  edMarks();$('edAdd').scrollIntoView({behavior:'smooth',block:'nearest'})}
function edMarks(){const off=CMP.source_offset||0,f=t=>t==null?'-':mmss(off+t);
  $('edMarks').textContent=`Start ${f(ED.addA)} · End ${f(ED.addB)}`+(ED.addA!=null&&ED.addB!=null?` (${mmss(ED.addB-ED.addA)})`:'')}
$('edAddX').onclick=()=>{$('edSrc').pause();$('edAdd').style.display='none'};
$('edMarkA').onclick=()=>{ED.addA=$('edSrc').currentTime;if(ED.addB!=null&&ED.addB<=ED.addA)ED.addB=null;edMarks()};
$('edMarkB').onclick=()=>{ED.addB=$('edSrc').currentTime;if(ED.addA!=null&&ED.addB<=ED.addA)ED.addA=null;edMarks()};
$('edAddGo').onclick=async()=>{if(ED.addA==null||ED.addB==null||ED.addB-ED.addA<1){toast('Mark a start and an end first (at least 1 second apart).');return}
  const sel=edSelM();const r=await api('/api/run',{kind:'compaddrange',comp:CMP.id,start:+ED.addA.toFixed(2),end:+ED.addB.toFixed(2),after:sel?sel.mid:''});
  $('edSrc').pause();$('edAdd').style.display='none';lastJobKey='running';
  toast(r.queued?'<b>In line:</b> the part is added when the current job finishes.':'<b>Adding the part...</b>');poll()};
// intro / outro / music + chapters
async function edMediaLoad(){try{ED.media=(await api('/api/editor_media')).items}catch(e){ED.media=[]}edMediaDraw()}
function edMediaDraw(){if(!CMP)return;const vids=ED.media.filter(x=>x.kind==='video'),mus=ED.media.filter(x=>x.kind==='music');
  const opt=(list,cur)=>'<option value="">None</option>'+list.map(x=>`<option value="${esc(x.name)}"${x.name===cur?' selected':''}>${esc(x.name)} (${mmss(x.dur)})</option>`).join('');
  $('edIntro').innerHTML=opt(vids,CMP.intro);$('edOutro').innerHTML=opt(vids,CMP.outro);$('edMusic').innerHTML=opt(mus,CMP.music);
  const vol=CMP.music_volume??15;$('edVol').value=vol;$('edVolV').textContent=vol+'%';$('edVolBox').style.display=CMP.music?'':'none'}
$('edIntro').onchange=()=>cmpDo('media',{intro:$('edIntro').value});
$('edOutro').onchange=()=>cmpDo('media',{outro:$('edOutro').value});
$('edMusic').onchange=()=>cmpDo('media',{music:$('edMusic').value});
$('edVol').oninput=()=>$('edVolV').textContent=$('edVol').value+'%';
$('edVol').onchange=()=>cmpDo('media',{music_volume:+$('edVol').value});
$('edMediaUp').onclick=()=>$('edMediaFile').click();
$('edMediaFile').onchange=async e=>{const f=e.target.files[0];e.target.value='';if(!f)return;toast(`Uploading <b>${esc(f.name)}</b>...`);
  const r=await fetch('/api/editor_media_upload?name='+encodeURIComponent(f.name),{method:'POST',body:f});let j={};try{j=await r.json()}catch(x){}
  if(!r.ok){toast(esc(j.error||'The upload didn\'t work.'));return}await edMediaLoad();toast(`<b>${esc(j.name)}</b> is ready - pick it as the intro, outro or music.`)};
$('edChap').onclick=async()=>{if(!CMP)return;const box=$('edChapBox');if(box.style.display!=='none'){box.style.display='none';return}
  const r=await api('/api/comp_chapters?id='+encodeURIComponent(CMP.id));
  $('edChapTxt').value=r.text||'YouTube needs at least 3 chapters, each 10 seconds or longer. Add more parts (or longer ones) first.';box.style.display=''};
$('edChapCopy').onclick=()=>{navigator.clipboard.writeText($('edChapTxt').value).then(()=>toast('Chapters copied.'),()=>{$('edChapTxt').select();document.execCommand('copy');toast('Chapters copied.')})};
$('cmpPick').onchange=()=>{setCur($('cmpPick').value);edStop(true);$('edAdd').style.display='none';loadComps()};
$('cmpNew').onclick=newComp;
$('cmpRen').onclick=()=>{const n=prompt('New name:',CMP.name);if(n)cmpDo('settings',{name:n})};
$('cmpDel').onclick=()=>{if(confirm(`Delete "${CMP.name}" and its ${CMP.moments.length} parts? (Videos you already exported stay.)`))cmpDo('delete')};
$('cmpGoal').onchange=()=>{const m=+$('cmpGoal').value;if(m>0)cmpDo('settings',{goal:m*60})};
$('cmpShuffle').onclick=()=>cmpDo('shuffle');$('cmpOldest').onclick=()=>cmpDo('oldest');
document.querySelectorAll('#cmpTr button').forEach(b=>b.onclick=()=>cmpDo('settings',{transition:b.dataset.v}));
document.querySelectorAll('#cmpNum button').forEach(b=>b.onclick=()=>cmpDo('settings',{numbers:b.dataset.v==='1'}));
async function cmpExport(premiere){if(!CMP||!CMP.moments.length){toast('Add some parts first.');return}
  const r=await api('/api/run',{kind:'compexport',comp:CMP.id,premiere});lastJobKey='running';
  toast(r.queued?'<b>In line:</b> the export starts when the current job finishes.':'<b>Exporting...</b> progress shows on the Make Shorts tab.');poll()}
$('cmpExport').onclick=()=>cmpExport(false);$('cmpPrem').onclick=()=>cmpExport(true);
edMediaLoad();
// keyword search side: Crash words, "+ Add to compilation", "Added (4th)"
$('kwCrash').onclick=()=>{const w=crashWords||'crash, crashed, wreck, my car, flip, flipped, oh no';const cur=$('kwWords').value.trim();
  $('kwWords').value=cur&&!cur.includes(w)?cur+', '+w:w;$('kwChat').checked=true;$('kwSimilar').checked=true;
  toast('<b>Crash words added.</b> Chat spikes ("KEKW", "LUL"...) help find the funny ones, so "Also search chat" is on.')};
$('kwComp').onchange=async()=>{if($('kwComp').value==='__new'){const id=await newComp();if(!id)$('kwComp').value=cmpCur||'';return}
  setCur($('kwComp').value);await loadComps()};
let addingNow={};
function markAdded(){if(!KW)return;const used={};(CMP&&CMP.moments||[]).forEach((m,k)=>{if(m.sid===KW.sid)used[m.i]=k+1});
  const len=CMP?CMP.moments.reduce((a,m)=>a+m.b-m.a,0):0;$('kwCompLen').textContent=CMP?`now ${mmss(len)} of ${mmss(CMP.goal||480)}`:'';
  document.querySelectorAll('[data-a=comp]').forEach(b=>{const i=+b.dataset.i;
    if(used[i]){b.textContent=`Added (${nth(used[i])})`;b.classList.add('added');b.disabled=true}
    else if(addingNow[KW.sid+':'+i]){b.textContent='Adding...';b.classList.remove('added');b.disabled=true}
    else{b.textContent='+ Add to compilation';b.classList.remove('added');b.disabled=false}})}
async function addToComp(m){if(!KW.source_available){toast('The stream for this search was deleted. Run the search again to re-download it.');return}
  if(!cmpCur||!CMPS.some(c=>c.id===cmpCur)){const id=await newComp();if(!id)return}
  addingNow[KW.sid+':'+m.i]=true;markAdded();
  try{const r=await api('/api/run',{kind:'compadd',comp:cmpCur,sid:KW.sid,idx:m.i});lastJobKey='running';if(r.queued)toast('<b>In line:</b> added when the current job finishes.');poll()}
  catch(e){delete addingNow[KW.sid+':'+m.i];markAdded()}}

// ---------- review ----------
async function loadClips(){
  const data=await api('/api/clips');const grid=$('grid');grid.innerHTML='';
  if(!data.length){grid.innerHTML='<div class="empty" style="grid-column:1/-1">Nothing waiting for review.</div>';return}
  for(const c of data){
    const el=document.createElement('div');el.className='clip';
    el.innerHTML=`<video controls preload="none" poster="/media/${c.job}/${c.poster}" src="/media/${c.job}/${c.file}"></video>
      <div class="b"><input type="text" value="${esc(c.title)}">
      <div class="chips"><span class="chip s">score ${c.score}</span><span class="chip">${c.length}s</span>${c.reasons.map(r=>`<span class="chip">${esc(r)}</span>`).join('')}</div>
      ${streamLine(c)}
      <div class="act"><button class="btn ed">&#9986; Edit</button><button class="btn ok">Approve</button><button class="btn no">Reject</button>${colButton(c)}<button class="btn tcbtn" style="flex-basis:100%">Title card</button></div></div>`;
    const send=async st=>{await api('/api/decide',{job:c.job,id:c.id,status:st,title:el.querySelector('input').value});el.remove();poll();
      if(!grid.querySelector('.clip'))grid.innerHTML='<div class="empty" style="grid-column:1/-1">All done. Head to Upload to schedule the approved ones.</div>'};
    el.querySelector('.ok').onclick=()=>send('approved');el.querySelector('.no').onclick=()=>send('rejected');
    el.querySelector('.ed').onclick=()=>openEditor(c);
    grid.appendChild(el);
  }
  markCols();
  grid.querySelectorAll('.clip').forEach((el,k)=>{const b=el.querySelector('.tcbtn');if(b)b.onclick=()=>openTitles(data[k])});
}

// ---------- upload ----------
async function loadPlan(){
  if(!S)await poll();
  $('ytSetup').style.display=S.youtube.secret?'none':'block';
  $('ytState').textContent=S.youtube.token?'YouTube connected':(S.youtube.secret?'Google will ask you to sign in on first upload':'');
  const plan=await api('/api/plan');const box=$('plan');
  box.innerHTML=plan.length?plan.map(p=>`<div class="it"><img src="${p.poster}"><div><b>${esc(p.title)}</b><div class="tiny mute">${p.length}s &middot; YouTube slot: ${esc(p.when)}</div>${streamLine(p)}</div>
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
const keys=['saved_keywords','saved_keywords_max','search_lead_sec','search_tail_sec','keep_source_days','delete_exported','delete_exported_days','delete_searches','search_keep_days','edit_window_min','export_folder','screenshot_folder','export_handles_sec','export_vertical_too','output_fps','auto_enabled','auto_time','channel_url','auto_twitch_clips','shorts_per_stream','captions','delete_source','delete_rejected','delete_uploaded','use_gpu','twitch_client_id','twitch_client_secret','schedule_times'];
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
  const il=$('inbLayout');if(il){const v=(INB&&INB.layout)||il.value;il.innerHTML='<option value="">Default layout</option>'+src.layouts.map(l=>`<option value="${l.id}">${esc(l.name)}</option>`).join('');
    il.value=src.layouts.some(l=>l.id===v)?v:''}
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
  if(SAFE)safeZones($('prev'));
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
  frInit(info.framing||null);E.mk=(info.markers||[]).map(t=>t-off).filter(t=>t>=0&&t<=E.dur);secInit(info.sections);
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
  tl.querySelectorAll('.mk').forEach(x=>x.remove());
  for(const t of (E.mk||[])){if(t<E.vs||t>E.ve)continue;const m=document.createElement('div');m.className='mk'+(Math.abs(t-E.a)<.01||Math.abs(t-E.b)<.01?' hit':'');
    m.style.left=X(t)+'%';m.title='Marker '+fmt(t+E.off);
    m.onmousedown=e=>{e.stopPropagation();e.preventDefault()};
    m.onclick=e=>{e.stopPropagation();$('edSrc').currentTime=t;drawTL()};
    m.oncontextmenu=e=>{e.preventDefault();e.stopPropagation();E.mk=E.mk.filter(x=>x!==t);mkSave();drawTL()};
    tl.appendChild(m)}
  const ph=$('edSrc').currentTime||E.a;$('tlPh').style.left=X(ph)+'%';
  $('vIn').textContent=fmt(E.a+E.off);$('vOut').textContent=fmt(E.b+E.off);
  secDraw();
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
// drag the whole selection: both ends move together and the length stays the same
let grab=0;
$('tlSel').onmousedown=e=>{if(!E)return;tlDrag='move';grab=tAt(e)-E.a;$('tl').classList.add('moving');e.stopPropagation();e.preventDefault()};
$('tl').onmousedown=e=>{if(!E)return;$('edSrc').currentTime=tAt(e);drawTL()};
window.addEventListener('mousemove',e=>{if(!tlDrag||!E)return;const t=tAt(e);
  if(tlDrag==='move'){const len=E.b-E.a;let a=t-grab;
    // snap whichever end is nearer a marker
    const sa=snap(a),sb=snap(a+len);if(sa!==a&&(sb===a+len||Math.abs(sa-a)<=Math.abs(sb-a-len)))a=sa;else if(sb!==a+len)a=sb-len;
    E.a=+Math.max(0,Math.min(E.dur-len,a)).toFixed(2);E.b=+(E.a+len).toFixed(2);$('edSrc').currentTime=E.a;drawTL();return}
  if(tlDrag==='in')E.a=snap(t);else E.b=snap(t);
  E.a=Math.max(0,Math.min(E.a,E.b-3));E.b=Math.min(E.dur,Math.max(E.b,E.a+3));$('edSrc').currentTime=tlDrag==='in'?E.a:E.b;drawTL()});
window.addEventListener('mouseup',()=>{if(tlDrag){tlDrag=null;$('tl').classList.remove('moving');if(E&&(E.a<E.vs+1||E.b>E.ve-1)){setView();drawTL()}}});
// ---------- markers (trim editor) ----------
// snap = within 10 screen pixels of a marker
function snap(t){if(!E||!E.mk||!E.mk.length||!$('mkSnap').checked)return t;
  const r=$('tl').getBoundingClientRect(),tol=10/r.width*(E.ve-E.vs);let best=t,d=tol;
  for(const m of E.mk){const k=Math.abs(m-t);if(k<=d){d=k;best=m}}return best}
let mkTimer=null;
function mkSave(){clearTimeout(mkTimer);const job=E.job,id=E.id,list=E.mk.map(t=>t+E.off);
  mkTimer=setTimeout(()=>api('/api/markers',{job,id,markers:list}).catch(()=>{}),400)}
function mkAdd(){if(!E)return;const t=+($('edSrc').currentTime||0).toFixed(2);
  if(E.mk.some(m=>Math.abs(m-t)<.2)){toast('There\'s already a marker there.');return}
  E.mk.push(t);E.mk.sort((a,b)=>a-b);mkSave();drawTL()}
function mkJump(dir){if(!E||!E.mk.length)return;const ph=$('edSrc').currentTime;
  const t=dir>0?E.mk.find(m=>m>ph+.05):[...E.mk].reverse().find(m=>m<ph-.05);if(t===undefined)return;
  if(t<E.vs||t>E.ve){E.pad=Math.min(1800,Math.max(E.pad,Math.abs(t-(t<E.vs?E.a:E.b))+10));setView()}
  $('edSrc').currentTime=t;drawTL()}
$('mkAdd').onclick=mkAdd;$('mkPrev').onclick=()=>mkJump(-1);$('mkNext').onclick=()=>mkJump(1);
$('mkClear').onclick=()=>{if(!E||!E.mk.length)return;if(!confirm('Remove all markers on this Short?'))return;E.mk=[];mkSave();drawTL()};
$('mkSnap').onchange=()=>drawTL();
window.addEventListener('keydown',e=>{if(!E||!$('ed').classList.contains('on'))return;
  if(/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)&&document.activeElement.type!=='checkbox'&&document.activeElement.type!=='radio'&&document.activeElement.type!=='range')return;
  if((e.ctrlKey||e.metaKey)&&e.shiftKey&&(e.key==='e'||e.key==='E')){e.preventDefault();shot(true);return}
  if((e.ctrlKey||e.metaKey)&&(e.key==='k'||e.key==='K')){e.preventDefault();secCut();return}
  if(e.ctrlKey||e.metaKey||e.altKey)return;
  if(e.key==='m'||e.key==='M'){e.preventDefault();mkAdd()}
  if(e.key==='c'||e.key==='C'){e.preventDefault();secCut()}});
let stopAt=null;
$('edSrc').addEventListener('timeupdate',()=>{if(!E)return;if(stopAt!==null&&$('edSrc').currentTime>=stopAt){$('edSrc').pause();stopAt=null}drawTL()});
$('edPlaySel').onclick=()=>{$('edSrc').currentTime=E.a;stopAt=E.b;$('edSrc').play()};
$('edPlayPre').onclick=()=>{$('edSrc').currentTime=Math.max(0,E.a-15);stopAt=E.a+2;$('edSrc').play()};
$('edWider').onclick=()=>{E.pad=Math.min(E.pad*2.5,1800);setView();drawTL()};
$('edReset').onclick=()=>{E.a=E.oa;E.b=E.ob;E.pad=60;setView();drawTL();$('edSrc').currentTime=E.a};
$('edSave').onclick=async()=>{if(!E||edSaving)return;
  if(E.b-E.a>180&&!confirm('This is over 3 minutes, which is longer than YouTube allows for a Short. Make it anyway?'))return;
  edSaving=true;$('edSave').disabled=true;$('edSave').textContent='Updating...';$('edSrc').pause();
  // let go of the current Short's file so Windows can replace it
  {const v=$('edShort');E.shortSrc=v.getAttribute('src');v.pause();v.removeAttribute('src');v.load()}
  try{const r=await api('/api/run',{kind:'rerender',job:E.job,id:E.id,start:E.a+E.off,end:E.b+E.off,layout:$('edLayout').value,framing:frSend(),sections:secSend()});
    if(r.queued){edSaving=false;$('edSave').disabled=false;$('edSave').textContent='Update Short';closeEditor();toast('<b>In line:</b> this Short updates when the current job finishes.');poll();return}
    lastJobKey='running';poll()}catch(e){edSaving=false;$('edSave').disabled=false;$('edSave').textContent='Update Short'}};

// ---------- sections (trim editor): razor cuts, and each part's look + banner spot ----------
// E.cuts = cut points (video times). E.parts = the settings of parts as last chosen: [{start,end,look,banner,box}]
let secSel=-1,secTimer=null,secDrag=null,liveRAF=null;
const LOOKNAME={normal:'Normal',closeup:'Close-up',gameplay:'Gameplay only'},BANNAME={layout:'banner: layout',bottom:'banner: bottom',top:'banner: top',off:'no banner'};
function secInit(list){const off=E.off;E.parts=(list||[]).map(x=>Object.assign({},x,{start:x.start-off,end:x.end-off}));
  const cs=new Set();for(const x of E.parts){cs.add(+x.start.toFixed(2));cs.add(+x.end.toFixed(2))}
  E.cuts=[...cs].sort((a,b)=>a-b);secSel=-1}
// the parts of the Short right now: from Start to End, split at every cut inside it
function pieces(){if(!E)return[];const pts=[E.a,...E.cuts.filter(t=>t>E.a+.05&&t<E.b-.05),E.b];const out=[];
  for(let i=0;i<pts.length-1;i++){const a=pts[i],b=pts[i+1],m=(a+b)/2;
    const st=(E.parts||[]).find(x=>x.start<=m&&x.end>m)||{};
    out.push({start:a,end:b,look:st.look||'normal',banner:st.banner||'layout',box:st.box||null})}
  return out}
function secSet(list){E.parts=list.map(x=>Object.assign({},x));secSave();secDraw();liveDraw()}
function secSend(){return pieces().map(x=>Object.assign({},x,{start:+(x.start+E.off).toFixed(2),end:+(x.end+E.off).toFixed(2)}))}
function secSave(){clearTimeout(secTimer);const job=E.job,id=E.id,list=secSend();
  secTimer=setTimeout(()=>api('/api/sections',{job,id,sections:list}).catch(()=>{}),400)}
function pieceAt(t){const ps=pieces();let i=ps.findIndex(p=>t>=p.start&&t<p.end);if(i<0)i=t>=E.b?ps.length-1:0;return i}
function secDraw(){if(!E)return;const tl=$('secTl');tl.innerHTML='';const ps=pieces();
  if(secSel>=ps.length)secSel=ps.length-1;
  ps.forEach((p,i)=>{const d=document.createElement('div');d.className='pc '+p.look+(p.banner==='off'?' nob':'')+(i===secSel?' on':'');
    d.style.left=X(p.start)+'%';d.style.width=Math.max(.3,X(p.end)-X(p.start))+'%';
    d.textContent=LOOKNAME[p.look]+' · '+BANNAME[p.banner];d.title=fmt(p.start+E.off)+' - '+fmt(p.end+E.off)+'  '+d.textContent;
    d.onclick=e=>{e.stopPropagation();secSel=i;const v=$('edSrc');if(v.currentTime<p.start||v.currentTime>=p.end)v.currentTime=p.start+.01;secDraw();liveDraw()};
    tl.appendChild(d)});
  for(const t of E.cuts){if(t<=E.a+.05||t>=E.b-.05||t<E.vs||t>E.ve)continue;const c=document.createElement('div');c.className='cut';c.style.left=X(t)+'%';
    c.title='Cut at '+fmt(t+E.off)+' - right-click to remove';
    c.onclick=e=>{e.stopPropagation();$('edSrc').currentTime=t;drawTL()};
    c.oncontextmenu=e=>{e.preventDefault();e.stopPropagation();secRemoveCut(t)};tl.appendChild(c)}
  const ph=document.createElement('div');ph.className='sph';ph.style.left=X($('edSrc').currentTime||E.a)+'%';tl.appendChild(ph);
  const p=ps[secSel];
  $('secWhich').textContent=p?`${secSel+1} of ${ps.length} (${fmt(p.start+E.off)} - ${fmt(p.end+E.off)}, ${(p.end-p.start).toFixed(1)}s)`:'click a part on the bar';
  document.querySelectorAll('#secLook button').forEach(b=>{b.classList.toggle('on',!!p&&b.dataset.v===p.look);b.disabled=!p});
  document.querySelectorAll('#secBan button').forEach(b=>{b.classList.toggle('on',!!p&&b.dataset.v===p.banner);b.disabled=!p});
  $('secJoin').disabled=!p||secSel===0;
  const showBox=!!p&&p.look!=='normal';$('secBoxWrap').style.display=showBox?'':'none';
  if(showBox){$('secBoxT').textContent=p.look==='closeup'?'Close-up area (what fills the screen)':'Gameplay area (what fills the screen)';secBoxDraw()}}
function secCut(){if(!E)return;const t=+($('edSrc').currentTime||0).toFixed(2);
  if(t<=E.a+.3||t>=E.b-.3){toast('Move the playhead inside the Short first (between Start and End).');return}
  if(E.cuts.some(c=>Math.abs(c-t)<.2)){toast('There\'s already a cut there.');return}
  const ps=pieces();E.cuts.push(t);E.cuts.sort((a,b)=>a-b);
  // both halves keep the look the part had
  secSet(ps);secSel=pieceAt(t+.01);secDraw()}
function secRemoveCut(t){const ps=pieces();const i=ps.findIndex(p=>Math.abs(p.start-t)<.01);E.cuts=E.cuts.filter(c=>Math.abs(c-t)>=.01);
  if(i>0){ps[i-1].end=ps[i].end;ps.splice(i,1)}secSel=Math.max(0,i-1);secSet(ps)}
$('secCut').onclick=secCut;
$('secJoin').onclick=()=>{const p=pieces()[secSel];if(p&&secSel>0)secRemoveCut(p.start)};
$('secClear').onclick=()=>{if(!E||!E.cuts.length&&!(E.parts||[]).length)return;if(!confirm('Remove all cuts and go back to one normal part?'))return;E.cuts=[];secSel=-1;secSet([])};
function secChange(k,v){const ps=pieces(),p=ps[secSel];if(!p)return;p[k]=v;
  if(k==='look'){if(v==='normal')p.box=null;else if(p.banner==='layout')p.banner='bottom';
    if(v!=='normal'){const same=ps.find(q=>q!==p&&q.look===v&&q.box);p.box=same?clone(same.box):null}}
  secSet(ps)}
document.querySelectorAll('#secLook button').forEach(b=>b.onclick=()=>secChange('look',b.dataset.v));
document.querySelectorAll('#secBan button').forEach(b=>b.onclick=()=>secChange('banner',b.dataset.v));
// the area of the stream a close-up / gameplay-only part shows
const defBox=look=>clone((F&&F[look==='closeup'?'avatar':'gameplay'])||{x:0,y:0,w:1,h:1});
const pBox=p=>p.box||defBox(p.look);
function secBoxDraw(){const p=pieces()[secSel];if(!p||p.look==='normal')return;const v=$('edSrc'),c=$('secCan'),x=c.getContext('2d');
  if(v.videoWidth){c.width=960;c.height=Math.round(960*v.videoHeight/v.videoWidth);x.drawImage(v,0,0,c.width,c.height)}
  const b=pBox(p),e=$('secBox');e.className='box '+(p.look==='closeup'?'av':'gp');
  e.style.left=b.x*100+'%';e.style.top=b.y*100+'%';e.style.width=b.w*100+'%';e.style.height=b.h*100+'%';$('secZoom').value=Math.round(b.w*100)}
function secBoxSet(b,save){const ps=pieces(),p=ps[secSel];if(!p)return;p.box=b;E.parts=ps;if(save)secSave();secBoxDraw();liveDraw()}
const secPos=e=>{const r=$('secStage').getBoundingClientRect();return[Math.min(1,Math.max(0,(e.clientX-r.left)/r.width)),Math.min(1,Math.max(0,(e.clientY-r.top)/r.height))]};
$('secStage').onmousedown=e=>{const p=pieces()[secSel];if(!p||p.look==='normal')return;e.preventDefault();const q=secPos(e),b=pBox(p);
  secDrag=(q[0]>=b.x&&q[0]<=b.x+b.w&&q[1]>=b.y&&q[1]<=b.y+b.h)?{move:true,dx:q[0]-b.x,dy:q[1]-b.y,b:clone(b)}:{move:false,s:q}};
window.addEventListener('mousemove',e=>{if(!secDrag)return;const q=secPos(e);let b;
  if(secDrag.move){const o=secDrag.b;b={w:o.w,h:o.h,x:Math.min(1-o.w,Math.max(0,q[0]-secDrag.dx)),y:Math.min(1-o.h,Math.max(0,q[1]-secDrag.dy))}}
  else b={x:Math.min(secDrag.s[0],q[0]),y:Math.min(secDrag.s[1],q[1]),w:Math.max(.03,Math.abs(q[0]-secDrag.s[0])),h:Math.max(.03,Math.abs(q[1]-secDrag.s[1]))};
  secBoxSet(b,false)});
window.addEventListener('mouseup',()=>{if(secDrag){secDrag=null;secSave()}});
$('secZoom').oninput=()=>{const p=pieces()[secSel];if(!p)return;const b=pBox(p),cx=b.x+b.w/2,cy=b.y+b.h/2,ar=b.h/b.w;
  let w=Math.min(1,+$('secZoom').value/100),h=Math.min(1,w*ar);w=h/ar;
  secBoxSet({w,h,x:Math.min(1-w,Math.max(0,cx-w/2)),y:Math.min(1-h,Math.max(0,cy-h/2))},true)};
$('secBoxReset').onclick=()=>{const p=pieces()[secSel];if(p)secBoxSet(null,true)};
$('secBoxAll').onclick=()=>{const ps=pieces(),p=ps[secSel];if(!p)return;const b=clone(pBox(p));ps.forEach(q=>{if(q.look===p.look)q.box=clone(b)});secSet(ps);toast('<b>Done:</b> every '+LOOKNAME[p.look].toLowerCase()+' part uses this area.')};

// ---------- live preview: the Short as it will look at the playhead ----------
function liveDraw(){liveDraw0();if(SAFE&&E&&F)safeZones($('live'))}
function liveDraw0(){if(!E||!F)return;const v=$('edSrc'),c=$('live'),y=c.getContext('2d'),PW=c.width,PH=c.height,W=v.videoWidth,H=v.videoHeight;
  y.fillStyle='#000';y.fillRect(0,0,PW,PH);if(!W)return;
  const t=v.currentTime,inside=t>=E.a&&t<=E.b,p=pieces()[pieceAt(t)]||{look:'normal',banner:'layout'};
  $('liveWhat').textContent=inside?'· '+LOOKNAME[p.look]+', '+BANNAME[p.banner]:'· (playhead is outside the Short)';
  const cover=(b,dy,dh)=>{let sx=b.x*W,sy=b.y*H,sw=b.w*W,sh=b.h*H;const r=PW/dh;
    if(sw/sh>r){const nw=sh*r;sx+=(sw-nw)/2;sw=nw}else{const nh=sw/r;sy+=(sh-nh)/2;sh=nh}y.drawImage(v,sx,sy,sw,sh,0,dy,PW,dh)};
  let seam;
  if(p.look!=='normal'){cover(pBox(p),0,PH);seam=PH/2}
  else{const top=F.top_height/1920*PH;
    if(F.mode==='stack'){cover(F.avatar,0,top);cover(F.gameplay,top,PH-top);seam=top}
    else if(F.mode==='single'){cover(F.gameplay,0,PH);seam=PH/2}
    else{y.filter='blur(10px) brightness(0.8)';cover({x:0,y:0,w:1,h:1},0,PH);y.filter='none';const h=PW*H/W;y.drawImage(v,0,(PH-h)/2,PW,h);seam=(PH-h)/2}}
  if(p.banner==='off')return;const lay=frLay(),k=PW/1080;
  for(const o of (S.settings.overlays||[])){const on=lay.banners==null?o.enabled!==false:lay.banners.includes(o.file);
    if(!on||!/\.(png|webp|jpe?g)$/i.test(o.file))continue;const im=ovImgs[o.file];
    if(!im){const n=ovImgs[o.file]=new Image();n.onload=liveDraw;n.src='/overlay/'+encodeURIComponent(o.file);continue}
    if(!im.complete||!im.naturalWidth)continue;if(o.position==='full'){y.drawImage(im,0,0,PW,PH);continue}
    const pos=p.banner==='layout'?o.position:p.banner,off=p.banner==='layout'?(o.offset||0)*k:0,h=PW*im.naturalHeight/im.naturalWidth;
    y.drawImage(im,0,(pos==='top'?0:pos==='bottom'?PH-h:seam-h/2)+off,PW,h)}}
function liveLoop(){liveDraw();if(!$('edSrc').paused)liveRAF=requestAnimationFrame(liveLoop);else liveRAF=null}
$('edSrc').addEventListener('play',()=>{if(!liveRAF)liveRAF=requestAnimationFrame(liveLoop)});
['seeked','loadeddata','pause'].forEach(ev=>$('edSrc').addEventListener(ev,()=>{liveDraw();if(secSel>=0)secBoxDraw()}));

// ---------- screenshot of the frame at the playhead ----------
async function shot(vertical){if(!E)return;$('edSrc').pause();const at=+(($('edSrc').currentTime||0)+E.off).toFixed(3);
  try{const r=await api('/api/snapshot',{job:E.job,id:E.id,at,vertical,layout:$('edLayout').value,framing:frSend(),sections:secSend()});
    toast(`<b>Screenshot saved:</b> ${esc(r.name)}<br><span class="tiny mute">${esc(r.folder)}</span><br><button class="link" onclick="api('/api/open_folder',{path:${esc(JSON.stringify(r.folder)).replace(/'/g,'&#39;')}})">Open the folder</button> &nbsp; <button class="link" onclick="pickFolder('screenshot_folder')">Change folder</button>`)}catch(e){}}
$('shotShort').onclick=()=>shot(true);$('shotStream').onclick=()=>shot(false);

// ---------- framing for one Short (trim editor) ----------
// F = this Short's framing (boxes, style, Peanut height). Starts from its own saved framing, else its layout.
let F=null,frOwn=false,frDrag=null;
const frLay=()=>{const src=LY||S.layouts;return src.layouts.find(l=>l.id===$('edLayout').value)||src.layouts[0]};
const frPick=l=>clone({mode:l.mode,top_height:l.top_height||760,avatar:l.avatar||{x:.7,y:.5,w:.3,h:.5},gameplay:l.gameplay||{x:.15,y:0,w:.7,h:1}});
function frInit(own){frOwn=!!own;F=own?clone(own):frPick(frLay());frSync()}
function frSend(){return frOwn?F:'none'}
function frMark(){frOwn=true;frSync()}
function frSync(){if(!F)return;
  $('frState').textContent=frOwn?'Custom framing for this Short':'Using the layout\'s framing';
  document.querySelectorAll('#frMode button').forEach(b=>b.classList.toggle('on',b.dataset.m===F.mode));
  $('frWhich').style.display=F.mode==='blurfit'?'none':'';$('frZoomWrap').style.display=F.mode==='blurfit'?'none':'';
  $('frThWrap').style.display=F.mode==='stack'?'':'none';$('frTh').value=F.top_height;$('frThV').textContent=Math.round(F.top_height/1920*100)+'%';
  if(F.mode==='single')document.querySelector('[name=frw][value=gameplay]').checked=true;
  document.querySelector('[name=frw][value=avatar]').parentElement.style.display=F.mode==='stack'?'':'none';
  const b=F[frSel()];$('frZoom').value=Math.round(b.w*100);frDraw()}
const frSel=()=>document.querySelector('[name=frw]:checked').value;
function frDraw(){liveDraw();if(!F||$('frPanel').style.display==='none')return;
  const v=$('edSrc'),W=v.videoWidth,H=v.videoHeight,c=$('frCan'),x=c.getContext('2d');
  if(W){c.width=960;c.height=Math.round(960*H/W);x.drawImage(v,0,0,c.width,c.height)}
  for(const k of ['avatar','gameplay']){const b=F[k],e=$('f_'+k);
    e.style.display=(k==='gameplay'?F.mode!=='blurfit':F.mode==='stack')?'block':'none';
    e.style.left=b.x*100+'%';e.style.top=b.y*100+'%';e.style.width=b.w*100+'%';e.style.height=b.h*100+'%'}
  const p=$('frPrev'),y=p.getContext('2d'),PW=270,PH=480;y.fillStyle='#1a1b1f';y.fillRect(0,0,PW,PH);if(!W)return;
  const cover=(b,dy,dh)=>{let sx=b.x*W,sy=b.y*H,sw=b.w*W,sh=b.h*H;const r=PW/dh;
    if(sw/sh>r){const nw=sh*r;sx+=(sw-nw)/2;sw=nw}else{const nh=sw/r;sy+=(sh-nh)/2;sh=nh}
    y.drawImage(v,sx,sy,sw,sh,0,dy,PW,dh)};
  const top=F.top_height/1920*PH;
  if(F.mode==='stack'){cover(F.avatar,0,top);cover(F.gameplay,top,PH-top)}
  else if(F.mode==='single')cover(F.gameplay,0,PH);
  else{y.filter='blur(6px) brightness(0.8)';cover({x:0,y:0,w:1,h:1},0,PH);y.filter='none';const h=PW*H/W;y.drawImage(v,0,(PH-h)/2,PW,h)}
  const seam=F.mode==='stack'?top:F.mode==='single'?PH/2:(PH-PW*H/W)/2,lay=frLay();
  for(const o of (S.settings.overlays||[])){const on=lay.banners==null?o.enabled!==false:lay.banners.includes(o.file);
    if(!on||!/\.(png|webp|jpe?g)$/i.test(o.file))continue;const im=ovImgs[o.file];
    if(!im){const n=ovImgs[o.file]=new Image();n.onload=frDraw;n.src='/overlay/'+encodeURIComponent(o.file);continue}
    if(!im.complete||!im.naturalWidth)continue;if(o.position==='full'){y.drawImage(im,0,0,PW,PH);continue}
    const h=PW*im.naturalHeight/im.naturalWidth,off=(o.offset||0)/4;y.drawImage(im,0,(o.position==='top'?0:o.position==='bottom'?PH-h:seam-h/2)+off,PW,h)}
  if(SAFE)safeZones(p);
}
$('frToggle').onclick=()=>{const p=$('frPanel'),open=p.style.display==='none';p.style.display=open?'':'none';
  $('frToggle').innerHTML='Framing for this Short '+(open?'&#9652;':'&#9662;');if(open){$('edSrc').pause();frDraw()}};
['seeked','loadeddata','pause'].forEach(ev=>$('edSrc').addEventListener(ev,frDraw));
document.querySelectorAll('#frMode button').forEach(b=>b.onclick=()=>{F.mode=b.dataset.m;frMark()});
document.querySelectorAll('[name=frw]').forEach(r=>r.onchange=()=>frSync());
$('frZoom').oninput=()=>{const k=frSel(),b=F[k],cx=b.x+b.w/2,cy=b.y+b.h/2,ar=b.h/b.w;
  let w=Math.min(1,+$('frZoom').value/100),h=Math.min(1,w*ar);w=h/ar;
  F[k]={w,h,x:Math.min(1-w,Math.max(0,cx-w/2)),y:Math.min(1-h,Math.max(0,cy-h/2))};frOwn=true;$('frState').textContent='Custom framing for this Short';frDraw()};
$('frTh').oninput=()=>{F.top_height=+$('frTh').value;frMark()};
const frPos=e=>{const r=$('frStage').getBoundingClientRect();return[Math.min(1,Math.max(0,(e.clientX-r.left)/r.width)),Math.min(1,Math.max(0,(e.clientY-r.top)/r.height))]};
$('frStage').onmousedown=e=>{if(!F||F.mode==='blurfit')return;e.preventDefault();const p=frPos(e),k=frSel(),b=F[k];
  frDrag=(p[0]>=b.x&&p[0]<=b.x+b.w&&p[1]>=b.y&&p[1]<=b.y+b.h)?{move:true,k,dx:p[0]-b.x,dy:p[1]-b.y}:{move:false,k,s:p}};
window.addEventListener('mousemove',e=>{if(!frDrag)return;const p=frPos(e),b=F[frDrag.k];
  if(frDrag.move){b.x=Math.min(1-b.w,Math.max(0,p[0]-frDrag.dx));b.y=Math.min(1-b.h,Math.max(0,p[1]-frDrag.dy))}
  else F[frDrag.k]={x:Math.min(frDrag.s[0],p[0]),y:Math.min(frDrag.s[1],p[1]),w:Math.max(.03,Math.abs(p[0]-frDrag.s[0])),h:Math.max(.03,Math.abs(p[1]-frDrag.s[1]))};
  frOwn=true;$('frState').textContent='Custom framing for this Short';frDraw()});
window.addEventListener('mouseup',()=>{if(frDrag){frDrag=null;frSync()}});
$('edLayout').addEventListener('change',()=>{if(!frOwn)frInit(null)});
$('frReset').onclick=()=>{frInit(null);toast('<b>Back to the layout:</b> press Update Short to re-cut with it.')};
$('frUse').onclick=()=>{frOwn=true;$('edSave').click()};
$('frSaveLy').onclick=async()=>{const name=prompt('Name for the new layout (e.g. "GTA close-up"):');if(!name)return;
  const data=clone(LY||S.layouts),base=frLay();
  const l=Object.assign({id:newId(),name:name.trim().slice(0,40),banners:base.banners??null},clone(F));
  data.layouts.push(l);await api('/api/layouts',data);S.layouts=clone(data);if(LY){LY.layouts.push(clone(l))}
  updateLayoutMenus();$('edLayout').value=l.id;frOwn=false;frSync();
  toast('<b>Saved "'+esc(l.name)+'".</b> Pick it when you make Shorts. Press Update Short to use it here.')};

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

poll().then(()=>{if(S){$('kwCpu').style.display=S.hw.gpu_speech&&S.settings.use_gpu?'none':'block';updateLayoutMenus();liveFill();mkDraw()}});loadSearches();loadComps();loadCols();setInterval(poll,1500);liveTick();setInterval(()=>{if(!document.hidden)liveTick()},2000);
</script></body></html>"""
