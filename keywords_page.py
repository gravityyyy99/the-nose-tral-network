"""Smell keywords: the words the models were trained on, which you can test."""
import joblib
import streamlit as st

import sensor
import ui
from train_nose import PROFILE_PATH

SNIFF = None   # set by app.py so a keyword can open the Sniff page


def run():
    st.markdown('<div class="chap">KEYWORDS</div>', unsafe_allow_html=True)
    st.title("Smell keywords")
    labels = joblib.load(PROFILE_PATH)["labels"]
    samples = list(sensor.load_samples())
    st.markdown(f"These are the **{len(labels)} smell words** the models were trained on. "
                "Type any of them on the Sniff page, or pick one below.")

    q = st.text_input("Filter", placeholder="Filter keywords, e.g. fruit", label_visibility="collapsed")
    words = [w for w in labels if q.strip().lower() in w.lower()]
    chips = "".join(
        f'<span class="kw u" style="animation-delay:{min(n * 0.015, 1.2):.2f}s;border-style:solid">{w}</span>'
        for n, w in enumerate(words))
    st.markdown(chips or "No keyword matches that.", unsafe_allow_html=True)
    st.caption(f"{len(words)} shown.")

    st.markdown('<div class="section">Everyday smells</div>', unsafe_allow_html=True)
    st.markdown('<div class="cap">Six hand-written smells, each made from its real aroma molecules.</div>',
                unsafe_allow_html=True)
    st.markdown("".join(f'<span class="kw u" style="animation-delay:.1s;border-style:solid">{s}</span>'
                        for s in samples), unsafe_allow_html=True)

    st.markdown('<div class="section">Try one</div>', unsafe_allow_html=True)
    choice = st.selectbox("Pick a keyword", sorted(set(labels) | set(samples)), index=None,
                          placeholder="Choose a smell word", label_visibility="collapsed")
    if st.button("Sniff this keyword", type="primary", disabled=choice is None) and choice:
        st.session_state.query = choice
        st.switch_page(SNIFF)
    st.caption("Want to see how well each word works? Open **Our journey** in the menu.")

    ui.footer()
