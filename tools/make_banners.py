"""Profile banners for LinkedIn (1584x396) and X (1500x500), in the same style as the site:
light grey, Inter, text on the right so the profile photo (bottom left) never covers it.

    python tools/make_banners.py      (needs Pillow; writes to ../banners/)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "resume" / "fonts"
OUT = ROOT.parent / "banners"
BG, INK, BLUE = "#f5f5f7", "#1d1d1f", "#0066cc"
SS = 2

def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size * SS)

def banner(w, h, name, size1, size2, right):
    img = Image.new("RGB", (w * SS, h * SS), BG)
    d = ImageDraw.Draw(img)
    lines = [("Engineering leader. CEO of Entringo.", font("Inter-Regular.ttf", size1), INK, 0),
             ("kristiansagi.com", font("Inter-Medium.ttf", size2), BLUE, int(size1 * 0.55))]
    hs = [f.getbbox(t)[3] for t, f, _, _ in lines]
    total = sum(hs) + sum(g * SS for *_, g in lines)
    y = (h * SS - total) // 2
    for (t, f, c, g), hh in zip(lines, hs):
        y += g * SS
        x = w * SS - right * SS - d.textlength(t, font=f)
        d.text((x, y), t, font=f, fill=c)
        y += hh
    OUT.mkdir(exist_ok=True)
    img.resize((w, h), Image.LANCZOS).save(OUT / name, quality=95)
    print("Wrote", OUT / name)

banner(1584, 396, "kristian-sagi-linkedin-1584x396.jpg", 34, 26, 150)
banner(1500, 500, "kristian-sagi-x-1500x500.jpg", 36, 28, 130)

# Plain versions (no text), like the banners of most Apple and Google leaders
for w, h, name in [(1584, 396, "kristian-sagi-linkedin-plain-1584x396.jpg"), (1500, 500, "kristian-sagi-x-plain-1500x500.jpg")]:
    Image.new("RGB", (w, h), BG).save(OUT / name, quality=95)
    print("Wrote", OUT / name)
