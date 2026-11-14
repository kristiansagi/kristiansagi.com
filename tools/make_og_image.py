"""Builds static/og/home-1200x630.jpg — the share image used when kristiansagi.com
is posted on LinkedIn, X, Slack etc. Apple-style: light grey, round portrait, Inter.

    python tools/make_og_image.py      (needs Pillow)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "resume" / "fonts"
OUT = ROOT / "static" / "og" / "home-1200x630.jpg"
PHOTO = ROOT / "static" / "kristian-sagi-profile-suit1.webp"

W, H, SS = 1200, 630, 2                      # render at 2x, then downscale for crisp edges
BG, INK, MUTED, BLUE = "#f5f5f7", "#1d1d1f", "#6e6e73", "#0066cc"

def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size * SS)

img = Image.new("RGB", (W * SS, H * SS), BG)
d = ImageDraw.Draw(img)

# Round portrait, left
D = 300 * SS
photo = Image.open(PHOTO).convert("RGB").resize((D, D), Image.LANCZOS)
mask = Image.new("L", (D, D), 0)
ImageDraw.Draw(mask).ellipse((0, 0, D - 1, D - 1), fill=255)
px, py = 120 * SS, (H * SS - D) // 2
img.paste(photo, (px, py), mask)

# Text, right
x = px + D + 70 * SS
lines = [
    ("Kristian Sägi", font("InterDisplay-SemiBold.ttf", 72), INK, 0),
    ("Engineering leader. CEO of Entringo.", font("Inter-Regular.ttf", 32), INK, 22),
    ("Building resilient companies,", font("Inter-Regular.ttf", 28), MUTED, 26),
    ("teams and systems.", font("Inter-Regular.ttf", 28), MUTED, 6),
    ("kristiansagi.com", font("Inter-Medium.ttf", 24), BLUE, 34),
]
heights = [f.getbbox(t)[3] for t, f, _, _ in lines]
total = sum(heights) + sum(gap * SS for *_, gap in lines)
y = (H * SS - total) // 2
for (text, f, color, gap), h in zip(lines, heights):
    y += gap * SS
    d.text((x, y), text, font=f, fill=color)
    y += h

img = img.resize((W, H), Image.LANCZOS)
OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "JPEG", quality=90, optimize=True, progressive=True)
print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
