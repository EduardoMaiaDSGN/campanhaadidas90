"""Lettering de CTA no topo, no estilo aprovado: discreto. Branco, peso só um toque acima do Regular, sem caixa, sem
sombra, linhas do mesmo tamanho, centralizado, entra no corte (sem fade). Se o fundo atrás for claro, um escurecido
bem leve no topo do quadro (degradê, não sombra na letra) mantém a leitura."""
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, SS = 1080, 1920, 30, 2
FONT = "/System/Library/Fonts/SFNS.ttf"

def ease_out(p):
    p = min(max(p, 0), 1)
    return 1 - (1 - p) ** 3

def lettering(lines, size=52, lh=1.22, peso=470):
    f = ImageFont.truetype(FONT, size * SS)
    f.set_variation_by_axes([100, 28, 400, peso])  # width, optical size, grade, weight: 470 = a touch above Regular (400); Medium is 510
    asc = int(size * SS * 0.95)
    cw = max(f.getbbox(t, anchor="ls")[2] for t in lines) + 8 * SS
    ch = asc + int(size * SS * lh) * (len(lines) - 1) + int(size * SS * 0.3)
    im = Image.new("RGBA", (cw, ch), (255, 255, 255, 0))
    d = ImageDraw.Draw(im)
    for i, t in enumerate(lines):
        d.text((cw // 2, asc + i * int(size * SS * lh)), t, font=f, fill=(255, 255, 255, 255), anchor="ms")
    return im.resize((cw // SS, ch // SS), Image.LANCZOS), asc // SS

def top_dim(a0=0.13, y0=240, y1=640):    # 0.42 read as "sombra muito forte"
    """per-row alpha of the black dim: a0 down to y0, smoothstep to 0 at y1"""
    p = np.clip((np.arange(H, dtype=float) - y0) / (y1 - y0), 0, 1)
    return a0 * (1 - p * p * (3 - 2 * p))

def render(out, dur, linhas, base=290, size=52, peso=470, escurecer=0.13):
    """linhas: the CTA lines (same size). base: baseline of the first line. escurecer: top dim alpha (0 = none)."""
    card, asc = lettering(linhas, size=size, peso=peso)
    dim = top_dim(escurecer)
    n = round(dur * FPS)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", out], stdin=subprocess.PIPE)
    last = None
    for i in range(n):
        t = i / FPS
        p = q = 1.0                              # user: no fade in, the lettering (and its dim) just cut in
        if p >= 1 and q >= 1 and last is not None:
            enc.stdin.write(last)
            continue
        a = np.zeros((H, W, 4), np.uint8)
        a[..., 3] = (dim * q * 255).astype(np.uint8)[:, None]
        frame = Image.fromarray(a, "RGBA")
        c = card.copy()
        if p < 1:
            c.putalpha(c.getchannel("A").point(lambda v: int(v * p)))
        frame.alpha_composite(c, (W // 2 - c.width // 2, int(base - asc + (1 - p) * 8)))
        last = frame.tobytes()
        enc.stdin.write(last)
    enc.stdin.close()
    enc.wait()
    return out

