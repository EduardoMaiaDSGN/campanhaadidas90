"""Pasta azul do Finder (macOS) que aparece sobre a cabeça e some, com o nome embaixo como no Mac.
Sobreposição transparente 1080x1920 (PNG em MOV). Serve para ilustrar uma skill, um projeto, um arquivo."""
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS, SS = 1080, 1920, 30, 3

def ease_out_back(p, s=1.7):
    p = min(max(p, 0), 1) - 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2

def vgrad(w, h, top, bot):
    t = np.linspace(0, 1, h)[:, None, None]
    g = np.array(top)[None, None, :] * (1 - t) + np.array(bot)[None, None, :] * t
    a = np.full((h, w, 1), 255)
    return Image.fromarray(np.concatenate([np.repeat(g, w, axis=1), np.repeat(a, 1, axis=1).repeat(w, axis=1)[:, :w]], axis=2).astype(np.uint8), "RGBA")

def folder_icon(w):
    """Big Sur/Sonoma Finder folder, w px wide (drawn at SS and downsampled)."""
    fw, fh = w * SS, int(w * 0.80) * SS
    pad = int(fw * 0.08)
    img = Image.new("RGBA", (fw + 2 * pad, fh + 2 * pad), (0, 0, 0, 0))
    r = int(fw * 0.055)
    # shadow
    sh = Image.new("L", img.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle([pad, pad + int(fh * 0.14) + int(fh * 0.03), pad + fw, pad + fh + int(fh * 0.03)], r, fill=110)
    img.putalpha(sh.filter(ImageFilter.GaussianBlur(fw * 0.025)))
    img = Image.merge("RGBA", (Image.new("L", img.size, 0),) * 3 + (img.getchannel("A"),))
    # back + tab (tab with a soft slanted shoulder)
    back = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(back)
    d.rounded_rectangle([pad, pad + int(fh * 0.10), pad + fw, pad + fh], r, fill=255)
    tw, th = int(fw * 0.38), int(fh * 0.16)
    d.rounded_rectangle([pad, pad, pad + tw, pad + th + r], r, fill=255)
    d.polygon([(pad + tw - r, pad), (pad + tw + int(fw * 0.07), pad + int(fh * 0.10)), (pad + tw - r, pad + int(fh * 0.10))], fill=255)
    back = back.filter(ImageFilter.GaussianBlur(SS * 0.6))
    img.paste(vgrad(img.width, img.height, (64, 158, 232), (38, 128, 214)), (0, 0), back)
    # front panel
    front = Image.new("L", img.size, 0)
    fy0 = pad + int(fh * 0.22)
    ImageDraw.Draw(front).rounded_rectangle([pad, fy0, pad + fw, pad + fh], r, fill=255)
    img.paste(vgrad(img.width, img.height, (128, 206, 252), (82, 172, 242)), (0, 0), front)
    # crisp light edge along the front panel's top
    ImageDraw.Draw(img).line([(pad + r * 0.6, fy0 + SS), (pad + fw - r * 0.6, fy0 + SS)], fill=(196, 234, 255, 255), width=max(SS, 2))
    return img.resize((img.width // SS, img.height // SS), Image.LANCZOS)

from PIL import ImageFont

def with_label(icon, text, size_px):
    """Finder/desktop-style label under the icon: white SF Pro, soft dark shadow."""
    f = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", size_px * SS)
    f.set_variation_by_name("Medium")
    tw = f.getbbox(text)[2]
    lw, lh = max(icon.width * SS, tw + 40 * SS), int(size_px * 1.8) * SS
    lab = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    sh = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((lw // 2, lh // 2 + SS * 2), text, font=f, fill=(0, 0, 0, 230), anchor="mm")
    lab.alpha_composite(sh.filter(ImageFilter.GaussianBlur(SS * 3)))
    ImageDraw.Draw(lab).text((lw // 2, lh // 2), text, font=f, fill=(255, 255, 255, 255), anchor="mm")
    lab = lab.resize((lw // SS, lh // SS), Image.LANCZOS)
    out = Image.new("RGBA", (max(icon.width, lab.width), icon.height + lab.height - int(icon.height * 0.06)), (0, 0, 0, 0))
    out.alpha_composite(icon, ((out.width - icon.width) // 2, 0))
    out.alpha_composite(lab, ((out.width - lab.width) // 2, icon.height - int(icon.height * 0.06)))
    return out

def render(n, out, cx, cy, size=330, rotulo=None):
    """cx, cy: where the folder centre sits on the 1080x1920 canvas. rotulo: Finder-style name under it."""
    icon = folder_icon(size)
    if rotulo:
        icon = with_label(icon, rotulo, int(size * 0.13))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", out], stdin=subprocess.PIPE)
    dur = n / FPS
    for i in range(n):
        t = i / FPS
        s = ease_out_back(t / 0.22) if t < dur - 0.18 else max(0.0, 1 - ((t - (dur - 0.18)) / 0.18) ** 2) * 1.0
        alpha = 1.0 if t < dur - 0.18 else max(0.0, 1 - (t - (dur - 0.18)) / 0.18)
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if s > 0.02:
            ic = icon.resize((max(2, int(icon.width * s)), max(2, int(icon.height * s))), Image.LANCZOS)
            if alpha < 1:
                ic.putalpha(ic.getchannel("A").point(lambda v: int(v * alpha)))
            float_y = int(-10 * min(t / dur, 1))
            frame.alpha_composite(ic, (int(cx - ic.width / 2), int(cy - ic.height / 2 + float_y)))
        enc.stdin.write(frame.tobytes())
    enc.stdin.close()
    enc.wait()
    return out

