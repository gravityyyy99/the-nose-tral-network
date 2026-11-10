# The app

*Good science is wasted if nobody can try it. This chapter shows how all the pieces become something you can simply type into.*

Everything you are using is a **Streamlit** app: a Python library that turns scripts into web pages.

## What happens when you press Enter

1. **Spelling check** (`smell_query.py`). Your text is split on commas or the word "and". Each word is compared with the 138 smell words and the six sample names:
   - an exact match is used as it is,
   - a close match (similarity of at least 0.75, using Python's `difflib`) is **autocorrected**, and a warning tells you,
   - a weaker match (at least 0.5) is offered as a **suggestion**,
   - anything else is reported as unknown.
2. **Molecules.** The program fetches real molecules for your smell (see *The data*).
3. **Sensors.** One simulated sniff produces 8 readings (see *The electronic nose*).
4. **Nose model.** It predicts smell words from the 8 numbers only.
5. **Smell model.** It predicts smell words from the molecule structures.
6. **Display.** The app shows both answers, the molecule drawings, the sensor chart and the accuracy table.

## The tabs on the results

| Tab | Shows |
|---|---|
| Verdict | the top words from each model, with bar charts |
| Molecules | the real molecules, drawn as chemical structures |
| Sensors | the 8 sensor bars, with a table of what each reacts to |
| Accuracy | measured accuracy for the smell you asked about |

## The verdict message

- If the nose's top 5 includes the word you asked for, it says the nose **recognised** it.
- If not, but the nose and the smell model share words, it reports the **overlap**.
- If neither, it says the nose is **unsure**. This is shown honestly rather than hidden.

## Project layout

| File | Job |
|---|---|
| `app.py` | the web app entry point and menu |
| `sniff_page.py` | the interactive "Sniff a smell" page |
| `keywords_page.py` | the list of smell words you can test |
| `journey_page.py` | the animated "Our journey" page and its graphs |
| `about_page.py`, `site_config.py` | the "About me" page and author details |
| `assets/` | the logo files (light and dark versions) |
| `docs_pages.py`, `docs_content/` | this documentation |
| `ui.py` | the shared look and feel |
| `smell_model.py` | fingerprints, training and prediction for the smell model |
| `sensor.py` | the simulated 8-sensor array |
| `smell_query.py` | spelling correction and molecule lookup |
| `train_nose.py` | training the two nose models |
| `evaluate.py` | measuring accuracy per smell word |
| `test_app.py` | an automatic check that everything runs |
| `samples.json` | the six hand-written smells |

## Technology used

Python, RDKit (chemistry), scikit-learn (random forests), pandas and NumPy (data), Altair (charts) and Streamlit (the app).

> **The takeaway.** The app is a thin layer over the models: fix the spelling, pick molecules, sniff, ask both models, and show everything, including when the nose is unsure.
