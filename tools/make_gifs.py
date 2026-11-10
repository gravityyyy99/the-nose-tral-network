"""Makes the two GIFs used in README.md.

  docs/img/hologram.gif  a rotating 3D hologram of assets/me.png (point cloud, depth from brightness).
                         This is a Python re-creation of the idea behind the About page, not a screen capture.
  docs/img/tour.gif      an animated tour made from the real screenshots in docs/screenshots/.

Run from the project root:  python tools/make_gifs.py
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "img")
os.makedirs(OUT, exist_ok=True)
ACCENT = np.array([217, 119, 87], dtype=float)
BG_TOP, BG_BOT = np.array([34, 33, 31]), np.array([22, 21, 20])


def font(size, serif=False):
    for name in (("georgia.ttf", "times.ttf") if serif else ("segoeui.ttf", "arial.ttf")):
        for base in ("C:/Windows/Fonts/", ""):
            try:
                return ImageFont.truetype(base + name, size)
            except OSError:
                pass
    return ImageFont.load_default()


# ------------------------------------------------------------------ rotating hologram
def hologram(frames=60, w=480, h=600, ss=2):
    img = Image.open(os.path.join(ROOT, "assets", "me.png")).convert("RGBA")
    gw = 104
    gh = int(gw * img.height / img.width)
    arr = np.asarray(img.resize((gw, gh), Image.LANCZOS)).astype(float)
    rgb, alpha = arr[..., :3], arr[..., 3]
    lum = (rgb @ np.array([.299, .587, .114]) / 255) ** 0.62
    jj, ii = np.nonzero(alpha > 128)
    L = lum[jj, ii]
    cols = rgb[jj, ii] / 255
    X = (ii / (gw - 1) - .5) * 2.7
    Y = (.5 - jj / (gh - 1)) * 2.7 * (gh / gw)
    Z = (L - .42) * .95
    tint = np.clip(.5 * cols * 255 * .9 + .5 * ACCENT * (.6 + L[:, None] * 1.1), 0, 255)
    rng = np.random.default_rng(3)
    mol = np.column_stack([rng.uniform(-1.9, 1.9, 70), rng.uniform(-2.2, 2.2, 70), rng.uniform(-1.5, 1.5, 70)])
    W, H = w * ss, h * ss
    grad = np.linspace(0, 1, H)[:, None, None]
    bg = (BG_TOP * (1 - grad) + BG_BOT * grad).repeat(W, axis=1).astype(np.uint8)
    base_img = Image.fromarray(bg).convert("RGBA")
    cx, cy, D = W / 2, H * .47, 7.5
    f = 118 * ss * D
    out = []
    for t in range(frames):
        ph = t / frames
        th = 2 * math.pi * ph
        im = base_img.copy()
        # light beam
        beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(beam).polygon([(cx - 120 * ss, H * .12), (cx + 120 * ss, H * .12), (cx + 230 * ss, H * .86), (cx - 230 * ss, H * .86)], fill=(217, 119, 87, 22))
        im = Image.alpha_composite(im, beam)
        d = ImageDraw.Draw(im)
        # base rings
        for k, R in enumerate((165, 205, 250)):
            s = 1 + .05 * math.sin(2 * math.pi * ph + k)
            r = R * ss * s
            d.ellipse([cx - r, H * .86 - r * .17, cx + r, H * .86 + r * .17], outline=(217, 119, 87, 190), width=2 * ss)
        # floating molecules
        for m in mol:
            yy = ((m[1] + 2.2 + ph * 4.4 * (0.6 + (m[2] + 1.5) / 3)) % 4.4) - 2.2
            sx, sy = cx + m[0] * 118 * ss, cy - yy * 118 * ss
            d.ellipse([sx - 2 * ss, sy - 2 * ss, sx + 2 * ss, sy + 2 * ss], fill=(217, 119, 87, 150))
        # rotate and project the hologram
        xr = X * math.cos(th) + Z * math.sin(th)
        zr = -X * math.sin(th) + Z * math.cos(th)
        s = f / (D - zr)
        sx, sy = cx + xr * s, cy - Y * s
        r = (.30 + .55 * L) * .021 * s
        order = np.argsort(zr)                      # far to near
        for k in order:
            col = tuple(int(c) for c in tint[k])
            d.ellipse([sx[k] - r[k], sy[k] - r[k], sx[k] + r[k], sy[k] + r[k]], fill=col)
        # scan line
        ys = cy - math.sin(2 * math.pi * ph * 2) * (2.7 * (gh / gw) / 2) * 118 * ss
        d.line([(cx - 190 * ss, ys), (cx + 190 * ss, ys)], fill=(217, 119, 87, 150), width=2 * ss)
        d.text((24 * ss, 20 * ss), "Aroma-GPT", font=font(22 * ss, True), fill=(245, 244, 238))
        d.text((24 * ss, 50 * ss), "3D hologram, rotating", font=font(13 * ss), fill=(163, 161, 152))
        out.append(im.convert("RGB").resize((w, h), Image.LANCZOS))
    pal = [f.quantize(colors=128, method=Image.MEDIANCUT, dither=Image.NONE) for f in out]
    pal[0].save(os.path.join(OUT, "hologram.gif"), save_all=True, append_images=pal[1:], duration=55, loop=0, optimize=True, disposal=1)
    print("wrote hologram.gif", os.path.getsize(os.path.join(OUT, "hologram.gif")) // 1024, "KB")


# ------------------------------------------------------------------ tour of the site
def tour(width=760):
    shots = [("01-home.jpg", "Pick or type a smell"),
             ("02-sniff-results.jpg", "The nose and the smell model, side by side"),
             ("03-keywords.jpg", "138 smell words you can try"),
             ("04-journey.jpg", "Our journey: the build story, in motion"),
             ("05-about-hologram.jpg", "About me: a 3D hologram that reacts as you scroll"),
             ("07-documentation.jpg", "An 11-chapter documentation book"),
             ("08-coming-soon.jpg", "Coming soon: the real-hardware chapter")]
    frames, durs = [], []
    prev = None
    for n, (fn, cap) in enumerate(shots, 1):
        im = Image.open(os.path.join(ROOT, "docs", "screenshots", fn)).convert("RGB")
        im = im.resize((width, int(width * 507 / 800)), Image.LANCZOS)   # same size for every slide
        bar = Image.new("RGBA", im.size, (0, 0, 0, 0))
        bd = ImageDraw.Draw(bar)
        bh = 44
        bd.rectangle([0, im.height - bh, im.width, im.height], fill=(20, 19, 18, 215))
        bd.text((16, im.height - bh + 11), f"{n} / {len(shots)}", font=font(17, True), fill=(217, 119, 87, 255))
        bd.text((78, im.height - bh + 12), cap, font=font(16), fill=(245, 244, 238, 255))
        cur = Image.alpha_composite(im.convert("RGBA"), bar).convert("RGB")
        if prev is not None:
            for a in (.2, .4, .6, .8):
                frames.append(Image.blend(prev, cur, a)); durs.append(60)
        frames.append(cur); durs.append(1900)
        prev = cur
    pal = [f.quantize(colors=128, method=Image.MEDIANCUT, dither=Image.NONE) for f in frames]
    pal[0].save(os.path.join(OUT, "tour.gif"), save_all=True, append_images=pal[1:], duration=durs, loop=0, optimize=True, disposal=1)
    print("wrote tour.gif", os.path.getsize(os.path.join(OUT, "tour.gif")) // 1024, "KB")


if __name__ == "__main__":
    hologram()
    tour()
