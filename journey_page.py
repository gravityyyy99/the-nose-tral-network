"""Our journey: how the project was made, step by step, with graphics, in motion."""
import json
import os

import altair as alt
import joblib
import numpy as np
import pandas as pd
import streamlit as st

import sensor
import ui
from train_nose import PROFILE_PATH

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = []        # documentation pages, set by app.py so we can link to them

TIERS = {"s": "Nose finds it easily (70% or more)", "m": "Nose finds it sometimes (30 to 69%)",
         "w": "Nose rarely finds it (under 30%)"}
COLORS = {"s": "#788c5d", "m": "#c96442", "w": "#a8a69b"}


def _tier(v):
    return "s" if v >= 0.7 else "m" if v >= 0.3 else "w"


@st.cache_data
def _fingerprints():
    """Average sensor reading of each curated smell, plus 30 noisy sniffs of coffee."""
    rng = np.random.default_rng(5)
    rows, coffee = [], None
    for name, info in sensor.load_samples().items():
        smiles = list(info["molecules"].values())
        reads = np.array([sensor.sniff(smiles, rng) for _ in range(60)])
        pct = sensor.to_percent(reads)
        for j, ch in enumerate(sensor.CHANNELS):
            rows.append({"Smell": name, "Sensor": ch, "Reaction (%)": float(pct[:, j].mean())})
        if name == "coffee":
            coffee = pct[:30]
    noisy = [{"Sniff": i, "Sensor": ch, "Reaction (%)": float(coffee[i, j])}
             for i in range(len(coffee)) for j, ch in enumerate(sensor.CHANNELS)]
    return pd.DataFrame(rows), pd.DataFrame(noisy)


def _bar(label, value_text, width, cls=""):
    return (f'<div style="display:flex;justify-content:space-between"><b>{label}</b><span>{value_text}</span></div>'
            f'<div class="bar {cls}"><i style="--w:{width}%"></i></div>')


def run():
    ev_path = os.path.join(HERE, "evaluation.json")
    ev = json.load(open(ev_path)) if os.path.exists(ev_path) else {}
    nose_acc = ev.get("nose_top5_per_word", {})
    auc = ev.get("smell_model_auc_per_word", {})
    labels = joblib.load(PROFILE_PATH)["labels"]

    st.markdown('<div class="chap">THE WHOLE STORY</div>', unsafe_allow_html=True)
    st.title("Our journey")
    st.markdown("How The Nose-tral Network was made, from the first idea to what you are using now. "
                "Everything here is in motion: the path a smell takes, the numbers behind it, the steps we "
                "followed, the keywords we trained on, and how each part performed.")

    # ------------------------------------------------------------ 1. path
    st.markdown('<div class="section">1. The path of a smell</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="journey">'
        '<div class="jn"><b>STEP 1</b><span>Keyword</span><small>you type a smell</small></div><div class="jl"></div>'
        '<div class="jn"><b>STEP 2</b><span>Molecules</span><small>real aroma chemicals</small></div><div class="jl"></div>'
        '<div class="jn"><b>STEP 3</b><span>Sensors</span><small>8 gas sensors react</small></div><div class="jl"></div>'
        '<div class="jn"><b>STEP 4</b><span>Two AIs</span><small>nose model and smell model</small></div>'
        '</div>', unsafe_allow_html=True)
    st.caption("Every keyword travels along this path, from a word to chemistry to sensor readings to a guess.")

    # ------------------------------------------------------------ 2. numbers
    st.markdown('<div class="section">2. The project in numbers</div>', unsafe_allow_html=True)
    nums = [("4983", "molecules labelled by experts"), ("138", "smell words learned"),
            ("8", "simulated gas sensors"), ("6000", "simulated sniffs used to train the nose")]
    for col, (n, label) in zip(st.columns(4), nums):
        col.markdown(f'<div class="stat"><div class="n cnt" style="--to:{n}"></div><div class="l">{label}</div></div>',
                     unsafe_allow_html=True)

    # ------------------------------------------------------------ 3. roadmap
    st.markdown('<div class="section">3. The roadmap we followed</div>', unsafe_allow_html=True)
    auc_all = f"{ev['smell_model_mean_auc']:.2f}" if ev else "n/a"
    steps = [
        ("The idea", "Computers cannot smell, but smell is chemistry. Follow the Google, Osmo and Monell research "
                     "at laptop scale, and pair it with an electronic nose."),
        ("Get the data", "Downloaded the OpenPOM dataset: 4,983 molecules labelled by experts with 138 smell words."),
        ("Build the smell model", f"Turned each molecule into a 2,048-number fingerprint and trained a random forest. "
                                  f"Result: {auc_all} ROC-AUC on unseen molecules."),
        ("Simulate an electronic nose", "Created 8 virtual gas sensors, each tuned to a property such as size, "
                                        "sulfur or aromatic rings, with noise, humidity and drift."),
        ("Train the six-smell nose", "Sniffed six everyday smells 200 times each and trained a classifier. "
                                     "Result: about 98% on held-back sniffs in the last training run (it varies a little each run)."),
        ("Teach the nose any smell", "Trained on 6,000 sniffs of mixtures built from all 138 words, "
                                     "so it can describe any smell you type."),
        ("Make it typeable", "Added free-text input with spelling correction, so a typo like lavendar still works."),
        ("Measure every keyword", "Tested each of the 138 words separately, and recorded where the models "
                                  "succeed and where they fail."),
        ("Build the interface and the book", "Made this app, the documentation chapters and the keyword pages."),
        ("Next: real devices", "Replace the simulated nose with real smelling hardware, test it, and update this project."),
    ]
    html = ['<div class="tl">']
    for n, (t, d) in enumerate(steps, 1):
        html.append(f'<div class="tli" style="animation-delay:{n * 0.25:.2f}s"><div class="dot">{n}</div>'
                    f'<div class="tlb"><b>{t}</b><p>{d}</p></div></div>')
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)

    # ------------------------------------------------------------ 4. data split
    st.markdown('<div class="section">4. How the data was used</div>', unsafe_allow_html=True)
    st.markdown('<div class="cap">Models are tested only on examples they never saw while learning. '
                'Each bar shows the share kept for learning and the share held back for testing.</div>',
                unsafe_allow_html=True)
    a, b = st.columns(2)
    a.markdown("**Smell model** (4,983 molecules)" + _bar("Learning", "3,986 molecules, 80%", 80)
               + _bar("Testing (never seen)", "997 molecules, 20%", 20, "g"), unsafe_allow_html=True)
    b.markdown("**Nose model** (6,000 sniffs)" + _bar("Learning", "4,800 sniffs, 80%", 80)
               + _bar("Testing (never seen)", "1,200 sniffs, 20%", 20, "g"), unsafe_allow_html=True)

    # ------------------------------------------------------------ 5. keyword map
    st.markdown('<div class="section">5. The keywords we trained on</div>', unsafe_allow_html=True)
    st.markdown('<div class="cap">All 138 smell words. The colour shows how often the electronic nose finds that '
                'word among its top 5 guesses in testing. Hover a word for exact numbers.</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="legend">' + "".join(
        f'<span><i style="background:{COLORS[k]}"></i>{v}</span>' for k, v in TIERS.items()) + "</div>",
        unsafe_allow_html=True)
    chips = []
    for n, w in enumerate(labels):
        v = nose_acc.get(w)
        delay = f"animation-delay:{min(n * 0.02, 1.5):.2f}s"
        if v is None:
            chips.append(f'<span class="kw u" style="{delay}">{w}</span>')
            continue
        tip = f"{w}: nose finds it {v:.0%} of the time" + (f", smell model accuracy {auc[w]:.2f}" if w in auc else "")
        chips.append(f'<span class="kw {_tier(v)}" title="{tip}" style="{delay}">{w}</span>')
    st.markdown("".join(chips), unsafe_allow_html=True)

    # ------------------------------------------------------------ 6. sensor fingerprints
    st.markdown('<div class="section">6. Every smell leaves a fingerprint</div>', unsafe_allow_html=True)
    st.markdown('<div class="cap">Each row is one of the six everyday smells, each column one of the 8 sensors. '
                'Darker means a stronger reaction. The pattern across the row is the smell\'s fingerprint, '
                'and it is what the nose model learns to recognise.</div>', unsafe_allow_html=True)
    fp, noisy = _fingerprints()
    heat = alt.Chart(fp).mark_rect(cornerRadius=4).encode(
        x=alt.X("Sensor:N", sort=sensor.CHANNELS, title=None, axis=alt.Axis(labelAngle=-30)),
        y=alt.Y("Smell:N", title=None),
        color=alt.Color("Reaction (%):Q", scale=alt.Scale(range=["#f4e3da", "#c96442", "#7a2e14"]),
                        legend=alt.Legend(title="Reaction")),
        tooltip=["Smell", "Sensor", alt.Tooltip("Reaction (%):Q", format=".0f")],
    ).properties(height=260)
    ui.chart(heat)

    st.markdown('<div class="cap">The same fingerprints as lines. Where the lines separate, the nose can tell the '
                'smells apart. Where they overlap, it gets confused.</div>', unsafe_allow_html=True)
    lines = alt.Chart(fp).mark_line(point=True, strokeWidth=2.5).encode(
        x=alt.X("Sensor:N", sort=sensor.CHANNELS, title=None, axis=alt.Axis(labelAngle=-30)),
        y=alt.Y("Reaction (%):Q", scale=alt.Scale(zero=False)),
        color=alt.Color("Smell:N", scale=alt.Scale(range=["#c96442", "#788c5d", "#6c8ebf", "#d4a24c", "#9b6b9e", "#7a7a73"])),
        tooltip=["Smell", "Sensor", alt.Tooltip("Reaction (%):Q", format=".0f")],
    ).properties(height=320)
    ui.chart(lines)

    st.markdown('<div class="cap">Real sensors are noisy. Here are 30 separate sniffs of the same coffee. '
                'The faint lines are individual sniffs, the bold line is their average. '
                'The nose has to see through this mess.</div>', unsafe_allow_html=True)
    mean_line = noisy.groupby("Sensor", as_index=False)["Reaction (%)"].mean()
    faint = alt.Chart(noisy).mark_line(opacity=.25, color="#c96442").encode(
        x=alt.X("Sensor:N", sort=sensor.CHANNELS, title=None, axis=alt.Axis(labelAngle=-30)),
        y=alt.Y("Reaction (%):Q", scale=alt.Scale(zero=False)), detail="Sniff:N")
    bold = alt.Chart(mean_line).mark_line(strokeWidth=4, color="#c96442", point=True).encode(
        x=alt.X("Sensor:N", sort=sensor.CHANNELS), y="Reaction (%):Q")
    ui.chart((faint + bold).properties(height=300))

    # ------------------------------------------------------------ 7. performance
    st.markdown('<div class="section">7. How every keyword performed</div>', unsafe_allow_html=True)
    if nose_acc and auc:
        st.markdown('<div class="cap">Each dot is one smell word. Left to right: how well the smell model understands '
                    'the molecules. Bottom to top: how well the electronic nose finds the word from sensor readings alone. '
                    'Words in the top right are easy for both.</div>', unsafe_allow_html=True)
        rows = [{"word": w, "Smell model accuracy (AUC)": auc[w], "Nose top-5 hit rate": nose_acc[w],
                 "tier": TIERS[_tier(nose_acc[w])]} for w in nose_acc if w in auc]
        df = pd.DataFrame(rows)
        ui.chart(alt.Chart(df).mark_circle(size=90, opacity=.85).encode(
            x=alt.X("Smell model accuracy (AUC):Q", scale=alt.Scale(domain=[0.4, 1.0])),
            y=alt.Y("Nose top-5 hit rate:Q", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 1.02])),
            color=alt.Color("tier:N", legend=None, scale=alt.Scale(
                domain=[TIERS[k] for k in "smw"], range=[COLORS[k] for k in "smw"])),
            tooltip=["word", alt.Tooltip("Smell model accuracy (AUC):Q", format=".2f"),
                     alt.Tooltip("Nose top-5 hit rate:Q", format=".0%")],
        ).properties(height=380))

        c1, c2, c3 = st.columns(3)
        c1.metric("Smell model accuracy", f"{ev['smell_model_mean_auc']:.2f} AUC", help="0.5 is guessing, 1.0 is perfect")
        c2.metric("Nose: right word in top 5", f"{ev['nose_top5']:.0%}", f"vs {ev['chance_top5']:.0%} by chance")
        c3.metric("Nose: best guess correct", f"{ev['nose_top1']:.0%}", f"vs {ev['chance_top1']:.1%} by chance")

        st.markdown('<div class="cap">The ten smells the nose finds best, and the ten it finds hardest.</div>',
                    unsafe_allow_html=True)
        s = sorted(nose_acc, key=lambda w: (-nose_acc[w], w))
        best = pd.DataFrame({"Smell word": s[:10], "Hit rate": [nose_acc[w] for w in s[:10]]})
        worst = pd.DataFrame({"Smell word": s[-10:][::-1], "Hit rate": [nose_acc[w] for w in s[-10:][::-1]]})
        l, r = st.columns(2)
        for col, d, colr, title in ((l, best, ui.TEAL, "Easiest for the nose"), (r, worst, ui.BLUE, "Hardest for the nose")):
            ui.chart(alt.Chart(d).mark_bar(color=colr, cornerRadiusEnd=4).encode(
                y=alt.Y("Smell word:N", sort=list(d["Smell word"]), title=None),
                x=alt.X("Hit rate:Q", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 1])),
                tooltip=["Smell word", alt.Tooltip("Hit rate:Q", format=".0%")],
            ).properties(height=280, title=title), col)

        top5 = pd.DataFrame({"word": list(nose_acc), "hit": list(nose_acc.values())})
        ui.chart(alt.Chart(top5).mark_bar(color=ui.BLUE, cornerRadiusEnd=3).encode(
            x=alt.X("hit:Q", bin=alt.Bin(step=0.1), title="How often the nose finds the word in its top 5"),
            y=alt.Y("count()", title="Number of smell words"),
        ).properties(height=240, title="Electronic nose: how many words are found how often"))
        st.caption("The nose is simulated for now, so a real sensor would score lower. "
                   "A version built with real smelling devices is planned.")
    else:
        st.info("Run `python evaluate.py` to generate the performance graphs.")

    # ------------------------------------------------------------ 8. read the story
    st.markdown('<div class="section">8. Read the full story</div>', unsafe_allow_html=True)
    st.markdown("Every step above is explained in detail in the documentation. Pick a chapter to jump straight in.")
    if BOOK:
        st.page_link(BOOK[0], label="Open the documentation contents")
        cols = st.columns(2)
        for i, page in enumerate(BOOK[1:]):
            cols[i % 2].page_link(page)
    ui.footer()
