"""Animated SVG explainers for README.md (docs/img/anim-*.svg).

GitHub plays animated SVGs inline. The 3D isometric 'electronic nose' uses the real fingerprints produced by the
SIMULATED sensors in sensor.py (average of 60 noisy sniffs per smell); everything else is an illustration.

Run from the project root:  python tools/make_motion_graphics.py
"""
import math
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_readme_graphics import (ACC, BG, CARD, INK, LINE, MUTED, ROOT, SAGE, SANS, SERIF, SOFT,  # noqa: E402
                                  arrow, box, save, svg, text)

sys.path.insert(0, ROOT)


def anim(attr, values, times, dur, extra=""):
    """A looping SMIL <animate>. `times` are fractions of the loop (start at 0, end at 1)."""
    return (f'<animate attributeName="{attr}" values="{";".join(str(v) for v in values)}" '
            f'keyTimes="{";".join(f"{t:.4f}" for t in times)}" dur="{dur}s" repeatCount="indefinite" {extra}/>')


def window(i, n, lead=0.02, hold=None):
    """keyTimes + opacity values so something is visible only during slot i of n in a loop."""
    s, e = i / n, (i + 1) / n
    hold = hold if hold is not None else (e - s) - 2 * lead
    t = [0.0, s + 0.0005, s + lead, s + lead + hold, e - 0.0005, 1.0]
    return t, [0, 0, 1, 1, 0, 0]


# ---------------------------------------------------------------- 1. animated journey
def anim_journey():
    dur = 8
    steps = [("1", "You pick a smell", "Vanilla, Smoky,\nWoody or Citrus"),
             ("2", "Real molecules", "6 aroma molecules\nthat carry that smell"),
             ("3", "8 virtual sensors", "each reacts a little\ndifferently (simulated)"),
             ("4", "Two AIs answer", "one reads sensors,\none reads molecules")]
    b = text(40, 52, "The journey of one smell, animated", 26, INK, 500, family=SERIF)
    b += text(40, 80, "Watch a smell travel from a word, to chemistry, to sensor readings, to an AI guess", 14, MUTED)
    xs = [40 + i * 262 for i in range(4)]
    for i, x in enumerate(xs):
        b += box(x, 120, 215, 170)
        t, v = window(i, 4, lead=0.03)
        b += (f'<rect x="{x}" y="120" width="215" height="170" rx="14" fill="none" stroke="{ACC}" stroke-width="3.5" opacity="0">'
              f'{anim("opacity", v, t, dur)}</rect>')
        b += f'<circle cx="{x + 34}" cy="152" r="16" fill="{ACC}"/>' + text(x + 34, 158, steps[i][0], 15, "#fff", 700, "middle")
        b += text(x + 20, 205, steps[i][1], 17, INK, 600, family=SERIF)
        for j, line in enumerate(steps[i][2].split("\n")):
            b += text(x + 20, 230 + j * 18, line, 13, MUTED)
    # little icons that move
    b += (f'<text x="{xs[0] + 150}" y="160" font-size="15" fill="{ACC}" font-family="{SERIF}" font-weight="600">Vanilla'
          f'{anim("opacity", [1, 1, 0, 0, 1], [0, .4, .45, .95, 1], 2)}</text>'
          f'<rect x="{xs[0] + 196}" y="146" width="2" height="16" fill="{ACC}">{anim("opacity", [1, 0, 1], [0, .5, 1], 1)}</rect>')
    mx, my = xs[1] + 160, 158
    ring = " ".join(f"{mx + 15 * math.cos(math.radians(a)):.1f},{my + 15 * math.sin(math.radians(a)):.1f}" for a in range(0, 360, 60))
    b += (f'<g><polygon points="{ring}" fill="none" stroke="{SAGE}" stroke-width="2.5"/>'
          f'<circle cx="{mx + 15}" cy="{my}" r="4" fill="{ACC}"/><circle cx="{mx - 7.5}" cy="{my - 13}" r="4" fill="{SAGE}"/>'
          f'<animateTransform attributeName="transform" type="rotate" from="0 {mx} {my}" to="360 {mx} {my}" dur="8s" repeatCount="indefinite"/></g>')
    bx = xs[2] + 135
    for k in range(8):
        h = [10, 22, 16, 26, 12, 20, 28, 14][k]
        b += (f'<rect x="{bx + k * 8}" y="{170 - h}" width="5" height="{h}" rx="2" fill="{ACC}">'
              f'<animate attributeName="height" values="{h};{max(6, 30 - h)};{h}" dur="{1.6 + k * 0.17:.2f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="y" values="{170 - h};{170 - max(6, 30 - h)};{170 - h}" dur="{1.6 + k * 0.17:.2f}s" repeatCount="indefinite"/></rect>')
    nx = xs[3] + 150
    b += (f'<circle cx="{nx}" cy="158" r="9" fill="{ACC}"><animate attributeName="r" values="9;12;9" dur="1.4s" repeatCount="indefinite"/></circle>'
          f'<circle cx="{nx + 32}" cy="158" r="9" fill="{SAGE}"><animate attributeName="r" values="12;9;12" dur="1.4s" repeatCount="indefinite"/></circle>'
          f'<line x1="{nx + 11}" y1="158" x2="{nx + 21}" y2="158" stroke="{MUTED}" stroke-width="2"/>')
    # connectors with travelling dots
    for i in range(3):
        x1, x2 = xs[i] + 217, xs[i + 1] - 2
        b += f'<line x1="{x1}" y1="205" x2="{x2}" y2="205" stroke="{LINE}" stroke-width="3" stroke-linecap="round"/>'
        for k in range(3):
            b += (f'<circle r="5" cy="205" fill="{ACC}"><animate attributeName="cx" values="{x1};{x2}" dur="1.5s" begin="{k * 0.5 + i * 0.2:.2f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.85;1" dur="1.5s" begin="{k * 0.5 + i * 0.2:.2f}s" repeatCount="indefinite"/></circle>')
    b += box(40, 318, 1010, 58, SOFT, SOFT)
    b += text(60, 343, "At the end you see: the molecules drawn as structures, the 8 sensor bars, the nose's guess,", 14, INK)
    b += text(60, 363, "the smell model's words, and the measured accuracy for that smell.", 14, INK)
    save("anim-journey.svg", svg(1090, 400, b, "Animated journey of one smell"))


# ---------------------------------------------------------------- 2. 3D isometric nose
def anim_nose_3d():
    import sensor
    rng = np.random.default_rng(5)
    samples = sensor.load_samples()
    names = list(samples)
    grid = []
    for name in names:
        smiles = list(samples[name]["molecules"].values())
        grid.append(sensor.to_percent(np.array([sensor.sniff(smiles, rng) for _ in range(60)])).mean(axis=0))
    grid = np.array(grid)
    lo, hi = grid.min(), grid.max()
    heights = 10 + (grid - lo) / (hi - lo + 1e-9) * 150          # scaled for visibility

    u, ox, oy = 56, 320, 255
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))

    def iso(x, y, z):
        return ox + (x - y) * c30 * u, oy + (x + y) * s30 * u - z

    def pts(*ps):
        return " ".join(f"{iso(*p)[0]:.1f},{iso(*p)[1]:.1f}" for p in ps)

    b = text(40, 50, "A 3D look at the electronic nose", 26, INK, 500, family=SERIF)
    b += text(40, 76, "Each bar is one of the 8 SIMULATED sensors. Watch the fingerprint change from smell to smell.", 14, MUTED)
    # platform slab
    x0, x1, y0, y1, th = -0.7, 8.0, -1.4, 1.4, 14
    b += f'<polygon points="{pts((x0, y1, -th), (x1, y1, -th), (x1, y1, 0), (x0, y1, 0))}" fill="#d9d6c8"/>'
    b += f'<polygon points="{pts((x1, y0, -th), (x1, y1, -th), (x1, y1, 0), (x1, y0, 0))}" fill="#c4c0ae"/>'
    b += f'<polygon points="{pts((x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0))}" fill="{SOFT}" stroke="{LINE}" stroke-width="1.5"/>'
    for k in range(9):                                            # grid lines on the platform
        b += f'<polygon points="{pts((x0 + k * (x1 - x0) / 8, y0, 0), (x0 + k * (x1 - x0) / 8, y1, 0))}" fill="none" stroke="{LINE}" stroke-width="1"/>'
    n = len(names)
    times = [i / n for i in range(n)] + [1.0]
    splines = ";".join(["0.45 0 0.2 1"] * n)
    dur = n * 3.2
    cols = {"top": "#e08a68", "xf": ACC, "yf": "#9b4a2e"}
    for i in range(8):
        bx0, bx1, by0, by1 = i + 0.12, i + 0.82, -0.38, 0.38

        def state(h):
            return {"top": pts((bx0, by0, h), (bx1, by0, h), (bx1, by1, h), (bx0, by1, h)),
                    "xf": pts((bx1, by0, 0), (bx1, by1, 0), (bx1, by1, h), (bx1, by0, h)),
                    "yf": pts((bx0, by1, 0), (bx1, by1, 0), (bx1, by1, h), (bx0, by1, h))}

        seq = [state(heights[s, i]) for s in range(n)] + [state(heights[0, i])]
        for face in ("yf", "xf", "top"):
            vals = ";".join(s[face] for s in seq)
            b += (f'<polygon points="{seq[0][face]}" fill="{cols[face]}" stroke="#7a2e14" stroke-opacity=".25" stroke-width="1">'
                  f'<animate attributeName="points" values="{vals}" keyTimes="{";".join(f"{t:.4f}" for t in times)}" '
                  f'calcMode="spline" keySplines="{splines}" dur="{dur}s" repeatCount="indefinite"/></polygon>')
        lx, ly = iso(i + 0.47, 1.05, 0)
        b += text(lx, ly + 18, i + 1, 13, INK, 700, "middle")
    # drifting molecules above the platform
    random.seed(4)
    for k in range(14):
        sx, sy = iso(random.uniform(-0.5, 7.8), random.uniform(-1.2, 1.2), random.uniform(5, 40))
        d = random.uniform(2.5, 5)
        b += (f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{random.uniform(2.5, 4.5):.1f}" fill="{SAGE}" opacity=".0">'
              f'<animate attributeName="cy" values="{sy:.0f};{sy - 90:.0f}" dur="{d:.1f}s" begin="{k * 0.37:.2f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;.8;0" dur="{d:.1f}s" begin="{k * 0.37:.2f}s" repeatCount="indefinite"/></circle>')
    # smell name that changes
    for s, name in enumerate(names):
        t, v = window(s, n, lead=0.015)
        b += (f'<text x="850" y="120" font-size="28" fill="{ACC}" font-family="{SERIF}" font-weight="500" opacity="0">{name.title()}'
              f'{anim("opacity", v, t, dur)}</text>')
    b += text(850, 146, "average fingerprint of 60 simulated sniffs", 12, MUTED)
    # legend
    for i, (nm, _) in enumerate(sensor.CHANNEL_INFO):
        yy = 200 + i * 27
        b += f'<circle cx="862" cy="{yy - 5}" r="10" fill="{ACC}"/>' + text(862, yy - 1, i + 1, 11, "#fff", 700, "middle")
        b += text(882, yy, nm, 14, INK)
    b += text(850, 460, "SIMULATED sensors: maths plus random noise.", 12, ACC, 600)
    b += text(850, 478, "Bar heights are scaled so differences show.", 12, MUTED)
    save("anim-nose-3d.svg", svg(1160, 520, b, "Animated 3D isometric electronic nose"))


# ---------------------------------------------------------------- 3. how the smell model learns
def anim_learning():
    dur = 10
    b = text(40, 50, "How the smell model learns, animated", 26, INK, 500, family=SERIF)
    b += text(40, 76, "An illustration of the idea (the real fingerprint has 2,048 slots, this one is shrunk to fit)", 14, MUTED)

    def fade(start, end=0.95):
        return anim("opacity", [0, 0, 1, 1, 0, 0], [0, start - .001, start + .03, end - .03, end, 1], dur)

    # 1. molecule
    mx, my = 120, 190
    ring = [(mx + 38 * math.cos(math.radians(a)), my + 38 * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    g = f'<g opacity="0">{fade(0.0)}'
    g += f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in ring)}" fill="none" stroke="{SAGE}" stroke-width="4"/>'
    g += f'<line x1="{ring[0][0]}" y1="{ring[0][1]}" x2="{ring[0][0] + 34}" y2="{ring[0][1] - 18}" stroke="{SAGE}" stroke-width="4"/>'
    g += f'<line x1="{ring[3][0]}" y1="{ring[3][1]}" x2="{ring[3][0] - 34}" y2="{ring[3][1] + 12}" stroke="{SAGE}" stroke-width="4"/>'
    for (x, y), c in zip(ring, (ACC, SAGE, SAGE, ACC, SAGE, SAGE)):
        g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{c}"/>'
    g += f'<circle cx="{ring[0][0] + 34}" cy="{ring[0][1] - 18}" r="9" fill="{ACC}"/><circle cx="{ring[3][0] - 34}" cy="{ring[3][1] + 12}" r="9" fill="{ACC}"/></g>'
    b += g + text(120, 290, "1. A molecule", 15, INK, 600, "middle", SERIF) + text(120, 309, "(its shape and atoms)", 12, MUTED, anchor="middle")
    b += arrow(215, 190, 275, 190)
    # 2. fingerprint grid
    gx, gy, cs = 300, 140, 16
    random.seed(7)
    lit = set(random.sample(range(10 * 6), 17))
    b += f'<g opacity="0">{fade(0.1)}'
    for k in range(60):
        r, c = divmod(k, 10)
        if k in lit:
            t0 = 0.16 + 0.012 * sorted(lit).index(k)
            b += (f'<rect x="{gx + c * (cs + 3)}" y="{gy + r * (cs + 3)}" width="{cs}" height="{cs}" rx="4" fill="{SOFT}">'
                  f'{anim("fill", [SOFT, SOFT, ACC, ACC, SOFT, SOFT], [0, t0, t0 + .02, .93, .95, 1], dur)}</rect>')
        else:
            b += f'<rect x="{gx + c * (cs + 3)}" y="{gy + r * (cs + 3)}" width="{cs}" height="{cs}" rx="4" fill="{SOFT}"/>'
    b += "</g>" + text(gx + 95, 290, "2. Its fingerprint", 15, INK, 600, "middle", SERIF) + text(gx + 95, 309, "lit slots = fragments present", 12, MUTED, anchor="middle")
    b += arrow(515, 190, 575, 190)
    # 3. forest
    fx = 600
    b += f'<g opacity="0">{fade(0.42)}'
    for t in range(3):
        cx = fx + t * 95
        nodes = [(cx, 140), (cx - 22, 175), (cx + 22, 175), (cx - 34, 212), (cx - 10, 212), (cx + 12, 212), (cx + 34, 212)]
        for a, c in ((0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)):
            b += f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[c][0]}" y2="{nodes[c][1]}" stroke="{MUTED}" stroke-width="2"/>'
        for k, (x, y) in enumerate(nodes):
            t0 = 0.46 + t * 0.04 + k * 0.012
            b += (f'<circle cx="{x}" cy="{y}" r="7" fill="{SAGE if k < 3 else ACC}">'
                  f'{anim("r", [7, 7, 11, 7, 7], [0, t0, t0 + .02, t0 + .05, 1], dur)}</circle>')
    b += "</g>" + text(fx + 95, 290, "3. A forest of trees", 15, INK, 600, "middle", SERIF) + text(fx + 95, 309, "each tree asks yes/no questions", 12, MUTED, anchor="middle")
    b += arrow(885, 190, 945, 190)
    # 4. words
    b += text(990, 126, "4. Smell words", 15, INK, 600, "middle", SERIF)
    for k, (w, sc) in enumerate((("sweet", .62), ("vanilla", .55), ("creamy", .31))):
        y = 150 + k * 44
        t0 = 0.66 + k * 0.06
        b += (f'<g opacity="0">{anim("opacity", [0, 0, 1, 1, 0, 0], [0, t0, t0 + .03, .95, .96, 1], dur)}'
              f'<rect x="945" y="{y}" width="90" height="32" rx="16" fill="#f4e3da"/>'
              + text(990, y + 21, w, 14, "#a84e2f", 600, "middle") +
              f'<rect x="945" y="{y + 36}" width="90" height="4" rx="2" fill="{SOFT}"/><rect x="945" y="{y + 36}" width="{90 * sc:.0f}" height="4" rx="2" fill="{ACC}"/></g>')
    b += box(40, 330, 1010, 50, SOFT, SOFT)
    b += text(60, 360, "No one tells the model that certain fragments smell fruity. It works that out from ~5,000 molecules labelled by experts.", 14, INK)
    save("anim-learning.svg", svg(1090, 405, b, "Animated: how the smell model learns"))


if __name__ == "__main__":
    anim_journey()
    anim_nose_3d()
    anim_learning()
