#!/usr/bin/env python3
"""
Wallpaper Generator — Phone-Ready, High Variation Each Run

Usage:
  python wallpaper_generator.py [--w 1170] [--h 2532] [--seed 123] [--outdir output]

Requires: Pillow (PIL), numpy (optional but recommended)
"""
import math
import os
import random
import argparse
from datetime import datetime

try:
    import numpy as np
except Exception:
    np = None

from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance

# ---------------------------
# Utilities
# ---------------------------

def clamp(x, a=0, b=255):
    return max(a, min(b, int(x)))

def lerp(a, b, t):
    return a + (b - a) * t

def hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join([c*2 for c in h])
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def choose_palette():
    # Hand-picked palettes with contrast + harmony
    palettes = [
        ["#0f0f1a","#1b1f3b","#533a71","#a88fac","#ffd6e0"],
        ["#0b1d26","#1b263b","#415a77","#778da9","#e0e1dd"],
        ["#0a0908","#22333b","#eae0d5","#c6ac8f","#5e503f"],
        ["#0f2027","#203a43","#2c5364","#f5f7fa","#c3cfe2"],
        ["#1e152a","#23395b","#406e8e","#8ea8c3","#cbf7ed"],
        ["#1b1b3a","#693668","#a74482","#f84aa7","#ff3562"],
        ["#051923","#003554","#006494","#0582ca","#00a6fb"],
        ["#2f1b41","#87255b","#a8dadc","#f1faee","#457b9d"],
        ["#141414","#292929","#fca311","#e5e5e5","#14213d"],
        ["#0f0f0f","#2d6a4f","#40916c","#95d5b2","#d8f3dc"],
        ["#1b262c","#0f4c75","#3282b8","#bbe1fa","#f7f7ff"],
        ["#1d1e22","#2c2e33","#3f4147","#ffd166","#ef476f"],
    ]
    p = random.choice(palettes)
    random.shuffle(p)
    return list(map(hex_to_rgb, p))

def random_phone_size():
    common = [(1170,2532),(1242,2688),(1440,3200),(1080,2400),(1290,2796),(1440,2560)]
    return random.choice(common)

def save_image(img, outdir):
    os.makedirs(outdir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(outdir, f"wallpaper_{ts}.png")
    img.save(path, "PNG", optimize=True)
    print(f"Saved: {path}")

# ---------------------------
# Backgrounds
# ---------------------------

def bg_linear_gradient(size, c1, c2, angle_deg=None):
    w, h = size
    if angle_deg is None:
        angle_deg = random.uniform(0, 360)
    angle = math.radians(angle_deg)
    # Create coordinates grid with numpy if available (faster & smoother)
    if np is not None:
        x = np.linspace(-0.5, 0.5, w)
        y = np.linspace(-0.5, 0.5, h)
        X, Y = np.meshgrid(x, y)
        t = (np.cos(angle) * X + np.sin(angle) * Y)
        t = (t - t.min()) / (t.max() - t.min() + 1e-8)
        r = (1 - t) * c1[0] + t * c2[0]
        g = (1 - t) * c1[1] + t * c2[1]
        b = (1 - t) * c1[2] + t * c2[2]
        arr = np.dstack([r, g, b]).astype(np.uint8)
        return Image.fromarray(arr, mode="RGB")
    else:
        # Fallback: draw lines
        img = Image.new("RGB", size, c1)
        draw = ImageDraw.Draw(img)
        steps = max(w, h)
        for i in range(steps):
            t = i / (steps - 1)
            col = tuple(clamp(lerp(c1[j], c2[j], t)) for j in range(3))
            # Map i to line along angle by blending rectangles (approx)
            if w >= h:
                draw.line([(i,0),(i,h)], fill=col)
            else:
                draw.line([(0,i),(w,i)], fill=col)
        if angle_deg not in (0, 90, 180, 270):
            img = img.rotate(angle_deg, resample=Image.BICUBIC, expand=False)
        return img

def bg_radial_gradient(size, inner, outer):
    w, h = size
    cx, cy = w/2, h/2
    max_r = math.hypot(w, h)/2
    if np is not None:
        y, x = np.ogrid[:h, :w]
        dist = np.sqrt((x - cx)**2 + (y - cy)**2)
        t = (dist / max_r).clip(0, 1)
        r = (1 - t) * inner[0] + t * outer[0]
        g = (1 - t) * inner[1] + t * outer[1]
        b = (1 - t) * inner[2] + t * outer[2]
        arr = np.dstack([r, g, b]).astype(np.uint8)
        return Image.fromarray(arr, "RGB")
    else:
        img = Image.new("RGB", size, outer)
        mask = Image.new("L", size, 0)
        mdraw = ImageDraw.Draw(mask)
        for i in range(512, -1, -1):
            r = int(max_r * i / 512)
            alpha = int(255 * (1 - i / 512))
            mdraw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=alpha)
        fg = Image.new("RGB", size, inner)
        return Image.composite(fg, img, mask)

def add_paper_texture(img, strength=0.08):
    w, h = img.size
    noise = Image.effect_noise((w, h), 100)
    noise = noise.filter(ImageFilter.GaussianBlur(radius=1.2))
    # Normalize and blend
    if strength > 0:
        noise = ImageEnhance.Contrast(noise).enhance(1.2)
        noise = ImageEnhance.Brightness(noise).enhance(1.05)
        noise_rgb = Image.merge("RGB", (noise, noise, noise))
        img = ImageChops.blend(img, noise_rgb, strength)
    return img

# ---------------------------
# Pattern generators (overlay layers)
# ---------------------------

def pattern_scatter_circles(size, palette):
    w, h = size
    layer = Image.new("RGBA", size, (0,0,0,0))
    draw = ImageDraw.Draw(layer, "RGBA")
    n = random.randint(120, 260)
    for _ in range(n):
        r = random.uniform(min(w,h)*0.005, min(w,h)*0.08)
        x = random.uniform(-r, w + r)
        y = random.uniform(-r, h + r)
        c = random.choice(palette)
        a = random.randint(40, 140)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(c[0], c[1], c[2], a))
    return layer

def pattern_stripes(size, palette):
    w, h = size
    layer = Image.new("RGBA", size, (0,0,0,0))
    draw = ImageDraw.Draw(layer, "RGBA")
    angle = random.uniform(10, 80)
    spacing = random.randint(int(min(w,h)*0.02), int(min(w,h)*0.06))
    thickness = random.randint(max(2, spacing//4), spacing)
    c = random.choice(palette)
    col = (c[0], c[1], c[2], random.randint(40,110))
    # Draw stripes by sweeping across a rotated canvas
    diag = int(math.hypot(w,h))
    tmp = Image.new("RGBA", (diag, diag), (0,0,0,0))
    tdraw = ImageDraw.Draw(tmp, "RGBA")
    for x in range(0, diag+spacing, spacing):
        tdraw.rectangle([x, 0, x+thickness, diag], fill=col)
    tmp = tmp.rotate(angle, resample=Image.BICUBIC, expand=True)
    # Center crop onto layer
    x0 = (tmp.width - w)//2
    y0 = (tmp.height - h)//2
    layer = tmp.crop((x0, y0, x0+w, y0+h))
    return layer

def pattern_concentric(size, palette):
    w, h = size
    cx, cy = w/2, h/2
    layer = Image.new("RGBA", size, (0,0,0,0))
    draw = ImageDraw.Draw(layer, "RGBA")
    rings = random.randint(8, 20)
    max_r = math.hypot(w, h)/2
    for i in range(rings):
        t = i / (rings - 1 + 1e-6)
        r = lerp(max_r*0.05, max_r, t)
        c = random.choice(palette)
        a = random.randint(30, 120)
        thick = random.uniform(max_r*0.005, max_r*0.03)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(c[0], c[1], c[2], a), width=int(max(1, thick)))
    return layer

def pattern_triangles(size, palette):
    w, h = size
    layer = Image.new("RGBA", size, (0,0,0,0))
    draw = ImageDraw.Draw(layer, "RGBA")
    gx = random.randint(6, 14)
    gy = random.randint(10, 20)
    sx, sy = w / gx, h / gy
    jitter = 0.4
    points = []
    for iy in range(gy + 1):
        row = []
        for ix in range(gx + 1):
            jx = (random.uniform(-jitter, jitter) * sx)
            jy = (random.uniform(-jitter, jitter) * sy)
            row.append((ix*sx + jx, iy*sy + jy))
        points.append(row)
    # Triangulate grid cells into two triangles each
    for iy in range(gy):
        for ix in range(gx):
            p00 = points[iy][ix]
            p10 = points[iy][ix+1]
            p01 = points[iy+1][ix]
            p11 = points[iy+1][ix+1]
            tri1 = [p00, p10, p11]
            tri2 = [p00, p01, p11]
            for tri in (tri1, tri2):
                c = random.choice(palette)
                a = random.randint(40, 120)
                draw.polygon(tri, fill=(c[0], c[1], c[2], a))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 1.8)))
    return layer

def pattern_waves(size, palette):
    w, h = size
    layer = Image.new("RGBA", size, (0,0,0,0))
    draw = ImageDraw.Draw(layer, "RGBA")
    lines = random.randint(6, 14)
    amp = random.uniform(h*0.02, h*0.08)
    freq = random.uniform(1.0, 3.5)
    thickness = random.randint(2, 6)
    for i in range(lines):
        phase = random.uniform(0, math.pi*2)
        c = random.choice(palette)
        a = random.randint(60, 160)
        y0 = int(lerp(h*0.1, h*0.9, i/(lines-1 + 1e-6)))
        pts = []
        for x in range(-w//10, w + w//10, max(2, w//300)):
            y = y0 + math.sin((x / w) * math.pi * 2 * freq + phase) * amp
            pts.append((x, y))
        draw.line(pts, fill=(c[0], c[1], c[2], a), width=thickness, joint="curve")
    return layer

def pattern_soft_blobs(size, palette):
    w, h = size
    layer = Image.new("RGBA", size, (0,0,0,0))
    blobs = random.randint(6, 16)
    for _ in range(blobs):
        r = random.uniform(min(w,h)*0.08, min(w,h)*0.25)
        x = random.uniform(r*0.8, w - r*0.8)
        y = random.uniform(r*0.8, h - r*0.8)
        c = random.choice(palette)
        a = random.randint(80, 160)
        blob = Image.new("RGBA", (int(r*2.5), int(r*2.5)), (0,0,0,0))
        bdraw = ImageDraw.Draw(blob, "RGBA")
        bdraw.ellipse([0,0,blob.width,blob.height], fill=(c[0], c[1], c[2], a))
        blob = blob.filter(ImageFilter.GaussianBlur(radius=r*0.35))
        layer.alpha_composite(blob, (int(x - blob.width/2), int(y - blob.height/2)))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=random.uniform(1.0, 2.5)))
    return layer

def pattern_dots(size, palette):
    w, h = size
    layer = Image.new("RGBA", size, (0,0,0,0))
    draw = ImageDraw.Draw(layer, "RGBA")
    spacing = random.randint(int(min(w,h)*0.02), int(min(w,h)*0.05))
    r = max(1, spacing//4)
    offset = random.choice([0, spacing//2])
    for y in range(0, h+spacing, spacing):
        for x in range(offset, w+spacing, spacing):
            c = random.choice(palette)
            a = random.randint(40, 140)
            draw.ellipse([x-r, y-r, x+r, y+r], fill=(c[0], c[1], c[2], a))
    return layer

def subtle_vignette(img, strength=0.25):
    w, h = img.size
    vignette = bg_radial_gradient((w,h), (0,0,0), (0,0,0))
    mask = Image.new("L", (w,h), 0)
    # Create mask where edges are darker
    m = Image.new("L", (w,h), 0)
    md = ImageDraw.Draw(m)
    md.rectangle([0,0,w,h], fill=255)
    blur = int(min(w,h)*0.08)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=blur))
    # Blend by multiplying with a factor
    dark = Image.new("RGB", (w,h), (0,0,0))
    return Image.blend(img, ImageChops.multiply(img, ImageEnhance.Brightness(vignette).enhance(1.5)), strength)

def add_grain(img, amount=0.06):
    if amount <= 0:
        return img
    w, h = img.size
    noise = Image.effect_noise((w, h), random.randint(40, 90))
    noise = ImageEnhance.Contrast(noise).enhance(1.4)
    noise = ImageEnhance.Brightness(noise).enhance(1.0)
    noise_rgb = Image.merge("RGB", (noise, noise, noise))
    return ImageChops.blend(img, noise_rgb, amount)

# ---------------------------
# Composer
# ---------------------------

def compose_wallpaper(size=None, seed=None):
    if seed is not None:
        random.seed(seed)
        if np is not None:
            np.random.seed(seed)

    if size is None:
        size = random_phone_size()
    w, h = size

    palette = choose_palette()
    bg_choice = random.choice(["linear","radial"])
    if bg_choice == "linear":
        bg = bg_linear_gradient(size, random.choice(palette), random.choice(palette), angle_deg=random.uniform(0,360))
    else:
        bg = bg_radial_gradient(size, random.choice(palette), random.choice(palette))

    bg = add_paper_texture(bg, strength=random.uniform(0.04, 0.12))

    # Choose 2–4 patterns from the set
    patterns = [
        pattern_scatter_circles,
        pattern_stripes,
        pattern_concentric,
        pattern_triangles,
        pattern_waves,
        pattern_soft_blobs,
        pattern_dots,
    ]
    random.shuffle(patterns)
    n_layers = random.randint(2, 4)
    comp = bg.convert("RGBA")

    for i in range(n_layers):
        pat_func = patterns[i]
        layer = pat_func((w,h), palette)
        # Random blend mode
        mode = random.choice(["normal","multiply","screen","overlay","softlight","add","subtract"])
        opacity = random.uniform(0.25, 0.85)

        if mode == "normal":
            base = comp
            comp = Image.alpha_composite(base, Image.blend(Image.new("RGBA",(w,h),(0,0,0,0)), layer, opacity))
        else:
            # Convert to RGB for blend ops then reattach alpha
            base_rgb = comp.convert("RGB")
            lay_rgb = layer.convert("RGB")
            if mode == "multiply":
                blended = ImageChops.multiply(base_rgb, lay_rgb)
            elif mode == "screen":
                blended = ImageChops.screen(base_rgb, lay_rgb)
            elif mode == "overlay":
                blended = ImageChops.overlay(base_rgb, lay_rgb)
            elif mode == "softlight":
                blended = ImageChops.soft_light(base_rgb, lay_rgb)
            elif mode == "add":
                blended = ImageChops.add(base_rgb, lay_rgb, scale=1.0, offset=0)
            elif mode == "subtract":
                blended = ImageChops.subtract(base_rgb, lay_rgb, scale=1.0, offset=0)
            else:
                blended = base_rgb

            blended = ImageChops.blend(base_rgb, blended, opacity)
            comp = Image.merge("RGBA", (*blended.split(), comp.split()[-1]))

        # Occasionally soften the layer transitions
        if random.random() < 0.5:
            comp = comp.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.2, 0.8)))

    out = comp.convert("RGB")
    # Post FX
    if random.random() < 0.9:
        out = add_grain(out, amount=random.uniform(0.03, 0.08))
    if random.random() < 0.7:
        out = subtle_vignette(out, strength=random.uniform(0.08, 0.2))
    # Slight contrast pop
    out = ImageEnhance.Contrast(out).enhance(random.uniform(1.02, 1.12))
    out = ImageEnhance.Color(out).enhance(random.uniform(1.02, 1.15))
    return out

# ---------------------------
# Main
# ---------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--w", type=int, default=None, help="Width (pixels)")
    parser.add_argument("--h", type=int, default=None, help="Height (pixels)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--outdir", type=str, default="output_wallpapers", help="Output directory")
    args = parser.parse_args()

    size = None
    if args.w and args.h:
        size = (args.w, args.h)

    img = compose_wallpaper(size=size, seed=args.seed)
    save_image(img, args.outdir)

if __name__ == "__main__":
    main()
