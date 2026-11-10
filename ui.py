"""Shared look and feel: Claude-style cream/terracotta, light and dark modes, responsive layout."""
from string import Template

import altair as alt
import streamlit as st

import site_config as cfg

BLUE, TEAL, INK, MUTED = "#c96442", "#788c5d", "#141413", "#6b6a63"  # terracotta, sage, ink, warm grey

LIGHT = dict(bg="#faf9f5", side="#f0eee6", card="#ffffff", soft="#f0eee6", line="#e8e6dc", line2="#d9d6c8",
             ink="#141413", body="#3d3d3a", muted="#6b6a63", accent="#c96442", accent2="#788c5d",
             pill_bg="#f4e3da", pill_fg="#a84e2f", pt_bg="#e6ebdd", pt_fg="#55683f",
             weak_bg="#ecebe4", weak_fg="#6b6a63", glow="#f4e3da")
DARK = dict(bg="#1f1e1d", side="#191817", card="#2a2927", soft="#2f2e2b", line="#3d3c39", line2="#4a4945",
            ink="#f5f4ee", body="#d6d4cb", muted="#a3a198", accent="#d97757", accent2="#9bb27a",
            pill_bg="#4a2f25", pill_fg="#f0a58a", pt_bg="#34402a", pt_fg="#b5c99a",
            weak_bg="#3a3936", weak_fg="#b0aea4", glow="#4a2f25")


def is_dark():
    return bool(st.session_state.get("dark", True))   # dark is the default


def palette():
    return DARK if is_dark() else LIGHT


_CSS = Template("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;500;600&display=swap');
:root { --bg:$bg; --side:$side; --card:$card; --soft:$soft; --line:$line; --line2:$line2; --ink:$ink;
        --body:$body; --muted:$muted; --accent:$accent; --accent2:$accent2; --glow:$glow; }

/* ---------- page + Streamlit parts ---------- */
.stApp { background:var(--bg); color:var(--body); }
[data-testid="stHeader"] { background:color-mix(in srgb, var(--bg) 88%, transparent); backdrop-filter:blur(8px);
    transition:transform .3s ease, background-color .7s ease; }
.st-key-themesw { position:fixed; top:.62rem; right:4.4rem; width:58px; height:30px; z-index:1000002;
    transition:transform .3s ease; }
.st-key-themesw iframe { border-radius:30px; display:block; }
[data-testid="stSidebar"] { background:var(--side); border-right:1px solid var(--line); }
[data-testid="stSidebar"] * { color:var(--ink); }
.block-container { max-width:980px; padding-top:2.2rem; }
.stApp p, .stApp li, .stApp label, .stApp td, .stApp th, .stApp span { color:inherit; }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { color:var(--ink); }
h1, h2, h3, .section, .hero h1 { font-family:'Source Serif 4', Georgia, 'Times New Roman', serif !important; }
[data-testid="stCaptionContainer"], .stApp small { color:var(--muted) !important; }
.stApp hr { border-color:var(--line); }
.stApp a { color:var(--accent); }
.stApp code { background:var(--soft); color:var(--ink); }
.stApp blockquote { border-left:3px solid var(--accent); background:var(--soft); padding:.7rem 1rem; border-radius:0 12px 12px 0; margin:1rem 0; }
.stApp blockquote p { margin:0; color:var(--body); }
[data-testid="stTable"] table, [data-testid="stMarkdownContainer"] table { border-color:var(--line); }
[data-testid="stMarkdownContainer"] th { background:var(--soft); color:var(--ink); }
[data-testid="stMarkdownContainer"] td, [data-testid="stMarkdownContainer"] th { border-color:var(--line) !important; }
[data-testid="stMetric"] { background:var(--card); border:1px solid var(--line); border-radius:14px; padding:.8rem 1rem; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color:var(--ink) !important; }
[data-testid="stAlert"], [data-testid="stAlertContainer"], [data-testid="stAlert"] > div {
    background:var(--soft) !important; border:1px solid var(--line); border-radius:14px; }
[data-testid="stAlert"] *, [data-testid="stAlertContainer"] * { color:var(--ink) !important; }
[data-testid="stExpander"] details { background:var(--card); border:1px solid var(--line); border-radius:14px; }
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary *, [data-testid="stExpander"] summary svg {
    color:var(--ink) !important; fill:var(--ink) !important; }
[data-testid="stExpander"], [data-testid="stExpander"] details, [data-testid="stExpander"] summary,
[data-testid="stExpanderDetails"] { background:var(--card) !important; }
[data-testid="stExpander"] summary:hover { background:var(--soft) !important; }
[data-testid="stExpander"] [data-testid="stExpanderDetails"] p, [data-testid="stExpander"] [data-testid="stExpanderDetails"] li,
[data-testid="stExpander"] [data-testid="stExpanderDetails"] span { color:var(--body) !important; }
[data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] *, label p { color:var(--ink) !important; }
input::placeholder, textarea::placeholder { color:var(--muted) !important; opacity:1 !important; }
[data-testid="stMarkdownContainer"] > p, [data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] td, [data-testid="stMarkdownContainer"] th,
[data-testid="stMarkdownContainer"] strong, [data-testid="stMarkdownContainer"] em { color:var(--body); }
[data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3, [data-testid="stMarkdownContainer"] h4 { color:var(--ink); }
[data-testid="stTable"] td, [data-testid="stTable"] th { color:var(--body) !important; background:transparent !important; border-color:var(--line) !important; }
[data-testid="stTable"] th { background:var(--soft) !important; color:var(--ink) !important; }
[data-testid="stSelectbox"] div[data-baseweb="select"] *, [data-testid="stSelectbox"] svg { color:var(--ink) !important; fill:var(--ink) !important; }
[data-testid="stMetricDelta"], [data-testid="stMetricDelta"] * { color:var(--accent2) !important; background:transparent !important; }
[data-testid="stPageLink"] a, [data-testid="stPageLink"] a * { color:var(--ink) !important; }
div.stLinkButton > a, div.stLinkButton > a * { color:var(--ink) !important; }
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a, [data-testid="stSidebarNav"] a * { color:var(--ink) !important; }
[data-testid="stSidebarNav"] a[aria-current="page"] { background:var(--soft) !important; }
[data-testid="stSidebarNavSeparator"], [data-testid="stSidebarNav"] span[data-testid="stNavSectionHeader"] { color:var(--muted) !important; }
[data-testid="stTooltipContent"], [data-baseweb="tooltip"] * { color:var(--ink) !important; }
[data-testid="stImage"] img { background:#fff; border-radius:12px; }
div[data-testid="stTabs"] button { color:var(--muted); }
div[data-testid="stTabs"] button[aria-selected="true"] { color:var(--accent); }
div[data-baseweb="tab-border"] { background:var(--line); }
input, textarea { background:var(--card) !important; color:var(--ink) !important; }
div[data-testid="stTextInput"] input { border-radius:14px; border:1px solid var(--line2); padding:.8rem 1rem; }
div[data-testid="stTextInput"] input:focus { border-color:var(--accent); box-shadow:0 0 0 1px var(--accent); }
div[data-baseweb="select"] > div { background:var(--card); border-color:var(--line2); color:var(--ink); }
div[data-baseweb="popover"] ul, div[data-baseweb="menu"] { background:var(--card) !important; }
div[data-baseweb="popover"] li { color:var(--ink) !important; }
div.stButton > button, div.stLinkButton > a, [data-testid="stPageLink"] a {
    border-radius:999px; border:1px solid var(--line2); background:var(--card); color:var(--ink) !important; }
div.stButton > button:hover, div.stLinkButton > a:hover, [data-testid="stPageLink"] a:hover {
    border-color:var(--accent); color:var(--accent) !important; }
div.stButton > button[kind="primary"] { background:var(--accent); border-color:var(--accent); color:#fff !important; }
img[data-testid="stLogo"] { height:2.7rem; cursor:pointer; }
/* smooth motion: the menu glides open and shut, and each page fades in */
[data-testid="stSidebar"] { transition:transform .55s cubic-bezier(.22,.61,.36,1), margin-left .55s cubic-bezier(.22,.61,.36,1),
    width .55s cubic-bezier(.22,.61,.36,1), min-width .55s cubic-bezier(.22,.61,.36,1), opacity .4s ease !important; }
[data-testid="stSidebarContent"] { transition:opacity .4s ease; }
@keyframes pageIn { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:none; } }
.block-container { animation:pageIn .6s cubic-bezier(.22,.61,.36,1) both; }
div[data-baseweb="popover"], div[data-baseweb="popover"] > div, div[data-baseweb="popover"] ul, ul[role="listbox"],
[data-baseweb="menu"], [data-baseweb="select"] ul { background:var(--card) !important; color:var(--ink) !important; }
li[role="option"], li[role="option"] *, [data-baseweb="menu"] li, [data-baseweb="menu"] li * { color:var(--ink) !important; background:transparent; }
li[role="option"]:hover, li[role="option"][aria-selected="true"], [data-baseweb="menu"] li:hover { background:var(--soft) !important; }
div[data-baseweb="popover"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; box-shadow:0 8px 30px rgba(0,0,0,.25); }
[data-baseweb="select"] input { color:var(--ink) !important; }
[data-baseweb="select"] [data-testid="stSelectboxVirtualDropdown"] , [data-testid="stSelectboxVirtualDropdown"] * { background:var(--card) !important; color:var(--ink) !important; }
.st-key-darkbox { position:absolute; width:1px; height:1px; overflow:hidden; opacity:0; pointer-events:none; }
.stApp, [data-testid="stSidebar"], [data-testid="stHeader"], .step, .stat, .phase, .card, .jn, .pill, .kw, .foot,
[data-testid="stMetric"], [data-testid="stAlert"], [data-testid="stExpander"] details, input, .tli .dot,
.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp li, .stApp td, .stApp th, .section, .hero h1 {
    transition:background-color .7s ease, color .7s ease, border-color .7s ease; }
#MainMenu, footer { visibility:hidden; }

/* ---------- hero, cards, sections ---------- */
.hero { padding:2.2rem 0 1.4rem 0; border-bottom:1px solid var(--line); margin-bottom:1.4rem; }
.hero h1 { color:var(--ink); font-size:3.1rem; font-weight:500; margin:0 0 .3rem 0; letter-spacing:-.02em; }
.hero .tag { font-size:1.05rem; color:var(--accent); margin-bottom:1.1rem; font-weight:500; }
.hero p { font-size:1.08rem; line-height:1.65; max-width:720px; color:var(--body); margin:0; }
.stat { background:var(--soft); border-radius:16px; padding:1.1rem 1.3rem; height:100%; }
.stat .n { font-family:'Source Serif 4',Georgia,serif; font-size:2.1rem; font-weight:500; color:var(--ink); line-height:1.1; }
.stat .l { font-size:.86rem; color:var(--muted); margin-top:.3rem; }
.step { background:var(--card); border:1px solid var(--line); border-radius:16px; padding:1.1rem 1.2rem; min-height:9.5rem; }
.step .k { color:var(--accent); font-weight:600; font-size:.72rem; letter-spacing:.1em; }
.step .t { font-family:'Source Serif 4',Georgia,serif; font-size:1.1rem; font-weight:500; margin:.2rem 0 .3rem 0; color:var(--ink); }
.step .d { font-size:.88rem; color:var(--muted); line-height:1.5; }
.chap { color:var(--accent); font-weight:600; font-size:.8rem; letter-spacing:.18em; margin:1rem 0 -.6rem 0; }
.foot { text-align:center; color:var(--muted); font-size:.85rem; margin:2.5rem 0 1rem 0; padding-top:1rem; border-top:1px solid var(--line); }
.foot a { color:var(--accent); text-decoration:none; }
.section { font-size:1.6rem; font-weight:500; color:var(--ink); margin:2.2rem 0 .3rem 0; }
.cap { color:var(--muted); font-size:.95rem; margin-bottom:.8rem; line-height:1.55; }
.pill { display:inline-block; background:$pill_bg; color:$pill_fg; border-radius:999px; padding:.25rem .85rem;
        margin:.15rem .3rem .15rem 0; font-weight:500; font-size:.9rem; }
.pill.t { background:$pt_bg; color:$pt_fg; }
.card { background:var(--card); border:1px solid var(--line); border-radius:16px; padding:1rem 1.2rem; }

/* ---------- animated journey ---------- */
.journey { display:flex; align-items:center; margin:1rem 0 .4rem 0; }
.jn { background:var(--card); border:1px solid var(--line); border-radius:16px; padding:.9rem 1rem; min-width:128px;
      text-align:center; animation:pulse 6s infinite; }
.jn b { display:block; color:var(--accent); font-size:.72rem; letter-spacing:.12em; }
.jn span { font-family:'Source Serif 4',Georgia,serif; font-size:1.05rem; color:var(--ink); }
.jn small { display:block; color:var(--muted); font-size:.78rem; margin-top:.15rem; }
.jl { flex:1; height:2px; background:var(--line2); position:relative; min-width:24px; }
.jl::after { content:""; position:absolute; top:-4px; left:0; width:10px; height:10px; border-radius:50%;
             background:var(--accent); animation:travel 6s infinite; opacity:0; }
.journey > :nth-child(1) { animation-delay:0s; } .journey > :nth-child(3) { animation-delay:1.5s; }
.journey > :nth-child(5) { animation-delay:3s; } .journey > :nth-child(7) { animation-delay:4.5s; }
.journey > :nth-child(2)::after { animation-delay:.6s; } .journey > :nth-child(4)::after { animation-delay:2.1s; }
.journey > :nth-child(6)::after { animation-delay:3.6s; }
@keyframes travel { 0% { left:0; opacity:1; } 18% { left:calc(100% - 10px); opacity:1; } 22%,100% { left:calc(100% - 10px); opacity:0; } }
@keyframes pulse { 0%,24%,100% { border-color:var(--line); box-shadow:none; } 6%,16% { border-color:var(--accent); box-shadow:0 0 0 4px var(--glow); } }
@keyframes rise { from { opacity:0; transform:translateY(8px) scale(.96); } to { opacity:1; transform:none; } }

/* ---------- keyword chips, timeline ---------- */
.kw { display:inline-block; border-radius:999px; padding:.28rem .8rem; margin:.18rem .22rem; font-size:.88rem; font-weight:500;
      opacity:0; animation:rise .5s ease forwards; border:1px solid transparent; }
.kw.s { background:$pt_bg; color:$pt_fg; } .kw.m { background:$pill_bg; color:$pill_fg; }
.kw.w { background:$weak_bg; color:$weak_fg; } .kw.u { background:transparent; color:var(--muted); border:1px dashed var(--line2); }
.tl { position:relative; margin:.8rem 0 .5rem 1rem; padding-left:1.8rem; border-left:2px solid var(--line2); }
.tli { position:relative; margin-bottom:1.1rem; opacity:0; animation:rise .6s ease forwards; }
.tli .dot { position:absolute; left:-2.95rem; top:.1rem; width:1.9rem; height:1.9rem; border-radius:50%; background:var(--accent);
            color:#fff; font-weight:600; font-size:.85rem; display:flex; align-items:center; justify-content:center;
            box-shadow:0 0 0 5px var(--bg); }
.tli:last-child .dot { background:var(--card); color:var(--accent); border:2px dashed var(--accent); }
.tlb b { font-family:'Source Serif 4',Georgia,serif; font-size:1.1rem; font-weight:500; color:var(--ink); }
.tlb p { margin:.15rem 0 0 0; color:var(--muted); font-size:.93rem; line-height:1.55; }
.legend span { display:inline-block; margin-right:1rem; font-size:.85rem; color:var(--muted); }
.legend i { display:inline-block; width:.8rem; height:.8rem; border-radius:50%; margin-right:.3rem; vertical-align:-1px; }

/* ---------- animated counters, bars ---------- */
@property --n { syntax:'<integer>'; initial-value:0; inherits:false; }
.cnt { animation:count 2.2s ease-out forwards; counter-reset:num var(--n); }
.cnt::after { content:counter(num); }
@keyframes count { to { --n:var(--to); } }
.bar { height:12px; border-radius:999px; background:var(--soft); overflow:hidden; margin:.35rem 0 .9rem 0; }
.bar > i { display:block; height:100%; width:0; background:var(--accent); border-radius:999px; animation:grow 1.6s ease-out forwards; }
.bar.g > i { background:var(--accent2); }
@keyframes grow { to { width:var(--w); } }

/* ---------- about page ---------- */
.avatar { width:150px; height:150px; border-radius:50%; object-fit:cover; border:4px solid var(--card);
          box-shadow:0 0 0 2px var(--accent); }

/* ---------- coming soon ---------- */
.soon-badge { display:inline-block; background:var(--accent); color:#fff; border-radius:999px; padding:.3rem 1rem; font-weight:600;
              letter-spacing:.12em; font-size:.8rem; animation:glow 2.4s infinite; }
@keyframes glow { 0%,100% { box-shadow:0 0 0 0 var(--glow); } 50% { box-shadow:0 0 0 10px transparent; } }
.device { text-align:center; margin:1.2rem 0; }
.ring { transform-origin:center; animation:ring 3s ease-out infinite; opacity:0; }
.ring.r2 { animation-delay:1s; } .ring.r3 { animation-delay:2s; }
@keyframes ring { 0% { transform:scale(.4); opacity:.7; } 100% { transform:scale(1.5); opacity:0; } }
.drift { animation:drift 4s ease-in-out infinite; }
.drift.d2 { animation-delay:1.3s; } .drift.d3 { animation-delay:2.6s; }
@keyframes drift { 0% { transform:translateX(0); opacity:0; } 20% { opacity:1; } 100% { transform:translateX(60px); opacity:0; } }
.phase { background:var(--card); border:1px solid var(--line); border-radius:16px; padding:1rem 1.2rem; height:100%;
         transition:transform .25s ease, border-color .25s ease; }
.phase:hover { transform:translateY(-4px); border-color:var(--accent); }
.phase .k { color:var(--accent); font-weight:600; font-size:.72rem; letter-spacing:.1em; }
.phase .t { font-family:'Source Serif 4',Georgia,serif; font-size:1.1rem; color:var(--ink); margin:.2rem 0; }
.phase .d { font-size:.88rem; color:var(--muted); line-height:1.5; }
.shimmer { height:8px; border-radius:999px; margin-top:.7rem; background:linear-gradient(90deg,var(--soft) 25%,var(--accent) 50%,var(--soft) 75%);
           background-size:200% 100%; animation:shim 2.2s linear infinite; opacity:.7; }
@keyframes shim { from { background-position:200% 0; } to { background-position:-200% 0; } }

/* ---------- responsive: tablet, phone, TV ---------- */
@media (max-width:900px) { .block-container { padding-left:1.2rem; padding-right:1.2rem; } .hero h1 { font-size:2.6rem; } }
@media (max-width:640px) {
  .block-container { padding-top:1.2rem; padding-left:.9rem; padding-right:.9rem; }
  .hero { padding-top:1rem; } .hero h1 { font-size:2.1rem; } .hero p { font-size:1rem; }
  .section { font-size:1.35rem; }
  .journey { flex-direction:column; align-items:stretch; }
  .jn { min-width:0; } .jl { flex:none; width:2px; height:22px; margin:0 auto; }
  .jl::after { left:-4px; top:0; animation:none; opacity:0; }
  .step, .phase { min-height:0; margin-bottom:.4rem; } .stat { margin-bottom:.4rem; }
  .stat .n { font-size:1.7rem; }
  .tl { margin-left:.6rem; padding-left:1.5rem; } .tli .dot { left:-2.6rem; }
  .avatar { width:120px; height:120px; }
}
@media (min-width:1600px) { html { font-size:112%; } .block-container { max-width:1280px; } }
@media (min-width:2200px) { html { font-size:135%; } .block-container { max-width:1600px; } }
@media (min-width:3000px) { html { font-size:170%; } .block-container { max-width:2200px; } }
@media (prefers-reduced-motion:reduce) { * { animation-duration:.01s !important; animation-iteration-count:1 !important; } }
</style>
""")


def inject_css():
    st.markdown(_CSS.safe_substitute(**palette()), unsafe_allow_html=True)


# Graphical day/night switch. This HTML is constant, so Streamlit never re-mounts it and the
# sun-to-moon animation plays smoothly. It clicks a hidden Streamlit toggle (key "dark") in the
# page, reads its state back, sweeps a circular wave across the page, and remembers the choice.
_SWITCH_HTML = """
<style>
html,body{margin:0;background:transparent;overflow:hidden}
#root{height:30px;width:58px}
.sw{position:relative;width:58px;height:30px;border-radius:30px;cursor:pointer;overflow:hidden;border:0;padding:0;outline:none;
    background:linear-gradient(180deg,#7fc0ff,#d6ecff);transition:background .7s ease;box-shadow:inset 0 1px 4px rgba(0,0,0,.2),0 0 0 1px rgba(0,0,0,.06)}
.night .sw{background:linear-gradient(180deg,#080c26,#2a3270)}
.sw:focus-visible{box-shadow:0 0 0 2px #c96442}
.knob{position:absolute;top:4px;left:4px;width:22px;height:22px;border-radius:50%;background:#ffd34d;
      box-shadow:0 0 10px 2px rgba(255,211,77,.6);transition:transform .7s cubic-bezier(.5,-.25,.3,1.35),background .7s,box-shadow .7s}
.night .knob{transform:translateX(28px) rotate(360deg);background:#ecebe4;box-shadow:0 0 8px 1px rgba(205,210,255,.5)}
.crater{position:absolute;border-radius:50%;background:#c9c7bd;opacity:0;transition:opacity .6s .15s}
.night .crater{opacity:1}
.c1{width:5px;height:5px;left:4px;top:5px}.c2{width:3px;height:3px;left:12px;top:12px}.c3{width:3px;height:3px;left:6px;top:14px}
.cloud{position:absolute;background:#fff;border-radius:10px;height:5px;transition:transform .7s ease,opacity .5s;opacity:.95}
.cl1{width:15px;left:27px;top:16px}.cl2{width:11px;left:34px;top:9px}.cl3{width:9px;left:19px;top:5px}
.night .cloud{transform:translateX(-34px);opacity:0}
.star{position:absolute;width:2px;height:2px;border-radius:50%;background:#fff;opacity:0;transition:opacity .6s .2s}
.night .star{opacity:1;animation:tw 2s infinite}
.s1{left:30px;top:6px}.s2{left:42px;top:20px;animation-delay:.6s!important}.s3{left:48px;top:9px;animation-delay:1.1s!important}
@keyframes tw{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.25;transform:scale(.6)}}
</style>
<div id="root" class="night"><button class="sw" id="sw" aria-label="Switch between day and night" title="Day / night">
<span class="star s1"></span><span class="star s2"></span><span class="star s3"></span>
<span class="cloud cl1"></span><span class="cloud cl2"></span><span class="cloud cl3"></span>
<span class="knob"><span class="crater c1"></span><span class="crater c2"></span><span class="crater c3"></span></span>
</button></div>
<script>
const doc = window.parent.document, root = document.getElementById('root'), btn = document.getElementById('sw');
const hidden = () => doc.querySelector('.st-key-darkbox input[type=checkbox]');
const clickHidden = () => { const i = hidden(); if (i) i.click(); };
const paint = (night) => { root.classList.toggle('night', night); };
const store = (night) => { try { window.parent.localStorage.setItem('aroma-theme', night ? 'night' : 'day'); } catch (e) {} };

function sweep(toNight) {                      // circular wave from the switch across the whole page
  const r = btn.getBoundingClientRect(), f = window.frameElement.getBoundingClientRect();
  const x = f.left + r.left + r.width / 2, y = f.top + r.top + r.height / 2;
  const W = window.parent.innerWidth, H = window.parent.innerHeight;
  const radius = Math.hypot(Math.max(x, W - x), Math.max(y, H - y));
  const d = doc.createElement('div');
  d.style.cssText = 'position:fixed;z-index:999999;pointer-events:none;border-radius:50%;left:' + x + 'px;top:' + y + 'px;'
    + 'width:' + radius * 2 + 'px;height:' + radius * 2 + 'px;margin:' + (-radius) + 'px 0 0 ' + (-radius) + 'px;'
    + 'background:' + (toNight ? '#1f1e1d' : '#faf9f5') + ';transform:scale(0);opacity:1;'
    + 'transition:transform .75s cubic-bezier(.4,0,.2,1),opacity .6s ease';
  doc.body.appendChild(d);
  requestAnimationFrame(() => requestAnimationFrame(() => { d.style.transform = 'scale(1)'; }));
  setTimeout(() => { d.style.opacity = '0'; }, 1100);
  setTimeout(() => d.remove(), 1800);
}

let pending = null;                            // a change we asked for but Streamlit has not applied yet
btn.addEventListener('click', () => {
  const h = hidden(); const toNight = !(h && h.checked);
  pending = {night: toNight, t: Date.now()};
  paint(toNight); store(toNight); sweep(toNight); setTimeout(clickHidden, 450);
});

let restored = false;
setInterval(() => {                            // keep in sync with the real state
  const h = hidden(); if (!h) return;
  if (!restored) {
    restored = true;
    let saved = null; try { saved = window.parent.localStorage.getItem('aroma-theme'); } catch (e) {}
    if (saved && (saved === 'night') !== h.checked) { paint(saved === 'night'); clickHidden(); return; }
  }
  if (pending) {
    if (h.checked === pending.night || Date.now() - pending.t > 4000) pending = null; else return;
  }
  if (root.classList.contains('night') !== h.checked) paint(h.checked);
}, 250);
</script>
"""


def theme_switch():
    """Small sun/moon switch fixed in the header (top right). Needs `hidden_theme_toggle()`."""
    with st.container(key="themesw"):
        st.components.v1.html(_SWITCH_HTML, height=30)


def hidden_theme_toggle():
    """The real (invisible) Streamlit toggle that stores the dark-mode state."""
    with st.container(key="darkbox"):
        st.toggle("Dark mode", key="dark")


def chart(c, container=None, **kw):
    """Show an Altair chart with colours that match the current light/dark mode."""
    p = palette()
    c = (c.configure(background="rgba(0,0,0,0)")
         .configure_axis(labelColor=p["muted"], titleColor=p["ink"], gridColor=p["line"],
                         domainColor=p["line2"], tickColor=p["line2"], labelFontSize=11, titleFontSize=12)
         .configure_title(color=p["ink"], fontSize=14, anchor="start")
         .configure_legend(labelColor=p["muted"], titleColor=p["ink"])
         .configure_view(stroke=None))
    (container or st).altair_chart(c, width="stretch", theme=None, **kw)


def footer():
    links = []
    if cfg.GITHUB_URL:
        links.append(f'<a href="{cfg.GITHUB_URL}" target="_blank">GitHub</a>')
    if cfg.LINKEDIN_URL:
        links.append(f'<a href="{cfg.LINKEDIN_URL}" target="_blank">LinkedIn</a>')
    link_html = " &nbsp;|&nbsp; ".join(links)
    st.markdown(
        f'<div class="foot">&copy; {cfg.YEAR} {cfg.AUTHOR}. All rights reserved. '
        f'Created by {cfg.AUTHOR}.{(" &nbsp;|&nbsp; " + link_html) if link_html else ""}</div>',
        unsafe_allow_html=True)
