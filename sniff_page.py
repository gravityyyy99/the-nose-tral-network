"""The Sniff page: type a smell, watch the pipeline run."""
import json
import os

import altair as alt
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw

import sensor
import smell_model
import smell_query
import ui
from train_nose import PROFILE_PATH

HERE = os.path.dirname(os.path.abspath(__file__))
BLUE, TEAL = ui.BLUE, ui.TEAL
EXAMPLES = ["coffee", "vanilla", "fruity", "smoky", "banana", "woody", "citrus", "floral"]


def run():
    # ------------------------------------------------------------------ guard + data
    if not (os.path.exists(PROFILE_PATH) and os.path.exists(smell_model.MODEL_PATH)):
        st.error("Models not trained yet. Run `python smell_model.py` then `python train_nose.py`.")
        return

    nose = joblib.load(PROFILE_PATH)
    labels = nose["labels"]
    ev_path = os.path.join(HERE, "evaluation.json")
    ev = json.load(open(ev_path)) if os.path.exists(ev_path) else None

    # ------------------------------------------------------------------ hero
    st.markdown(
        '<div class="hero"><h1>Aroma-GPT</h1>'
        '<div class="tag">The Nose-tral Network: a project that teaches an AI to smell</div>'
        "<p>Smell is chemistry: every scent is a set of molecules. Aroma-GPT combines a "
        "<b>smell model</b> that reads a molecule's structure and describes it in words with an "
        "<b>electronic nose</b>, a simulated array of gas sensors, and a second model that "
        "recognises smells from the sensor readings alone. Type a smell and watch both work.</p>"
        "</div>", unsafe_allow_html=True)

    st.caption("The electronic nose is simulated for now. A version built with real smelling "
               "devices is planned, and this project will be updated as it is tested.")

    stats = [
        (f"{ev['smell_model_mean_auc']:.2f}" if ev else "n/a", "Smell model accuracy (ROC-AUC, 0.5 = guessing)"),
        ("138", "smell words understood"),
        ("4,983", "expert-labelled molecules"),
        ("8", "simulated gas sensors"),
    ]
    for col, (n, l) in zip(st.columns(4), stats):
        col.markdown(f'<div class="stat"><div class="n">{n}</div><div class="l">{l}</div></div>',
                     unsafe_allow_html=True)

    st.markdown('<div class="section">How it works</div>', unsafe_allow_html=True)
    steps = [
        ("STEP 1", "You name a smell", "Typos are corrected automatically."),
        ("STEP 2", "Real molecules", "We pick real aroma molecules that carry that smell."),
        ("STEP 3", "Sensors react", "8 gas sensors respond, with noise and humidity like real hardware."),
        ("STEP 4", "Two AIs describe it", "One reads the sensors, one reads the molecule structures."),
    ]
    for col, (k, t, d) in zip(st.columns(4), steps):
        col.markdown(f'<div class="step"><div class="k">{k}</div><div class="t">{t}</div>'
                     f'<div class="d">{d}</div></div>', unsafe_allow_html=True)

    # ------------------------------------------------------------------ input
    st.markdown('<div class="section">Try it</div>', unsafe_allow_html=True)
    st.session_state.setdefault("query", "")


    def pick(word):
        st.session_state.query = word


    st.text_input("What smell do you want to sniff?", key="query",
                  placeholder="Type any smell, e.g. coffee, fruity, smoky. Several: coffee, smoky")
    st.caption("Press Enter to sniff. Press it again for a fresh sniff: the sensors are noisy, so every sniff differs slightly.")
    ex_cols = st.columns(len(EXAMPLES))
    for col, w in zip(ex_cols, EXAMPLES):
        col.button(w, key=f"ex_{w}", on_click=pick, args=(w,), width="stretch")

    text = st.session_state.query
    if not text.strip():
        st.info("Pick an example above or type your own smell to begin.")
        with st.expander("See all 138 smell words"):
            st.write(", ".join(smell_query.vocabulary()))
        return

    # ------------------------------------------------------------------ spelling
    words = []
    for r in smell_query.resolve(text):
        if r["status"] == "ok":
            words.append(r["word"])
        elif r["status"] == "corrected":
            st.warning(f"Spelling: \"{r['original'].strip()}\" is not a smell I know. "
                       f"Autocorrected to **{r['word']}**.")
            words.append(r["word"])
        else:
            msg = f"\"{r['original'].strip()}\" is not a smell I know."
            if r["suggestions"]:
                msg += " Did you mean: " + ", ".join(f"**{s}**" for s in r["suggestions"]) + "?"
            st.error(msg)
    if not words:
        return

    # ------------------------------------------------------------------ pipeline
    rng = np.random.default_rng()
    smiles = sorted({s for w in words for s in smell_query.molecules_for(w, rng)})
    reading = sensor.sniff(smiles, rng)
    strength = sensor.to_percent(reading)
    scores = nose["reg"].predict(reading.reshape(1, -1))[0]
    order = np.argsort(scores)[::-1]
    nose_top = [labels[i] for i in order[:5]]
    model_scores = smell_model.predict_proba(smiles)
    model_top = sorted(model_scores, key=model_scores.get, reverse=True)[:8]

    st.markdown(f'<div class="section">Results for: {" + ".join(words)}</div>', unsafe_allow_html=True)

    # verdict
    asked = [w for w in words if w in nose_top]
    agree = [w for w in nose_top if w in model_top]
    if asked:
        st.success(f"The nose recognised **{', '.join(asked)}** from the sensor readings alone.")
    elif agree:
        st.info(f"The nose did not name {', '.join(words)} directly, but agrees with the smell model on: "
                f"**{', '.join(agree)}**.")
    else:
        st.info("The nose is unsure about this one. With only 8 sensors, similar smells blur together.")

    tab1, tab2, tab3, tab4 = st.tabs(["Verdict", "Molecules", "Sensors", "Accuracy"])

    with tab1:
        a, b = st.columns(2)
        a.markdown("**Nose model says** (from the 8 sensor readings only)")
        a.markdown("".join(f'<span class="pill">{w}</span>' for w in nose_top), unsafe_allow_html=True)
        b.markdown("**Smell model says** (from the molecule structures)")
        b.markdown("".join(f'<span class="pill t">{w}</span>' for w in model_top[:5]), unsafe_allow_html=True)

        def word_chart(names, values, color, title):
            df = pd.DataFrame({"Smell word": names, "Confidence": values})
            return alt.Chart(df).mark_bar(color=color, cornerRadiusEnd=4).encode(
                y=alt.Y("Smell word:N", sort=names, title=None),
                x=alt.X("Confidence:Q", title="Confidence"),
                tooltip=["Smell word", alt.Tooltip("Confidence:Q", format=".2f")],
            ).properties(height=270, title=title)

        top8 = order[:8]
        ui.chart(word_chart([labels[i] for i in top8], [float(scores[i]) for i in top8],
                            BLUE, "Nose model"), a)
        ui.chart(word_chart(model_top, [float(model_scores[w]) for w in model_top],
                            TEAL, "Smell model"), b)

    with tab2:
        st.markdown(f'<div class="cap">A smell is a mixture of molecules in the air. These {len(smiles)} '
                    'real aroma molecules are drawn as chemical structures: lines are bonds, letters are atoms.</div>',
                    unsafe_allow_html=True)
        mols = [Chem.MolFromSmiles(s) for s in smiles]
        st.image(Draw.MolsToGridImage(mols, molsPerRow=min(4, len(mols)), subImgSize=(230, 180)))

    with tab3:
        st.markdown('<div class="cap">The nose has 8 gas sensors, each sensitive to a different kind of molecule. '
                    'Together they form a fingerprint of the smell. A longer bar means a stronger reaction. '
                    'Hover a bar to see what that sensor reacts to.</div>', unsafe_allow_html=True)
        sdf = pd.DataFrame({"Sensor": sensor.CHANNELS, "Reaction strength (%)": strength,
                            "Reacts to": [d for _, d in sensor.CHANNEL_INFO]})
        ui.chart(alt.Chart(sdf).mark_bar(color=BLUE, cornerRadiusEnd=4).encode(
            y=alt.Y("Sensor:N", sort=sensor.CHANNELS, title=None),
            x=alt.X("Reaction strength (%):Q", scale=alt.Scale(domain=[0, 100]),
                    title="Reaction strength (0 = none, 100 = maximum)"),
            tooltip=["Sensor", "Reacts to", alt.Tooltip("Reaction strength (%):Q", format=".0f")],
        ).properties(height=320))
        st.table(sdf[["Sensor", "Reacts to"]].set_index("Sensor"))

    with tab4:
        st.markdown('<div class="cap">How trustworthy is this? The first two columns were measured on test data the '
                    'models never trained on. The last two come from the sniff you just ran, so they change every time.</div>',
                    unsafe_allow_html=True)
        lab_index = {w: i for i, w in enumerate(labels)}
        rank_of = {int(i): r + 1 for r, i in enumerate(order)}
        rows, ranks, aucs, hits = [], [], [], []
        for w in words:
            hit = ev.get("nose_top5_per_word", {}).get(w) if ev else None
            auc_w = ev.get("smell_model_auc_per_word", {}).get(w) if ev else None
            rk = rank_of.get(lab_index[w]) if w in lab_index else None
            if hit is not None: hits.append(hit)
            if auc_w is not None: aucs.append(auc_w)
            if rk is not None: ranks.append(rk)
            rows.append({
                "Smell": w,
                "Smell model accuracy (AUC)": f"{auc_w:.2f}" if auc_w is not None else "n/a",
                "Nose finds it in top 5 (testing)": f"{hit:.0%}" if hit is not None else "n/a",
                "Nose ranked it this sniff": f"#{rk} of {len(labels)}" if rk is not None else "n/a",
                "Nose confidence this sniff": f"{scores[lab_index[w]]:.2f}" if w in lab_index else "n/a",
            })
        st.table(pd.DataFrame(rows).set_index("Smell"))

        overlap = len(set(nose_top) & set(model_top[:5]))
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Smell model accuracy", f"{np.mean(aucs):.2f} AUC" if aucs else "n/a", help="0.5 is guessing, 1.0 is perfect")
        c2.metric("Nose hit rate (testing)", f"{np.mean(hits):.0%}" if hits else "n/a", help="How often the nose finds this smell in its top 5 guesses")
        c3.metric("Nose rank this sniff", f"#{min(ranks)}" if ranks else "n/a", help="Where the nose placed your smell among all 138 words")
        c4.metric("Models agree", f"{overlap} of 5", help="How many of the nose's top 5 words the smell model also puts in its top 5")
        if ev:
            st.caption(f"Across all {len(labels)} smell words the nose finds the right word in its top 5 about "
                       f"{ev['nose_top5']:.0%} of the time (random guessing: {ev['chance_top5']:.0%}). "
                       "The nose is simulated, so a real sensor would score lower. Distinctive smells (fruity, woody, vanilla) "
                       "work well; vague ones (tea, weedy, celery) do not.")

    ui.footer()
