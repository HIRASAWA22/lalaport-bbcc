# -*- coding: utf-8 -*-
import json
data = json.load(open('/home/claude/shops.json', encoding='utf-8'))
DATA_JS = json.dumps(data, ensure_ascii=False)

# 娘向け「推しレコメンド」セレクト（実在店名で参照）
RECO = [
 {"t":"韓国コスメ・ビューティー","d":"K-ビューティーを試すならここ",
  "names":["OnlyKorea","Sasa","elianto","Beauty Scents","I-Scent","IKUKO"]},
 {"t":"韓国グルメ＆カフェ","d":"韓国気分のごはん・スイーツ・カフェ",
  "names":["Seoul Garden","KorFry","Oiso Korean Traditional Cuisine & Cafe","TOUS les JOURS","CU MART","Photoism PLAY"]},
 {"t":"トレンドファッション","d":"今っぽい服をチェック",
  "names":["WEGO","6IXTY8IGHT","Global Work","SODA","Max Fashion","Earth Music and Ecology","F.O.S","MiX.Store"]},
 {"t":"アクセ＆小物","d":"アクセサリー・バッグで仕上げる",
  "names":["Lovisa","The Green Party","Swarovski","Coloris","NIID","LARRIE"]},
 {"t":"映えスイーツ＆ドリンク","d":"写真も映えるおやつタイム",
  "names":["MIXUE","Gong Cha","Tealive","Llao Llao","Matcha Eight","ZUS Coffee","Ben Gong's Tea","YOYO Bird's Nest Dessert Expert"]},
 {"t":"フォト＆映え雑貨","d":"プリで撮って、雑貨をおみやげに",
  "names":["Photoism PLAY","KKV","Miniso Friends","3COINS","Daiso","Doko Koko Goods"]},
]
RECO_JS = json.dumps(RECO, ensure_ascii=False)

OFFICIAL = "https://mitsui-shopping-park.com.my/LaLaportBBCC/Main/Index"

html = r'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>ららぽーとBBCC 攻略ブック</title>
<style>
:root{
  /* UI-002 色彩モード：標準（承認済みアイボリー基調）。初期表示はこれ */
  --bg:#f4f0ea; --card:#ffffff; --ink:#2c2a29; --sub:#5c7a95; --line:#dcd4c9; --hookbg:#eef2f5;
  --accent:#3f6486; --topbg:#ece6da; --topink:#2c2a29;
  --shop:#3f6a7d; --food:#b5532f; --super:#5f7d50; --conveni:#7a6b96; --ent:#9c5570; --service:#8a7a5c;
  --maxw:960px;
  --safe-b:env(safe-area-inset-bottom,0px);
}
/* クリア（白基調・明瞭） */
html[data-mode="clear"]{ --bg:#f7f9fb; --card:#ffffff; --ink:#1c2430; --sub:#5a6b7a; --line:#e4e8ee; --hookbg:#eef4fa; --accent:#2f6796; --topbg:#ffffff; --topink:#1c2430; }
/* ソフト（刺激を抑えたやわらかい配色） */
html[data-mode="soft"]{ --bg:#e9ebe8; --card:#f6f7f4; --ink:#2c342f; --sub:#6f7a72; --line:#d5d9d3; --hookbg:#e7eef0; --accent:#4a7488; --topbg:#e3e6e0; --topink:#2c342f; }
/* ダーク（暗所向け・コントラスト確保） */
html[data-mode="dark"]{ --bg:#12161a; --card:#1b2127; --ink:#e9edf1; --sub:#9fb0bd; --line:#2c353d; --hookbg:#20303a; --accent:#79b3d1; --topbg:#0f151a; --topink:#e9edf1; }
/* ハイコントラスト（文字・枠・選択を明確に） */
html[data-mode="contrast"]{ --bg:#ffffff; --card:#ffffff; --ink:#000000; --sub:#2a2a2a; --line:#4d4d4d; --hookbg:#e6eef5; --accent:#0b3d5c; --topbg:#ffffff; --topink:#000000; }
html[data-mode="contrast"] .chip{border-width:2px}
html[data-mode="contrast"] .card,html[data-mode="contrast"] .mapstore{border-width:2px}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Hiragino Kaku Gothic ProN","Yu Gothic",Meiryo,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  line-height:1.55;word-break:normal;line-break:strict;overflow-x:hidden}
.nw{white-space:nowrap}
a{color:inherit}

/* ---- masthead ---- */
.mast{background:var(--topbg);color:var(--topink);padding:11px 14px 11px;border-bottom:1px solid var(--line)}
.mast .kicker{display:none}
.mast h1{font-size:20px;line-height:1.3;margin:0 0 3px;font-weight:600;letter-spacing:.04em;color:var(--ink);
  font-family:"Hiragino Mincho ProN","Yu Mincho",YuMincho,"MS PMincho",serif}
.mast .meta{font-size:10.5px;color:var(--sub);margin:0;line-height:1.45}
.mast .meta a{color:var(--accent);text-decoration:underline;text-underline-offset:2px;font-weight:700}

/* ---- view tabs ---- */
.tabs{display:flex;gap:0;background:var(--topbg);position:sticky;top:0;z-index:30;border-bottom:1px solid var(--line)}
.tabs button{flex:1;appearance:none;border:0;background:transparent;color:var(--sub);
  font-size:14px;font-weight:800;padding:11px 8px;cursor:pointer;border-bottom:3px solid transparent}
.tabs button.on{color:var(--ink);border-bottom-color:var(--accent)}

/* ---- sticky controls ---- */
.controls{background:var(--bg);padding:10px 12px 8px;border-bottom:1px solid var(--line)}
.search{width:100%;padding:13px 14px;font-size:16px;border:2px solid var(--ink);border-radius:14px;
  background:var(--card);color:var(--ink);outline:none;font-weight:600}
.search::placeholder{color:var(--sub);font-weight:500}
.search:focus{border-color:var(--accent)}
.rowlabel{font-size:10.5px;letter-spacing:.12em;color:var(--sub);font-weight:800;margin:9px 2px 5px}
.chips{display:flex;flex-wrap:wrap;gap:7px;padding-bottom:3px}
.chip{flex:0 0 auto;padding:7px 13px;font-size:13px;font-weight:700;border-radius:999px;
  border:1.5px solid var(--line);background:var(--card);color:var(--sub);cursor:pointer;white-space:nowrap}
.chip.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.chip.food.on{background:var(--accent);border-color:var(--accent);color:#fff}
.quick .chip{border-style:dashed}

.wrap{max-width:var(--maxw);margin:0 auto;padding:0 12px calc(40px + var(--safe-b))}
.count{font-size:12px;color:var(--sub);font-weight:700;margin:12px 3px 8px}

/* ---- card grid ---- */
.grid{display:grid;grid-template-columns:1fr;gap:10px}
@media (min-width:680px){ .grid{grid-template-columns:1fr 1fr} }
.card{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);
  border-radius:16px;overflow:hidden}
.logowrap{height:96px;display:flex;align-items:center;justify-content:center;
  background:#fff;border-bottom:1px solid var(--line);padding:8px 16px;box-sizing:border-box}
.logo{height:54px;width:auto;max-width:78%;object-fit:contain;display:block}
.logo.crop{width:82%;height:52px;max-width:82%;object-fit:cover;object-position:center top;border-radius:4px}
.logoph{font-size:13px;font-weight:800;color:var(--sub);text-align:center;line-height:1.3}
.body{min-width:0;padding:11px 13px 13px}
.nm{font-size:15px;font-weight:800;letter-spacing:.01em;margin:1px 0 4px;overflow-wrap:anywhere}
.badges{display:flex;flex-wrap:wrap;gap:5px;align-items:center;margin-bottom:5px}
.tag{font-size:10px;font-weight:800;padding:2px 7px;border-radius:6px;color:#fff}
.b-shop{background:var(--shop)}.b-food{background:var(--food)}.b-super{background:var(--super)}
.b-conveni{background:var(--conveni)}.b-ent{background:var(--ent)}.b-service{background:var(--service)}
.floor{font-size:11px;font-weight:800;border:1.5px solid var(--ink);border-radius:6px;padding:1px 6px}
.price{font-size:11px;font-weight:800;color:var(--accent)}
.genre{font-size:12px;color:var(--sub);font-weight:700}
.cardmap{appearance:none;border:1.5px solid var(--accent);background:transparent;color:var(--accent);
  font-weight:800;font-size:11px;border-radius:7px;padding:2px 8px;cursor:pointer;white-space:nowrap}
.cardmap:hover{background:var(--accent);color:#fff}
.hook{font-size:12.5px;line-height:1.5;color:var(--ink);background:var(--hookbg);border-left:3px solid var(--accent);
  padding:5px 8px;border-radius:0 8px 8px 0;margin-top:6px;font-weight:600}
.note{font-size:12px;color:var(--sub);margin-top:3px}
.area{font-size:12px;color:var(--accent);font-weight:800;margin-top:3px}
.hours{font-size:12px;color:#b45309;font-weight:800;margin-top:3px}
.frame{border:1.5px solid var(--line);border-radius:14px;padding:12px;margin:14px 0;background:var(--card)}
.frametitle{font-size:16px;font-weight:600;margin:2px 2px 10px;color:var(--ink);letter-spacing:.03em;
  font-family:"Hiragino Mincho ProN","Yu Mincho",YuMincho,"MS PMincho",serif}
.unit{font-size:10.5px;color:var(--sub)}
.empty{padding:44px 12px;text-align:center;color:var(--sub);font-weight:700}

.sec{margin:20px 0 6px}
.sec .st{display:flex;align-items:baseline;gap:9px;border-bottom:3px solid var(--ink);padding-bottom:5px;margin-bottom:11px}
.sec .st .num{font-size:12px;font-weight:900;color:var(--accent)}
.sec .st h3{margin:0;font-size:17px;font-weight:900}
.sec .st .sd{font-size:11.5px;color:var(--sub);font-weight:700;margin-left:auto}
.mapwrap{margin:12px 0}
.mapzoombar{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin:2px 2px 8px}
.zbtn{min-height:44px;padding:8px 13px;border:1.5px solid var(--line);border-radius:10px;
  background:var(--card);color:var(--ink);font-weight:800;font-size:13px;cursor:pointer;line-height:1.1}
.zlink{margin-left:auto;color:var(--accent);font-weight:800;text-decoration:none;font-size:12px;padding:6px 2px}
.mapcap{font-size:12px;color:var(--sub);font-weight:700;margin:0 2px 6px}
.mapcap2{font-size:11px;color:var(--sub);margin:6px 2px 0}
.mapview{overflow:auto;max-height:72vh;border:1px solid var(--line);border-radius:12px;
  background:var(--card);-webkit-overflow-scrolling:touch;touch-action:pan-x pan-y pinch-zoom}
.mapview img{display:block;width:100%}
.mapimg{width:100%;border:1px solid var(--line);border-radius:12px;background:var(--card);display:block}
.maptools{display:flex;justify-content:space-between;align-items:center;gap:8px;margin:8px 2px;font-size:12px;color:var(--sub)}
.maptools a{color:var(--accent);font-weight:800;text-decoration:none}
/* 地図と連動：選択中の店（区画番号を大きく） */
.mapstore{background:var(--card);border:1.5px solid var(--accent);border-radius:14px;
  padding:12px 14px 13px;margin:12px 0 6px;text-align:center}
.mapstore .ms-nm{font-size:15px;font-weight:700;line-height:1.3;color:var(--sub);
  font-family:"Hiragino Mincho ProN","Yu Mincho",YuMincho,"MS PMincho",serif}
.mapstore .ms-numrow{display:flex;gap:10px;align-items:center;justify-content:center;margin:4px 0 2px;flex-wrap:wrap}
.mapstore .ms-flr{font-size:15px;font-weight:800;color:#fff;background:var(--accent);
  border-radius:8px;padding:3px 11px;letter-spacing:.02em}
.mapstore .ms-num{font-size:40px;font-weight:900;color:var(--accent);letter-spacing:.02em;line-height:1.05}
.mapstore .ms-cap{font-size:11.5px;color:var(--sub);font-weight:700;margin-top:2px}
.mapstore .ms-warn{font-size:12px;color:var(--food);font-weight:800;margin-top:8px;line-height:1.45}
.inlinemap{margin:4px 0 14px}
.inlinemap>summary{cursor:pointer;font-weight:800;font-size:13px;color:var(--accent);list-style:none;padding:9px 12px;border:1.5px dashed var(--line);border-radius:10px;display:inline-block}
.inlinemap>summary::-webkit-details-marker{display:none}
.inlinemap[open]>summary{margin-bottom:8px}
.foot{color:var(--sub);font-size:11px;margin-top:26px;border-top:1px solid var(--line);padding-top:12px;line-height:1.7}
.hide{display:none!important}
/* UI-002 配色モード切替バー（ヘッダ常設・文字ラベル・折り返し） */
.modebar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:10px}
.modebar .modelbl{font-size:11px;letter-spacing:.1em;font-weight:800;color:var(--topink);opacity:.7;margin-right:2px}
.modebar .modebtn{min-height:44px;padding:8px 13px;border-radius:11px;border:1.5px solid var(--line);
  background:var(--card);color:var(--ink);font-size:13px;font-weight:800;cursor:pointer;line-height:1.15}
.modebar .modebtn.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.modebar .modebtn.on::before{content:"✓ "}
</style>
</head>
<body>
<div class="mast">
  <p class="kicker">MALAYSIA ・ KUALA LUMPUR</p>
  <h1>ららぽーとBBCC 攻略ブック</h1>
  <p class="meta">三井ショッピングパーク ららぽーと ブキッ・ビンタン・シティ・センター<br>
  全 <span id="total"></span> 店　|　<span class="nw">営業時間 10:00–22:00</span>（館全体の目安）　|　<a href="''' + OFFICIAL + r'''" target="_blank" rel="noopener">公式サイト</a></p>
  <div class="modebar" role="group" aria-label="配色モード切替">
    <span class="modelbl">配色</span>
    <button type="button" class="modebtn" data-m="standard" onclick="setMode('standard')">標準</button>
    <button type="button" class="modebtn" data-m="clear" onclick="setMode('clear')">クリア</button>
    <button type="button" class="modebtn" data-m="soft" onclick="setMode('soft')">ソフト</button>
    <button type="button" class="modebtn" data-m="dark" onclick="setMode('dark')">ダーク</button>
    <button type="button" class="modebtn" data-m="contrast" onclick="setMode('contrast')">ハイコントラスト</button>
  </div>
</div>
<div class="tabs">
  <button id="tab-list" class="on" onclick="setView('list')">検索</button>
  <button id="tab-map" onclick="setView('map')">マップ</button>
  <button id="tab-hours" onclick="setView('hours')">早朝/深夜</button>
</div>

<!-- 検索ビュー -->
<div id="view-list">
  <div class="controls">
    <input id="q" class="search" type="search" placeholder="日本語でOK" autocomplete="off">
    <div class="rowlabel">分類　<span style="font-weight:600;color:var(--sub);font-size:11px">タップでON／もう一度でOFF・複数選択OK（掛け合わせて絞り込み）</span></div>
    <div class="chips" id="buckets"></div>
    <div class="rowlabel">サブ分類（ジャンル）</div>
    <div class="chips" id="genres"></div>
    <div class="rowlabel">フロア</div>
    <div class="chips" id="floors"></div>
    <div class="rowlabel">予算（飲食）</div>
    <div class="chips" id="prices"></div>
  </div>
  <div class="wrap">
    <div class="count" id="count"></div>
    <div id="floormap-inline"></div>
    <div class="grid" id="rows"></div>
    <div class="empty hide" id="empty">該当なし。別の言葉でも試してみてください（例：カフェ、スイーツ、スーツケース、コスメ）</div>
    <div class="foot">
      データ出典：ららぽーとBBCC公式サイト（店名・フロア・区画）。分類・ジャンル・日本語検索ワード・予算ランク・特徴メモは、店名やブランド・フロアからの目安で、公式の確定情報ではありません。予算の目安：¥お手軽／¥¥普通／¥¥¥ちょっと贅沢。星評価のような口コミ数値は含みません。営業状況や区画は変わることがあるため、現地の館内表示もご確認ください
    </div>
  </div>
</div>


<!-- 早朝/深夜ビュー -->
<div id="view-hours" class="hide">
  <div class="wrap">
    <div class="frame">
      <div class="frametitle">🌅 早朝より営業（10:00前オープン）</div>
      <div class="grid" id="rows-early"></div>
    </div>
    <div class="frame">
      <div class="frametitle">🌙 深夜まで営業（23:00以降）</div>
      <div class="grid" id="rows-late"></div>
    </div>
    <div class="foot">営業時間は公式サイト各店ページで確認した2026年8月時点の情報です（曜日で異なる店あり）。館の標準は10:00–22:00。この2枠はそこから外れる店のみ掲載。Special Open Hours指定でも標準どおり22:00閉店の店（Hut Dining Buffet／Shabu-yo／Sushi Yoshi）や、公式に時間掲載のない店（Tan Ngan Lo）は未掲載です</div>
  </div>
</div>

<!-- マップビュー -->
<div id="view-map" class="hide">
  <div class="controls">
    <div class="rowlabel">フロアを選ぶ</div>
    <div class="chips" id="mapfloors"></div>
  </div>
  <div class="wrap">
    <div id="map-store" class="mapstore hide"></div>
    <div class="mapwrap">
      <div class="mapzoombar">
        <button type="button" class="zbtn" onclick="mapZoom(-1)">− 縮小</button>
        <button type="button" class="zbtn" onclick="mapZoomFit()">フィット</button>
        <button type="button" class="zbtn" onclick="mapZoom(1)">＋ 拡大</button>
        <a id="map-open" href="#" target="_blank" rel="noopener" class="zlink">別タブで拡大 ↗</a>
      </div>
      <div id="map-caption" class="mapcap"></div>
      <div id="mapview" class="mapview"><img id="map-img" alt="フロアマップ"></div>
      <div class="mapcap2">指でのピンチ操作でも拡大できます。上下左右にスワイプで移動</div>
    </div>
    <div class="foot">フロアマップは公式サイトの画像です（上部の館名バナーはカットしています）。表示にはネット接続が必要です。上の「区画番号」を、この地図に印字された番号と照らし合わせると、選んだ店の場所が特定できます</div>
  </div>
</div>

<script>
const DATA = __DATA__;
const BYNAME = {}; DATA.forEach(d=>BYNAME[d.name]=d);
const MAPPRE='https://storagelpklpiweb.blob.core.windows.net/lpkl/Image/Upload/';
const FLOORMAPS={
 'LG1':MAPPRE+'20260720/1dc6a011-a2b1-4cbd-a320-bd9a2570f5bf.jpg',
 'G':MAPPRE+'20260720/c82173a1-cb12-4811-bb2a-254b47694b7c.jpg',
 'L1':MAPPRE+'20260720/4296797b-4b98-4a7d-a5c6-3e715d2772ac.jpg',
 'L2':MAPPRE+'20260720/2c0cd23a-7f75-4fe4-a576-f1518aa2d083.jpg',
 'L3':MAPPRE+'20260720/7794038a-2e08-48f8-8b2c-fc1bc8cf9da4.jpg',
 'L4':MAPPRE+'20260720/44535cb1-969a-4fb1-a337-7ba571378edf.jpg',
 'L5':MAPPRE+'20260720/95802d3d-4509-4061-89cc-bb5b85a005eb.jpg'
};
const FLOORLABEL={'LG1':'LG1（地下・グルメ）','G':'G（1F・入口）','L1':'L1','L2':'L2','L3':'L3','L4':'L4（フードコート）','L5':'L5（屋上）'};
document.getElementById('total').textContent = DATA.length;
const BL={shop:'ショップ',food:'飲食',super:'スーパー',conveni:'コンビニ的',ent:'娯楽',service:'サービス美容'};
const BORDER={shop:'b-shop',food:'b-food',super:'b-super',conveni:'b-conveni',ent:'b-ent',service:'b-service'};
const FLOORS=['LG1','G','L1','L2','L3','L4','L5'];
const state={q:'',mapFloor:'LG1'};
// 複数選択フィルタ（同種はOR、種類間はAND）。空＝すべて
const F={buckets:new Set(),genres:new Set(),floors:new Set(),prices:new Set()};
function toggleIn(set,val){ if(set.has(val)) set.delete(val); else set.add(val); }
function paintChips(wrap,set){ [...wrap.children].forEach(x=>{ const v=x.dataset.val;
  x.classList.toggle('on', v==='all' ? set.size===0 : set.has(v)); }); }

function esc(s){return (s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function phLabel(d){return (d.genre||'').slice(0,8);}
function cardHTML(d){
  const logo = d.img
    ? '<img class="logo'+(d.crop?' crop':'')+'" loading="lazy" src="'+esc(d.img)+'" alt="" onerror="this.outerHTML=\'<span class=&quot;logoph&quot;>'+esc(phLabel(d))+'</span>\'">'
    : '<span class="logoph">'+esc(phLabel(d))+'</span>';
  const img = '<div class="logowrap">'+logo+'</div>';
  const price = d.priceLabel ? '<span class="price nw">'+esc(d.priceLabel)+'</span>' : '';
  const note = d.note ? '<div class="note">'+esc(d.note)+'</div>' : '';
  const hook = d.hook ? '<div class="hook">'+esc(d.hook)+'</div>' : '';
  const area = d.area ? '<div class="area">📍 '+esc(d.area)+'</div>' : '';
  const hours = d.hours ? '<div class="hours">🕒 '+esc(d.hours)+'</div>' : '';
  const mapbtn = FLOORMAPS[d.floor] ? '<button class="cardmap" data-nm="'+esc(d.name)+'" onclick="showStoreMap(this)">🗺 地図</button>' : '';
  return '<div class="card">'+img+
    '<div class="body"><div class="nm">'+esc(d.name)+'</div>'+
    '<div class="badges"><span class="tag '+BORDER[d.bucket]+'">'+BL[d.bucket]+'</span>'+
    '<span class="floor nw">'+esc(d.floor)+'</span>'+price+mapbtn+'</div>'+
    '<div class="genre">'+esc((d.tags||[d.genre]).join('・'))+'　<span class="unit nw">'+esc(d.unit)+'</span></div>'+
    hook+area+hours+note+'</div></div>';
}

function makeChip(parent,label,val,active,onclick,cls){
  const c=document.createElement('span');
  c.className='chip'+(cls||'')+(active?' on':'');
  c.textContent=label;c.dataset.val=val;c.onclick=onclick;parent.appendChild(c);return c;
}
// ---- bucket chips（複数選択トグル）----
const bc={};DATA.forEach(d=>bc[d.bucket]=(bc[d.bucket]||0)+1);
const bwrap=document.getElementById('buckets');
function clickBucket(val){
  if(val==='all') F.buckets.clear(); else toggleIn(F.buckets,val);
  paintChips(bwrap,F.buckets); buildGenres(); renderList();
}
makeChip(bwrap,'すべて '+DATA.length,'all',true,()=>clickBucket('all'));
['shop','food','super','conveni','ent','service'].forEach(b=>{if(bc[b])makeChip(bwrap,BL[b]+' '+bc[b],b,false,()=>clickBucket(b));});
// ---- genre (sub-category) chips, rebuilt per selected buckets ----
const gwrap=document.getElementById('genres');
function clickGenre(val){
  if(val==='all') F.genres.clear(); else toggleIn(F.genres,val);
  paintChips(gwrap,F.genres); renderList();
}
function buildGenres(){
  const pool=DATA.filter(d=>F.buckets.size===0||F.buckets.has(d.bucket));
  const gc={};pool.forEach(d=>(d.tags||[d.genre]).forEach(t=>gc[t]=(gc[t]||0)+1));
  const genres=Object.keys(gc).sort((a,b)=>gc[b]-gc[a]||a.localeCompare(b));
  [...F.genres].forEach(g=>{ if(!gc[g]) F.genres.delete(g); }); // 対象外になったジャンルは解除
  gwrap.innerHTML='';
  makeChip(gwrap,'すべて','all',F.genres.size===0,()=>clickGenre('all'));
  genres.forEach(g=>makeChip(gwrap,g+' '+gc[g],g,F.genres.has(g),()=>clickGenre(g)));
}
// ---- floor chips（複数選択トグル）----
const fwrap=document.getElementById('floors');
function clickFloor(val){
  if(val==='all') F.floors.clear(); else toggleIn(F.floors,val);
  paintChips(fwrap,F.floors); renderList();
}
makeChip(fwrap,'すべて','all',true,()=>clickFloor('all'));
FLOORS.forEach(f=>{if(DATA.some(d=>d.floor===f))makeChip(fwrap,f,f,false,()=>clickFloor(f));});
// ---- price chips（複数選択トグル）----
const pwrap=document.getElementById('prices');
function clickPrice(val){
  if(val==='all') F.prices.clear(); else toggleIn(F.prices,val);
  paintChips(pwrap,F.prices); renderList();
}
makeChip(pwrap,'すべて','all',true,()=>clickPrice('all'),' food');
makeChip(pwrap,'¥ お手軽','1',false,()=>clickPrice('1'),' food');
makeChip(pwrap,'¥¥ 普通','2',false,()=>clickPrice('2'),' food');
makeChip(pwrap,'¥¥¥ 贅沢','3',false,()=>clickPrice('3'),' food');
document.getElementById('q').addEventListener('input',e=>{state.q=e.target.value.trim().toLowerCase();renderList();});

function renderList(){
  const rows=document.getElementById('rows');
  const terms=state.q.split(/\s+/).filter(Boolean);
  let out='',n=0;
  DATA.forEach(d=>{
    if(F.buckets.size && !F.buckets.has(d.bucket))return;
    if(F.genres.size && !(d.tags||[]).some(t=>F.genres.has(t)))return;
    if(F.floors.size && !F.floors.has(d.floor))return;
    if(F.prices.size){ if(d.bucket!=='food' || !F.prices.has(String(d.price)))return; }
    if(terms.length&&!terms.every(t=>d.kw.includes(t)))return;
    n++;out+=cardHTML(d);
  });
  rows.innerHTML=out;
  const im=document.getElementById('floormap-inline');
  const onef=F.floors.size===1 ? [...F.floors][0] : null;
  if(onef && FLOORMAPS[onef]){
    im.innerHTML='<details class="inlinemap"><summary>🗺 '+(FLOORLABEL[onef]||onef)+' の地図を見る</summary>'+
      '<img class="mapimg" loading="lazy" src="'+FLOORMAPS[onef]+'" alt="floor map"></details>';
  } else { im.innerHTML=''; }
  document.getElementById('count').textContent=n+' 店を表示中';
  document.getElementById('empty').classList.toggle('hide',n>0);
}
function renderHours(){
  const early=DATA.filter(d=>(d.openTags||[]).some(t=>t.indexOf('早朝')===0));
  const late=DATA.filter(d=>(d.openTags||[]).includes('深夜'));
  document.getElementById('rows-early').innerHTML=early.map(cardHTML).join('')||'<div class="empty">該当なし</div>';
  document.getElementById('rows-late').innerHTML=late.map(cardHTML).join('')||'<div class="empty">該当なし</div>';
}
function setView(v){
  ['list','map','hours'].forEach(x=>{
    document.getElementById('view-'+x).classList.toggle('hide',v!==x);
    document.getElementById('tab-'+x).classList.toggle('on',v===x);
  });
  window.scrollTo(0,0);
}
// ---- floor map（ズーム＋上部バナーのカット）----
const mfwrap=document.getElementById('mapfloors');
var mapZoomLv=1;
var MAP_BANNER=0.09;   // 地図画像 上部の館名バナーを高さ比でカット
function applyMapZoom(){
  var img=document.getElementById('map-img'); if(!img) return;
  img.style.width=(Math.round(mapZoomLv*100))+'%';
  var crop=function(){ var h=img.getBoundingClientRect().height; if(h>0) img.style.marginTop=(-Math.round(h*MAP_BANNER))+'px'; };
  if(img.complete && img.naturalWidth){ crop(); }
  else { img.onload=crop; }
}
function mapZoom(d){ mapZoomLv=Math.min(4, Math.max(1, +(mapZoomLv+(d>0?0.6:-0.6)).toFixed(2))); applyMapZoom(); }
function mapZoomFit(){ mapZoomLv=1; applyMapZoom(); var v=document.getElementById('mapview'); if(v) v.scrollTo(0,0); }
function renderMap(){
  const f=state.mapFloor||'LG1';
  const url=FLOORMAPS[f]||'';
  document.getElementById('map-img').src=url;
  document.getElementById('map-open').href=url;
  mapZoomLv=1; applyMapZoom();
  document.getElementById('map-caption').textContent='フロア：'+(FLOORLABEL[f]||f);
  [...mfwrap.children].forEach(x=>x.classList.toggle('on',x.dataset.val===f));
  // 選択中の店を地図の上に表示（連動）
  const box=document.getElementById('map-store');
  const d=state.mapStore ? BYNAME[state.mapStore] : null;
  if(d){
    const onfloor = d.floor===f;
    box.innerHTML=
      '<div class="ms-nm">'+esc(d.name)+'</div>'+
      '<div class="ms-numrow"><span class="ms-flr nw">'+esc(d.floor)+'</span>'+
        '<span class="ms-num nw">'+esc(d.unit)+'</span></div>'+
      '<div class="ms-cap">↑ この区画番号を、下の地図の印字と照らし合わせてください</div>'+
      (onfloor?'':'<div class="ms-warn">※この店は '+esc(d.floor)+' 階です。上のフロアボタンで '+esc(d.floor)+' を選ぶと地図が切り替わります</div>');
    box.classList.remove('hide');
  } else {
    box.innerHTML=''; box.classList.add('hide');
  }
}
function selectMapFloor(f){ state.mapFloor=f; state.mapStore=null; renderMap(); }
function showStoreMap(btn){
  const nm=btn.getAttribute('data-nm'); const d=BYNAME[nm];
  if(!d){ return; }
  state.mapStore=nm; state.mapFloor=FLOORMAPS[d.floor]?d.floor:(state.mapFloor||'LG1');
  renderMap(); setView('map');
}
function showFloorMap(f){ state.mapFloor=f; state.mapStore=null; renderMap(); setView('map'); }
FLOORS.forEach(f=>{ if(FLOORMAPS[f]) makeChip(mfwrap,(FLOORLABEL[f]||f),f,f===state.mapFloor,()=>selectMapFloor(f)); });
renderMap();
buildGenres();renderList();renderHours();

// ---- UI-002 色彩モード（5種・端末保存・不正値は標準へ復旧・OS自動追従なし）----
var MODES=['standard','clear','soft','dark','contrast'];
var MODEKEY='lalaportBbccColorMode';
function setMode(m){
  if(MODES.indexOf(m)<0) m='standard';
  document.documentElement.setAttribute('data-mode',m);
  try{ localStorage.setItem(MODEKEY,m); }catch(e){}
  var bs=document.querySelectorAll('.modebar .modebtn');
  for(var i=0;i<bs.length;i++){
    var on=bs[i].getAttribute('data-m')===m;
    bs[i].classList.toggle('on',on);
    bs[i].setAttribute('aria-pressed', on?'true':'false');
  }
}
(function(){
  var s=null; try{ s=localStorage.getItem(MODEKEY); }catch(e){ s=null; }
  if(MODES.indexOf(s)<0) s='standard';   // 不正値・未設定は標準へ安全復帰
  setMode(s);
})();

</script>
</body>
</html>'''

html = html.replace('__DATA__', DATA_JS)
open('/home/claude/lalaport_bbcc_book.html','w',encoding='utf-8').write(html)
print('wrote html', len(html), 'bytes')
