"""Generates the SVG diagrams used in README.md (docs/img/*.svg).

The accuracy chart uses the real numbers in evaluation.json. The sensor-fingerprint heatmap is computed
from the simulated sensors in sensor.py. Everything else is a hand-drawn diagram.

Run from the project root:  python tools/make_readme_graphics.py
"""
import json
import os
import sys
import textwrap
from xml.sax.saxutils import escape

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
OUT = os.path.join(ROOT, "docs", "img")
os.makedirs(OUT, exist_ok=True)

BG, CARD, LINE = "#faf9f5", "#ffffff", "#e3e0d4"
INK, MUTED, ACC, SAGE, SOFT = "#141413", "#6b6a63", "#c96442", "#788c5d", "#f0eee6"
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(title)}">'
            f'<rect width="{w}" height="{h}" rx="18" fill="{BG}"/>{body}</svg>')


def text(x, y, s, size=14, fill=INK, weight=400, anchor="start", family=SANS, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}" '
            f'font-family="{family}" {extra}>{escape(str(s))}</text>')


def box(x, y, w, h, fill=CARD, stroke=LINE, r=14, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{d}/>'


def arrow(x1, y1, x2, y2, color=ACC):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2 - 7}" y2="{y2}" stroke="{color}" stroke-width="2.5" stroke-linecap="round"/>'
            f'<polygon points="{x2},{y2} {x2 - 10},{y2 - 6} {x2 - 10},{y2 + 6}" fill="{color}"/>')


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name)


# ------------------------------------------------------------------ 1. the journey of a smell
def journey():
    steps = [("1", "You pick a smell", "e.g. Vanilla, Smoky,\nWoody or Citrus"),
             ("2", "Real molecules", "6 aroma molecules that\ncarry that smell"),
             ("3", "8 virtual sensors", "each reacts a little\ndifferently (simulated)"),
             ("4", "Two AIs answer", "one reads the sensors,\none reads the molecules")]
    b = text(40, 52, "The journey of one smell", 26, INK, 500, family=SERIF)
    b += text(40, 80, "What happens from the moment you pick a scent to the answers on screen", 14, MUTED)
    x = 40
    for i, (n, t, d) in enumerate(steps):
        b += box(x, 110, 215, 150)
        b += f'<circle cx="{x + 36}" cy="148" r="17" fill="{ACC}"/>' + text(x + 36, 154, n, 16, "#fff", 700, "middle")
        b += text(x + 20, 195, t, 17, INK, 600, family=SERIF)
        for j, line in enumerate(d.split("\n")):
            b += text(x + 20, 222 + j * 19, line, 13, MUTED)
        if i < 3:
            b += arrow(x + 218, 185, x + 262, 185)
        x += 262
    b += box(40, 290, 1010, 74, SOFT, SOFT)
    b += text(60, 322, "What you see:", 14, ACC, 700) + text(172, 322, "the molecules drawn as structures, the 8 sensor bars,", 14, INK)
    b += text(60, 345, "the nose's guess, the smell model's words, and the measured accuracy for that smell.", 14, INK)
    save("journey.svg", svg(1090, 390, b, "The journey of one smell"))


# ------------------------------------------------------------------ 2. architecture
def architecture():
    b = text(40, 50, "How the pieces fit together", 26, INK, 500, family=SERIF)
    b += text(40, 76, "Two models look at the same smell in two different ways", 14, MUTED)
    b += box(40, 120, 190, 70) + text(135, 150, "Smell word", 16, INK, 600, "middle", SERIF) + text(135, 172, "typed (typos fixed)", 12, MUTED, anchor="middle")
    b += arrow(232, 155, 290, 155)
    b += box(292, 120, 220, 70) + text(402, 150, "Real molecules", 16, INK, 600, "middle", SERIF) + text(402, 172, "from the dataset", 12, MUTED, anchor="middle")
    # branch 1: sensors -> nose model
    b += arrow(514, 140, 580, 100)
    b += box(582, 60, 210, 70, "#fbeee8", ACC) + text(687, 90, "8 simulated sensors", 15, INK, 600, "middle", SERIF) + text(687, 112, "noise + humidity + drift", 12, MUTED, anchor="middle")
    b += arrow(794, 95, 850, 95)
    b += box(852, 60, 200, 70, "#fbeee8", ACC) + text(952, 90, "Nose model", 16, INK, 600, "middle", SERIF) + text(952, 112, "numbers in, words out", 12, MUTED, anchor="middle")
    # branch 2: smell model
    b += arrow(514, 170, 580, 215)
    b += box(582, 180, 210, 70, "#eef2e8", SAGE) + text(687, 210, "Chemical fingerprint", 15, INK, 600, "middle", SERIF) + text(687, 232, "2,048 fragment counts", 12, MUTED, anchor="middle")
    b += arrow(794, 215, 850, 215)
    b += box(852, 180, 200, 70, "#eef2e8", SAGE) + text(952, 210, "Smell model", 16, INK, 600, "middle", SERIF) + text(952, 232, "structure in, words out", 12, MUTED, anchor="middle")
    b += box(40, 285, 1012, 70, SOFT, SOFT)
    b += text(60, 315, "Then the app compares both answers and shows", 14, INK) + text(60, 337, "confidence, molecules, sensors and accuracy for the smell you picked.", 14, INK)
    b += text(782, 82, "SIMULATED", 10, ACC, 700, "middle", extra='letter-spacing="2"')
    save("architecture.svg", svg(1090, 385, b, "Architecture of the project"))


# ------------------------------------------------------------------ 3. roadmap
def roadmap():
    done = ["The idea", "Get the data", "Smell model", "Simulated nose", "Train 6-smell nose",
            "Any-smell nose", "Typeable + typo fix", "Measure each word", "App + docs book"]
    b = text(40, 50, "The roadmap", 26, INK, 500, family=SERIF)
    b += text(40, 76, "Where this project started, where it is now, and where it is going", 14, MUTED)
    n = len(done) + 1
    x0, x1, y = 70, 1130, 190
    b += f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{LINE}" stroke-width="4" stroke-linecap="round"/>'
    b += f'<line x1="{x0}" y1="{y}" x2="{x0 + (x1 - x0) * 8 / 9}" y2="{y}" stroke="{ACC}" stroke-width="4" stroke-linecap="round"/>'
    for i, label in enumerate(done + ["Real sensors"]):
        x = x0 + (x1 - x0) * i / (n - 1)
        last = i == n - 1
        fill = BG if last else ACC
        stroke = f' stroke="{ACC}" stroke-width="3" stroke-dasharray="4 3"' if last else ""
        b += f'<circle cx="{x}" cy="{y}" r="17" fill="{fill}"{stroke}/>' + text(x, y + 5, i + 1, 14, ACC if last else "#fff", 700, "middle")
        up = i % 2 == 0
        ly = y - 40 if up else y + 50
        b += text(x, ly, label, 13, INK, 600 if not last else 700, "middle")
        b += text(x, ly + 16, "next" if last else "done", 11, ACC if last else SAGE, 700, "middle")
    b += box(40, 270, 1090, 66, SOFT, SOFT)
    b += text(60, 298, "Next: connect a real gas sensor (for example a BME688 on an ESP32), record real smells,", 14, INK)
    b += text(60, 320, "retrain the nose model on real readings and test it honestly on sessions it has never seen.", 14, INK)
    save("roadmap.svg", svg(1170, 360, b, "Project roadmap"))


# ------------------------------------------------------------------ 4. accuracy (real numbers from evaluation.json)
def accuracy():
    ev = json.load(open(os.path.join(ROOT, "evaluation.json")))
    top5 = ev["nose_top5_per_word"]
    s = sorted(top5, key=lambda w: (-top5[w], w))
    best, worst = s[:8], s[-8:][::-1]
    b = text(40, 50, "How accurate is it? (measured, not guessed)", 26, INK, 500, family=SERIF)
    b += text(40, 76, "All numbers come from evaluation.json, produced by evaluate.py on data the models never trained on", 14, MUTED)
    cards = [(f"{ev['smell_model_mean_auc']:.2f}", "Smell model, ROC-AUC", "0.50 = guessing, 1.00 = perfect"),
             (f"{ev['nose_top5']:.0%}", "Nose: right word in top 5", f"random guessing: {ev['chance_top5']:.1%}"),
             (f"{ev['nose_top1']:.0%}", "Nose: best guess correct", f"random guessing: {ev['chance_top1']:.1%}")]
    for i, (big, lab, sub) in enumerate(cards):
        x = 40 + i * 345
        b += box(x, 100, 325, 110, SOFT, SOFT)
        b += text(x + 22, 155, big, 44, ACC, 500, family=SERIF) + text(x + 22, 180, lab, 14, INK, 600) + text(x + 22, 198, sub, 12, MUTED)

    def bars(x, title, words, color):
        out = text(x, 250, title, 16, INK, 600, family=SERIF)
        for i, w in enumerate(words):
            y = 272 + i * 26
            v = top5[w]
            out += text(x, y + 14, w, 13, INK) + f'<rect x="{x + 110}" y="{y}" width="250" height="16" rx="8" fill="{SOFT}"/>'
            out += f'<rect x="{x + 110}" y="{y}" width="{max(250 * v, 3):.0f}" height="16" rx="8" fill="{color}"/>'
            out += text(x + 370, y + 13, f"{v:.0%}", 12, MUTED)
        return out

    b += bars(40, "Smells the nose finds easily", best, SAGE) + bars(560, "Smells the nose finds hard", worst, ACC)
    b += text(40, 505, "Bars show how often the simulated nose finds the right smell word among its top 5 guesses, per smell word.", 12, MUTED)
    b += text(40, 524, "The nose is simulated, so a real sensor would score lower.", 12, MUTED)
    save("accuracy.svg", svg(1090, 545, b, "Measured accuracy"))


# ------------------------------------------------------------------ 5. sensor fingerprints (simulated)
def fingerprints():
    import sensor
    rng = np.random.default_rng(5)
    samples = sensor.load_samples()
    names = list(samples)
    grid = []
    for name in names:
        smiles = list(samples[name]["molecules"].values())
        reads = np.array([sensor.sniff(smiles, rng) for _ in range(60)])
        grid.append(sensor.to_percent(reads).mean(axis=0))
    grid = np.array(grid)
    lo, hi = grid.min(), grid.max()
    b = text(40, 50, "Every smell leaves a fingerprint", 26, INK, 500, family=SERIF)
    b += text(40, 76, "Average reaction of the 8 SIMULATED sensors to six everyday smells (60 noisy sniffs each). Darker = stronger.", 14, MUTED)
    x0, y0, cw, ch = 190, 130, 100, 44
    for j, ch_name in enumerate(sensor.CHANNELS):
        b += text(x0 + j * cw + cw / 2, y0 - 12, ch_name, 11, INK, 600, "middle")
    for i, name in enumerate(names):
        b += text(x0 - 14, y0 + i * ch + 27, name, 14, INK, 600, "end")
        for j in range(len(sensor.CHANNELS)):
            t = (grid[i, j] - lo) / (hi - lo + 1e-9)
            r = int(244 + (122 - 244) * t); g = int(227 + (46 - 227) * t); bl = int(218 + (20 - 218) * t)
            b += f'<rect x="{x0 + j * cw + 2}" y="{y0 + i * ch + 2}" width="{cw - 4}" height="{ch - 4}" rx="8" fill="rgb({r},{g},{bl})"/>'
            b += text(x0 + j * cw + cw / 2, y0 + i * ch + 28, f"{grid[i, j]:.0f}", 13, "#fff" if t > .55 else INK, 600, "middle")
    b += text(40, 130 + len(names) * ch + 40, "The pattern across a row is what the nose model learns to recognise. Where rows look alike, the nose gets confused.", 13, MUTED)
    save("fingerprints.svg", svg(1030, 130 + len(names) * ch + 70, b, "Simulated sensor fingerprints"))


# ------------------------------------------------------------------ 6. honesty map
def honesty():
    real = ["Smell model trained on the OpenPOM dataset (4,983 molecules)", "Smell model accuracy on held-out molecules (0.83 ROC-AUC)",
            "Nose model trained with scikit-learn on simulated sniffs", "Per-word accuracy table (evaluation.json)",
            "Spelling correction, molecule drawings, the app itself"]
    fake = ["All 8 sensor readings: maths plus random noise, no hardware", "Nose accuracy numbers: measured on the same simulator it learned from",
            "Smell compositions in samples.json: hand-picked, not measured", "Molecules for a smell word: chosen from dataset labels",
            "Smell-model panel in the app: final model saw these molecules"]
    b = text(40, 50, "What is real and what is simulated", 26, INK, 500, family=SERIF)
    b += text(40, 76, "Honest labels for every output in the app", 14, MUTED)
    for x, title, items, col, tag in ((40, "Real results", real, SAGE, "REAL"), (560, "Simulated or demo", fake, ACC, "SIMULATED")):
        b += box(x, 100, 500, 300, CARD, col)
        b += f'<rect x="{x + 20}" y="120" width="{86 if tag == "REAL" else 120}" height="24" rx="12" fill="{col}"/>' + text(x + 20 + (43 if tag == "REAL" else 60), 137, tag, 12, "#fff", 700, "middle", extra='letter-spacing="2"')
        b += text(x + 20, 175, title, 20, INK, 500, family=SERIF)
        for i, it in enumerate(items):
            lines = textwrap.wrap(it, 54, break_on_hyphens=False)
            yy = 205 + i * 38
            b += f'<circle cx="{x + 28}" cy="{yy - 4}" r="4" fill="{col}"/>'
            for k, ln in enumerate(lines):
                b += text(x + 44, yy + k * 16, ln, 12.5, INK)
    save("honesty.svg", svg(1100, 430, b, "Real versus simulated"))


if __name__ == "__main__":
    journey(); architecture(); roadmap(); accuracy(); fingerprints(); honesty()
