#!/usr/bin/env python3
"""Generate c64-skills brand images from the cbm-buddy mascot.

    python3 assets/brand/make_brand.py [--mascot path.png] [--font path.ttf]

Writes:
    plugins/c64/.claude-plugin/icon.png   1024×1024 plugin icon
    assets/brand/banner.png               1280×640 README / GitHub social preview

The look is a C64 boot screen: a light-blue border around a blue screen, using the
Pepto palette. Re-run with a higher-resolution mascot for sharper output: the
script scales whatever it is given.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
BLUE = (0x35, 0x28, 0x79)        # C64 colour 6
LIGHT_BLUE = (0x6C, 0x5E, 0xB5)  # C64 colour 14


def load_mascot(path):
    im = Image.open(path).convert("RGBA")
    return im.crop(im.getchannel("A").getbbox())


def scale_to(im, width):
    h = round(im.height * width / im.width)
    big = im.resize((width, h), Image.LANCZOS)
    # A light unsharp mask on colour only, so upscaled edges don't look mushy.
    rgb = big.convert("RGB").filter(ImageFilter.UnsharpMask(radius=3, percent=60, threshold=2))
    out = rgb.convert("RGBA")
    out.putalpha(big.getchannel("A"))
    return out


def shadow(im, blur, opacity):
    a = im.getchannel("A").point(lambda v: int(v * opacity))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(a)
    pad = blur * 3
    canvas = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    canvas.paste(sh, (pad, pad), sh)
    return canvas.filter(ImageFilter.GaussianBlur(blur)), pad


def c64_screen(w, h, border):
    img = Image.new("RGBA", (w, h), LIGHT_BLUE + (255,))
    ImageDraw.Draw(img).rectangle([border, border, w - border - 1, h - border - 1], fill=BLUE + (255,))
    return img


def place(canvas, sprite, cx, bottom):
    sh, pad = shadow(sprite, blur=max(4, sprite.width // 40), opacity=0.45)
    x = cx - sprite.width // 2
    y = bottom - sprite.height
    off = sprite.width // 60
    canvas.alpha_composite(sh, (x - pad + off, y - pad + off * 2))
    canvas.alpha_composite(sprite, (x, y))


def text(draw, xy, s, font, fill):
    draw.text(xy, s, font=font, fill=fill)


def icon(mascot, font_path, out, with_ready):
    S, B = 1024, 72
    img = c64_screen(S, S, B)
    d = ImageDraw.Draw(img)
    cell = 52  # one C64 character cell at this scale
    if with_ready:
        f = ImageFont.truetype(font_path, cell, encoding="symb")
        text(d, (B + cell // 2, B + cell // 2), "READY.", f, LIGHT_BLUE)
        cy = B + cell // 2 + cell + 6
        d.rectangle([B + cell // 2, cy, B + cell // 2 + cell - 1, cy + cell - 1], fill=LIGHT_BLUE)
        sprite = scale_to(mascot, 760)
        place(img, sprite, S // 2, S - B - 40)
    else:
        sprite = scale_to(mascot, 800)
        place(img, sprite, S // 2, S // 2 + sprite.height // 2 + 10)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, optimize=True)
    return out


def banner(mascot, font_path, out):
    W, H, B = 1280, 640, 48
    img = c64_screen(W, H, B)
    d = ImageDraw.Draw(img)
    sprite = scale_to(mascot, 470)
    place(img, sprite, B + 60 + sprite.width // 2, H - B - 70)

    x = B + 40 + sprite.width + 60
    avail = W - B - 50 - x

    def fit(s, start):
        # Largest font size (multiple of 2) that keeps `s` inside the screen area.
        size = start
        while size > 10:
            f = ImageFont.truetype(font_path, size, encoding="symb")
            if d.textlength(s, font=f) <= avail:
                return f
            size -= 2
        return f

    title = "C64-SKILLS"
    lines = ["AI-ASSISTED", "COMMODORE 64 DEVELOPMENT", "", "BUILD. RUN. SEE IT WORK."]
    big = fit(title, 80)
    small = fit(max(lines, key=len), 30)
    text(d, (x, 165), title, big, (255, 255, 255))
    step = int(small.size * 1.45)
    y = 165 + big.size + 50
    for line in lines:
        text(d, (x, y), line, small, LIGHT_BLUE)
        y += step
    text(d, (x, y + step // 2), "READY.", small, LIGHT_BLUE)
    cy = y + step // 2 + step
    d.rectangle([x, cy, x + small.size - 1, cy + small.size - 1], fill=LIGHT_BLUE)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, optimize=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mascot", default=str(ROOT / "assets/brand/cbm-buddy.png"))
    ap.add_argument("--font", default=str(ROOT / "assets/brand/Commodore-64-v6.3.TTF"))
    ap.add_argument("--variant", choices=["plain", "ready"], default="plain")
    ap.add_argument("--icon-out", default=str(ROOT / "plugins/c64/.claude-plugin/icon.png"))
    ap.add_argument("--banner-out", default=str(ROOT / "assets/brand/banner.png"))
    a = ap.parse_args()
    m = load_mascot(a.mascot)
    print(icon(m, a.font, Path(a.icon_out), a.variant == "ready"))
    print(banner(m, a.font, Path(a.banner_out)))


if __name__ == "__main__":
    main()
