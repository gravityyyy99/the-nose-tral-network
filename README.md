<div align="center">

# The Nose-tral Network

### Aroma-GPT: an AI that learns what smells are made of, paired with a virtual electronic nose

![Python](https://img.shields.io/badge/python-3.10%2B-c96442)
![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-788c5d)
![License: MIT](https://img.shields.io/badge/license-MIT-6b6a63)
![Status](https://img.shields.io/badge/electronic%20nose-simulated%20(real%20hardware%20planned)-c96442)

<img src="docs/screenshots/01-home.jpg" alt="The Nose-tral Network home page" width="780">

</div>

Hi, I'm Dibyajyoti. **The Nose-tral Network** is the project, and **Aroma-GPT** is the name I gave the AI inside it.
You pick or type a smell (Vanilla, Smoky, Woody, Citrus, or any of 138 smell words), and the app shows you what
a smell is made of, how a row of gas sensors would react to it, and what two different AI models think it smells like.

> **A quick honesty note up front:** the electronic nose in this project is **simulated in code**. There is no
> hardware yet. I explain exactly what is real and what is simulated in
> [What is real and what is simulated](#what-is-real-and-what-is-simulated). Connecting real sensors is my next big step.

---

## Contents

- [Demo](#demo)
- [Motion graphics](#motion-graphics)
- [In plain words (no background needed)](#in-plain-words-no-background-needed)
- [Why I built this](#why-i-built-this)
- [How it works](#how-it-works)
- [How accurate is it?](#how-accurate-is-it)
- [What is real and what is simulated](#what-is-real-and-what-is-simulated)
- [Tech stack](#tech-stack)
- [Credit: what this is based on, and what I built on top](#credit-what-this-is-based-on-and-what-i-built-on-top)
- [Install and run it yourself](#install-and-run-it-yourself)
- [Project structure](#project-structure)
- [Roadmap](#roadmap)
- [License and contact](#license-and-contact)

---

## Demo

### Demo video

<!-- TODO: add your demo video here.
     Option A (YouTube / Drive link):  [![Watch the demo](docs/screenshots/01-home.jpg)](YOUR_VIDEO_LINK)
     Option B (file in the repo):      drag the .mp4 into this README on GitHub's web editor and it will embed. -->

> **Demo video: coming soon.** (I'll add the link here.)

### Screenshots

| | |
|---|---|
| **Pick or type a smell** <br> <img src="docs/screenshots/01-home.jpg" width="380"> | **Results: the nose and the smell model side by side** <br> <img src="docs/screenshots/02-sniff-results.jpg" width="380"> |
| **All 138 smell words you can try** <br> <img src="docs/screenshots/03-keywords.jpg" width="380"> | **"Our journey": the whole build story, in motion** <br> <img src="docs/screenshots/04-journey.jpg" width="380"> |
| **"About me": a 3D hologram built from my photo that reacts as you scroll** <br> <img src="docs/screenshots/05-about-hologram.jpg" width="380"> | **A documentation "book" with 11 chapters** <br> <img src="docs/screenshots/07-documentation.jpg" width="380"> |
| **"Coming soon": the real-hardware chapter** <br> <img src="docs/screenshots/08-coming-soon.jpg" width="380"> | *(more screenshots and a screen recording to come)* |

<!-- TODO: add a screen recording (GIF or mp4) of: picking "Vanilla", flipping through the tabs, and switching day/night mode. -->

The site has a **day/night switch** (it opens in dark mode), a menu that closes itself when you pick a section, and it
works on phones, tablets and big screens.


---

## Motion graphics

A smell is hard to explain with words alone, so here it is in motion.

**A tour of the site** (an animated slideshow made from the real screenshots above):

<div align="center">
<img src="docs/img/tour.gif" alt="Animated tour of the site" width="720">
</div>

**The 3D hologram** from the "About me" page. This GIF is **rendered by a Python script** (`tools/make_gifs.py`) that turns
my photo into a point cloud and uses brightness as depth, so it shows the idea. It is not a screen capture of the page.
The page itself does the same thing live in the browser with three.js and GSAP, and reacts as you scroll.

<div align="center">
<img src="docs/img/hologram.gif" alt="Rotating 3D hologram" width="360">
</div>

**Animated explainers** (animated SVGs, they play right here on GitHub):

| Where to see it | What it shows |
|---|---|
| [In plain words](#in-plain-words-no-background-needed) | The journey of one smell, from a word to an AI guess |
| [How it works](#how-it-works) | A 3D isometric electronic nose whose 8 bars morph between six smells |
| [The two models, briefly](#the-two-models-briefly) | How the smell model learns from molecule fingerprints |

> If an animation looks still, your viewer may not support animated SVGs. Open the file in `docs/img/` in a browser.
> **Screen recording:** a real screen recording of the live app is a nice extra. I'll add one later.
> <!-- TODO: add a real screen recording (mp4 or GIF) of the live app here -->

---

## In plain words (no background needed)

**What is this?**
Smells are made of tiny particles called *molecules* floating in the air. When you smell coffee, molecules from the
coffee reach your nose, and your brain turns that into "coffee". This project teaches a computer to do something
similar in two ways:

1. **From the chemistry.** I give a model the *shape* of a molecule and it says which smell words fit it
   (sweet, woody, fruity, smoky...). It learned this from almost 5,000 molecules that experts had already labelled.
2. **From sensors.** An *electronic nose* is a row of gas sensors. Each sensor reacts a little differently to different
   chemicals, so together they make a pattern of numbers, like a fingerprint. A second model looks only at that
   pattern and guesses the smell.

<img src="docs/img/anim-journey.svg" alt="Animated journey of one smell" width="100%">

**An everyday comparison.** Think of a wine taster. After tasting thousands of wines they can say "cherry, oak, a bit of
smoke". Nobody gave them a rulebook; they learned the patterns from examples. My models learn the same way, from examples.

**About the name.** "Aroma-GPT" is a playful name. It is **not** a chatbot and not a large language model. It is two
small machine-learning models (random forests) working together. "Nose-tral" is a pun on *neural network* and *nose*.

### Where electronic noses are used in the real world

Electronic noses are a real technology. In general, people use them for things like:

| Area | What the sensor array is used for |
|---|---|
| Food and drink | Checking freshness, spotting spoilage, keeping flavour consistent between batches |
| Air and environment | Monitoring air quality, detecting odours near factories or waste sites |
| Safety | Noticing gas leaks or dangerous fumes |
| Health research | Studying smells in breath as a possible sign of illness (this is still research) |
| Agriculture | Judging when fruit is ripe or when stored grain is going bad |
| Perfume and flavour industry | Comparing scents quickly instead of relying only on human noses |

*This table describes e-noses in general. My project is a learning demo and does not do any of these jobs yet.*

### How you could build one for real

In very simple terms, a real system needs four things:

1. **Hardware:** a few gas sensors (or one sensor that heats to several temperatures), plus a small board that reads them.
2. **Data:** record each smell many times, with clean air in between, on different days, because sensors drift.
3. **A model:** turn each recording into numbers and train a classifier to tell the smells apart.
4. **An honest test:** try it on recordings from a day the model has never seen. That is the test that matters.

That is exactly my plan for the next stage of this project (see the [Roadmap](#roadmap)).

---

## Why I built this

I was fascinated that smell is the sense computers understand least. Cameras see and microphones hear, but describing
a smell is still an open problem. I wanted to build the whole chain in one place, from a smell word, to the molecules
behind it, to sensor readings, to an AI guess, and to explain it clearly enough that anyone could follow along.

I started with a **virtual** electronic nose so I could build and test everything (the models, the app, the testing)
without waiting for hardware. **My plan is to connect a real gas sensor next** (for example a BME688 on an ESP32),
record real smells, retrain the nose model on real readings, and rank scents using actual hardware. The simulated
sensor was built so that swapping in real readings changes only where the 8 numbers come from.

---

## How it works

<img src="docs/img/architecture.svg" alt="How the pieces fit together" width="100%">

Say you pick **Vanilla** (or **Smoky**, **Woody**, **Citrus**; any of the 138 words works, and typos are fixed for you, so
"lavendar" becomes "lavender"). Here is what happens:

1. **Molecules.** The app picks six real aroma molecules that carry that smell. For six everyday smells (coffee,
   vanilla candle, mint, lemon, banana, wood smoke) I wrote the molecule lists by hand. For the other words it takes
   molecules the dataset's experts labelled with that word. The molecules are drawn as chemical structures.
2. **Sensors (simulated).** Eight virtual gas sensors react to those molecules: "Small and light", "Large and heavy",
   "Oily", "Water-loving", "Oxygen-rich", "Sulfur", "Aromatic rings" and "General gases". Random noise, humidity and drift are
   added so that no two sniffs are identical, like on real hardware. You see the 8 reaction bars.
3. **The nose model** looks *only* at those 8 numbers and predicts smell words. It never sees the molecules.
4. **The smell model** looks *only* at the molecules' chemical structure and predicts smell words.
5. **The Accuracy tab** shows the numbers for the smell you picked: how well the smell model does on that word, how
   often the nose finds it in testing, where the nose ranked it *this* sniff (out of 138), and how many of its top 5
   words the smell model agrees with.

**What the "confidence" is:** the nose model's score for a word (0 to 1) and where that word ranks among all 138. It is a
model score, not a guarantee.

<img src="docs/img/anim-nose-3d.svg" alt="Animated 3D isometric view of the simulated electronic nose" width="100%">

*The 8 bars are the SIMULATED sensors. Their heights come from the real simulator output (average of 60 noisy sniffs per smell), scaled so differences are visible.*

<img src="docs/img/fingerprints.svg" alt="Simulated sensor fingerprints for six smells" width="100%">

Each smell leaves a different pattern across the sensors, and that pattern is what the nose model learns. Where two rows
look alike, the nose gets confused.

### The two models, briefly

<img src="docs/img/anim-learning.svg" alt="Animated: how the smell model learns" width="100%">

*An illustration of the idea. The real fingerprint has 2,048 slots; the drawing shrinks it to fit.*

- **Smell model.** Each molecule becomes a "fingerprint": a count of its chemical fragments (a Morgan fingerprint from RDKit,
  2,048 numbers). A random forest (100 trees) learns which fragments go with which of 138 smell words.
- **Nose model.** I simulate thousands of noisy sniffs of mixtures, and a random forest regressor learns to predict the
  smell-word profile from just the 8 sensor numbers.

There is also a smaller classifier that recognises the 6 hand-written everyday smells.

---

## How accurate is it?

These numbers are **measured**, not guessed. They come from [`evaluate.py`](evaluate.py) (saved in
[`evaluation.json`](evaluation.json)), computed on examples the models did not train on.

<img src="docs/img/accuracy.svg" alt="Measured accuracy" width="100%">

| | Result | Random guessing |
|---|---|---|
| Smell model, average ROC-AUC over 138 words | **0.86** | 0.50 |
| Nose, right word in its top 5 guesses | **38%** | 3.6% |
| Nose, best guess is the right word | **10%** | 0.7% |

And for the four scents from the example above (from the same evaluation):

| Smell | Nose finds it in its top 5 | Smell model accuracy (ROC-AUC) |
|---|---|---|
| Vanilla | 83% | 0.94 |
| Smoky | 26% | 0.96 |
| Woody | 100% | 0.83 |
| Citrus | 84% | 0.84 |

Accuracy varies a lot by smell. Distinctive ones (fruity, woody, vanilla) work well. Vague ones (tea, weedy, celery) do not,
and **lavender is 0%** for the nose, which is a real weakness I show rather than hide. Notice that *smoky* is easy for the
smell model (0.96) but hard for the nose (26%): the chemistry is distinctive, but eight simulated sensors don't separate it well.

**Please read these as a demo of the method, not as a performance claim.** The nose is tested on the same simulator it
learned from, so a real sensor would score lower.

---

## What is real and what is simulated

<img src="docs/img/honesty.svg" alt="What is real and what is simulated" width="100%">

I went through the code to label every output:

| Output in the app | Is it real? |
|---|---|
| Smell model (random forest trained on the OpenPOM dataset) | **Real model**, really trained and tested on held-out molecules (ROC-AUC 0.86) |
| Nose model and the 6-smell classifier | **Real models**, but trained on **simulated** sensor data |
| The 8 sensor readings | **Simulated.** `sensor.py` is maths plus random noise. No hardware is involved |
| Nose accuracy numbers | **Real measurements, on the simulator.** A real sensor would score lower |
| Per-word accuracy table / `evaluation.json` | **Real**, produced by `evaluate.py` (a snapshot of the last run) |
| Molecules for the 6 everyday smells (`samples.json`) | **Hand-picked** by me from chemistry knowledge, not measured from real products |
| Molecules for other smell words | Chosen from the dataset's expert labels (the 25 "purest" per word, 6 drawn at random per sniff) |
| Smell-model panel in the app | The final model was trained on **all** the data, so for these molecules it has effectively seen the answers. It is a demo, not a fresh test. The honest score is the held-out **0.86** |
| A few numbers written in the docs text ("about 98%" for the 6-smell nose, the example table in chapter 8) | Copied from my last run. They can shift slightly if you retrain |
| Animated diagrams and the hologram GIF | **Illustrations.** The 3D bars use simulated sensor values. The hologram GIF is script-rendered from my photo. The tour GIF is made from real screenshots |
| Counters like 4,983 molecules, 138 words, 8 sensors, 6,000 sniffs, and the 80/20 split sizes | Facts about the code and data |

If `evaluation.json` is missing, the site shows "n/a" instead of any number.

---

## Tech stack

| Tool | What I used it for |
|---|---|
| **Python 3.10+** | Everything |
| **RDKit** | Reading molecules, building chemical fingerprints, drawing structures |
| **scikit-learn** | The random forest models and the accuracy measures |
| **pandas / NumPy** | Handling the data |
| **Streamlit** | The web app and multi-page navigation |
| **Altair** | The charts |
| **three.js + GSAP** (loaded from a CDN) | The 3D hologram and scroll animation on the About page |
| **Plain CSS and a little JavaScript** | The Claude-inspired look, dark/light mode, and the motion |

---

## Credit: what this is based on, and what I built on top

**This project is inspired by Google Research's work on the "principal odor map"**:

- Paper: Lee et al., *A principal odor map unifies diverse tasks in olfactory perception*, **Science (2023)**, from Google
  Research, Osmo and the Monell Chemical Senses Center. [doi:10.1126/science.ade4401](https://doi.org/10.1126/science.ade4401)

**The repository I used is [OpenPOM](https://github.com/BioMachineLearning/openpom)**, an open-source (MIT) rebuild of
that research by the community. To be accurate: it is a community rebuild, **not** an official Google repository.
OpenPOM's dataset is built on the Good Scents and Leffingwell odour databases, whose experts labelled the molecules.

**What I took from it:** only the **dataset** (`curated_GS_LF_merged_4983.csv`: 4,983 molecules, 138 smell words). My code
downloads it from OpenPOM when you train. I did **not** use OpenPOM's model code.

**What I built on top (all new in this repo):**

- A simpler smell model of my own (random forest on Morgan fingerprints), with a measured ROC-AUC of 0.86.
  (OpenPOM's graph neural network reports about 0.89 in its authors' tests; moving to it is on my roadmap.)
- The **simulated 8-sensor electronic nose**, with noise, humidity and drift.
- The **nose model** that works from sensor readings alone, and the any-smell training on mixtures.
- A **free-text interface** with spelling correction, and per-smell accuracy.
- The whole **website**: day/night mode, the "Our journey" page, a 3D hologram About page, and an 11-chapter documentation book.
- Honest evaluation of every smell word, including the failures.

---

## Install and run it yourself

You need **Python 3.10 or newer** (I built and tested it on 3.11) and an internet connection (the dataset is downloaded once).

```bash
# 1. Get the code
git clone https://github.com/gravityyyy99/the-nose-tral-network.git
cd the-nose-tral-network

# 2. Make a virtual environment and install the packages
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Run the app (the small trained models are already included in the repo)
streamlit run app.py
```

Then open the address Streamlit prints (usually http://localhost:8501), pick a smell and press **Sniff**.

- The trained models are included (`smell_model.joblib`, `nose_profile.joblib`, `nose.joblib`, about 27 MB in total), and the app
  needs roughly 300 MB of memory to run them. The first time it needs the dataset it downloads it into `data/` (1.6 MB).
- **Want to retrain from scratch?** Run these three, in order (a few minutes in total). They overwrite the models and `evaluation.json`:
  ```bash
  python smell_model.py              # downloads the dataset, trains the smell model, prints its ROC-AUC
  python train_nose.py               # simulates sniffs and trains the nose models
  python evaluate.py                 # measures accuracy per smell word (writes evaluation.json)
  ```
- To check everything works without a browser: `python test_app.py`.
- Your numbers may differ slightly from mine: the models and simulated sniffs are random, and I fixed seeds where I could.

---

## Project structure

```
app.py               the web app entry point: menu, logo, day/night switch
sniff_page.py        the "Sniff a smell" page (molecules, sensors, results, accuracy)
keywords_page.py     the 138 smell words you can try
journey_page.py      the animated "Our journey" page with graphs
about_page.py        the 3D "About me" page (assets/about3d.html)
docs_pages.py        the documentation book (docs_content/*.md)
ui.py                shared look and feel, dark/light mode, responsive CSS

smell_model.py       molecule fingerprints, training and prediction (molecule -> smell words)
sensor.py            the SIMULATED 8-sensor electronic nose
smell_query.py       spelling correction and molecule lookup
train_nose.py        trains the nose models on simulated sniffs
evaluate.py          measures accuracy per smell word -> evaluation.json
test_app.py          a quick end-to-end check
samples.json         six hand-written everyday smells and their molecules

assets/              logo files, the 3D hologram page, my photo
docs/img/            diagrams, animated SVGs and GIFs used in this README
docs/screenshots/    screenshots used in this README
tools/               scripts that draw the README graphics (make_readme_graphics.py, make_motion_graphics.py, make_gifs.py)
```

---

## Roadmap

<img src="docs/img/roadmap.svg" alt="Project roadmap" width="100%">

**Done**
- [x] Smell model trained on 4,983 expert-labelled molecules (ROC-AUC 0.86 on held-out molecules)
- [x] Simulated 8-sensor electronic nose with noise, humidity and drift
- [x] Nose model that works from the 8 numbers alone, for any of 138 smell words
- [x] Typeable interface with spelling correction, and per-smell accuracy
- [x] Evaluation of every smell word, including where it fails
- [x] Website, documentation book and "Our journey" page

**Next: the hardware version**
- [ ] Connect a real gas sensor (for example a BME688 on an ESP32) and stream readings to a laptop
- [ ] Record real smells in jars over several days, with clean air in between
- [ ] Retrain the nose model on real readings (replacing `sensor.py`)
- [ ] Test on sessions the model has never seen, and publish every result, good or bad
- [ ] Rank scents with the real device

**Later**
- [ ] Try OpenPOM's graph neural network as a stronger smell model
- [ ] A harder test that holds out whole chemical families
- [ ] Describe a smell in words and suggest molecules for it

---

## License and contact

Released under the [MIT License](LICENSE). &copy; 2026 Dibyajyoti Pradhan.

- GitHub: [@gravityyyy99](https://github.com/gravityyyy99)
- LinkedIn: [Dibyajyoti Pradhan](https://www.linkedin.com/in/dibyajyotipradhan/)

If you try it, I'd love to hear what you think, especially which smells it gets wrong.
