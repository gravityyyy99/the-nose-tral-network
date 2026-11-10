"""Builds the documentation 'book': one Streamlit page per chapter (markdown in docs_content/)."""
import json
import os

import altair as alt
import pandas as pd
import streamlit as st

import ui

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "docs_content")

# (file, sidebar title, url slug)
CONTENTS = ("00_contents.md", "Contents", "contents")
CHAPTERS = [
    ("01_plain_words.md", "In plain words", "plain-words"),
    ("02_big_idea.md", "How smell works", "how-smell-works"),
    ("03_data.md", "The data", "the-data"),
    ("04_smell_model.md", "The smell model", "smell-model"),
    ("05_electronic_nose.md", "The electronic nose", "electronic-nose"),
    ("06_training_nose.md", "Training the nose", "training-the-nose"),
    ("07_app.md", "The app", "the-app"),
    ("08_results.md", "Results and limits", "results"),
    ("09_credits.md", "Credits", "credits"),
    ("10_plans.md", "Future plans", "future-plans"),
    ("11_coming_soon.md", "Coming soon", "coming-soon"),
]
# every page in book order: contents first, then chapters
BOOK = [CONTENTS] + CHAPTERS


def label(i):
    """Sidebar/link label for BOOK[i]: 'Contents' or 'Chapter 3: The data'."""
    return BOOK[i][1] if i == 0 else f"Chapter {i}: {BOOK[i][1]}"

_pages = []


def _evaluation():
    p = os.path.join(HERE, "evaluation.json")
    return json.load(open(p)) if os.path.exists(p) else None


def _fill(text):
    ev = _evaluation()
    if ev:
        vals = {
            "auc": f"{ev['smell_model_mean_auc']:.2f}",
            "top1": f"{ev['nose_top1']:.0%}",
            "top5": f"{ev['nose_top5']:.0%}",
            "c1": f"{ev['chance_top1']:.1%}",
            "c5": f"{ev['chance_top5']:.1%}",
        }
    else:
        vals = {k: "n/a (run evaluate.py)" for k in ("auc", "top1", "top5", "c1", "c5")}
    for k, v in vals.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def _results_charts():
    ev = _evaluation()
    if not ev:
        return
    st.markdown("#### Accuracy for every smell word")
    st.caption("Each bar is one smell word. Longer bars mean the model handles that word better. "
               "Hover for the exact value.")
    auc = pd.DataFrame({"word": list(ev["smell_model_auc_per_word"]),
                        "AUC": list(ev["smell_model_auc_per_word"].values())})
    ui.chart(
        alt.Chart(auc).mark_bar(color=ui.TEAL).encode(
            x=alt.X("AUC:Q", bin=alt.Bin(step=0.05), title="Smell model accuracy (ROC-AUC)"),
            y=alt.Y("count()", title="Number of smell words"),
        ).properties(height=260, title="Smell model: how many words are handled how well"))
    top5 = pd.DataFrame({"word": list(ev["nose_top5_per_word"]),
                         "hit": list(ev["nose_top5_per_word"].values())})
    ui.chart(
        alt.Chart(top5).mark_bar(color=ui.BLUE).encode(
            x=alt.X("hit:Q", bin=alt.Bin(step=0.1), title="How often the nose finds the word in its top 5"),
            y=alt.Y("count()", title="Number of smell words"),
        ).properties(height=260, title="Electronic nose: how many words are found how often"))
    st.caption("Reading the nose chart: the pile at the far left are smells the nose almost never gets; "
               "the pile at the far right are smells it nearly always gets.")


def _coming_soon_visual():
    """Animated 'building' scene for the Coming soon chapter (single-line HTML so Markdown keeps it as HTML)."""
    svg = (
        '<svg viewBox="0 0 520 170" width="100%" style="max-width:560px" xmlns="http://www.w3.org/2000/svg">'
        '<g fill="#788c5d"><circle class="drift" cx="40" cy="60" r="5"/><circle class="drift d2" cx="30" cy="95" r="4"/>'
        '<circle class="drift d3" cx="45" cy="125" r="4.5"/></g>'
        '<g fill="none" stroke="#c96442" stroke-width="2"><circle class="ring" cx="300" cy="85" r="62"/>'
        '<circle class="ring r2" cx="300" cy="85" r="62"/><circle class="ring r3" cx="300" cy="85" r="62"/></g>'
        '<rect x="250" y="55" width="100" height="60" rx="10" fill="#c96442"/>'
        '<g stroke="#c96442" stroke-width="3" stroke-linecap="round">'
        '<line x1="265" y1="45" x2="265" y2="55"/><line x1="285" y1="45" x2="285" y2="55"/><line x1="305" y1="45" x2="305" y2="55"/>'
        '<line x1="325" y1="45" x2="325" y2="55"/><line x1="265" y1="115" x2="265" y2="125"/><line x1="285" y1="115" x2="285" y2="125"/>'
        '<line x1="305" y1="115" x2="305" y2="125"/><line x1="325" y1="115" x2="325" y2="125"/></g>'
        '<text x="300" y="91" text-anchor="middle" font-family="Georgia,serif" font-size="17" fill="#faf9f5">BME688</text>'
        '<rect x="395" y="68" width="85" height="34" rx="7" fill="none" stroke="#a3a198" stroke-width="2" stroke-dasharray="5 4"/>'
        '<text x="437" y="90" text-anchor="middle" font-family="Georgia,serif" font-size="14" fill="#a3a198">ESP32</text>'
        '<line x1="350" y1="85" x2="395" y2="85" stroke="#a3a198" stroke-width="2" stroke-dasharray="4 4"/></svg>')
    st.markdown(f'<div class="device"><span class="soon-badge">COMING SOON</span><br>{svg}</div>',
                unsafe_allow_html=True)


def _coming_soon_phases():
    phases = [
        ("PHASE 1", "Build the hardware", "Connect a real gas sensor to a small microcontroller and stream readings to a laptop."),
        ("PHASE 2", "Smell real things", "Record real smells in jars across several days, with clean air in between."),
        ("PHASE 3", "Retrain the nose", "Swap the simulated readings for the real ones and train the same model again."),
        ("PHASE 4", "Test and publish", "Test on sessions the model has never seen, then share every result, good or bad."),
    ]
    for col, (k, t, d) in zip(st.columns(4), phases):
        col.markdown(f'<div class="phase"><div class="k">{k}</div><div class="t">{t}</div>'
                     f'<div class="d">{d}</div><div class="shimmer"></div></div>', unsafe_allow_html=True)
    st.caption("All four phases are planned. The bars shimmer because the work is still ahead.")
    import site_config as cfg
    st.link_button("Follow the project on GitHub for updates", cfg.GITHUB_URL)


EXTRAS = {"08_results.md": _results_charts, "11_coming_soon.md": _coming_soon_phases}
PRE = {"11_coming_soon.md": _coming_soon_visual}


def _make(i):
    fname = BOOK[i][0]

    def page():
        if i > 0:
            st.markdown(f'<div class="chap">CHAPTER {i}</div>', unsafe_allow_html=True)
        with open(os.path.join(CONTENT, fname), encoding="utf-8") as f:
            text = _fill(f.read())
        if fname in PRE:   # motion/visual first, then the words
            head, _, rest = text.partition("\n")
            st.markdown(head)
            PRE[fname]()
            st.markdown(rest)
        else:
            st.markdown(text)
        if i == 0:   # the contents list, with a link to each chapter
            for j in range(1, len(BOOK)):
                st.page_link(_pages[j], label=label(j))
        if fname in EXTRAS:
            EXTRAS[fname]()
        st.divider()
        left, right = st.columns(2)
        if i > 0:
            left.page_link(_pages[i - 1], label=f"Previous: {label(i - 1)}")
        if i < len(BOOK) - 1:
            right.page_link(_pages[i + 1], label=f"Next: {label(i + 1)}")
        ui.footer()

    page.__name__ = f"chapter_{i}"
    return page


def build():
    _pages.clear()
    for i, (_, _, slug) in enumerate(BOOK):
        _pages.append(st.Page(_make(i), title=label(i), url_path=slug))
    return list(_pages)
