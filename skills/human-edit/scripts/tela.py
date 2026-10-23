"""Gravação de tela na faixa do split: recortes 4:3 bem fechados, com zoom/pan em keyframes suavizados.

Um plano = {"src": gravação, "t": tempo na gravação (s), "freeze": bool, "keys": [(offset_s, cx, cy, w), ...], "pop": bool}
Coordenadas em pixels da gravação; o recorte é sempre 4:3 (a proporção da faixa).
"""
import subprocess
import cv2
import numpy as np

BW, BH = 1080, 810
FPS = 30

def smooth(p):
    p = min(max(p, 0.0), 1.0)
    return p * p * p * (p * (6 * p - 15) + 10)          # smootherstep

def ease_out(p):
    p = min(max(p, 0.0), 1.0)
    return 1 - (1 - p) ** 3

def rect_at(keys, t):
    if t <= keys[0][0]:
        return keys[0][1:]
    for (ta, *a), (tb, *b) in zip(keys, keys[1:]):
        if t <= tb:
            p = smooth((t - ta) / (tb - ta)) if tb > ta else 1.0
            return tuple(x + (y - x) * p for x, y in zip(a, b))
    return keys[-1][1:]

_dims = {}
def dims(src):
    if src not in _dims:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                              "-of", "csv=p=0", src], capture_output=True, text=True, check=True).stdout.strip().split(",")
        _dims[src] = (int(out[0]), int(out[1]))
    return _dims[src]

def source_frames(src, t0, n, freeze):
    SW, SH = dims(src)
    size = SW * SH * 3
    if freeze:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", src, "-frames:v", "1",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
        f = np.frombuffer(raw[:size], np.uint8).reshape(SH, SW, 3)
        for _ in range(n):
            yield f
        return
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", src, "-vf", f"fps={FPS}",
                          "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        buf = p.stdout.read(size)
        if len(buf) == size:
            last = np.frombuffer(buf, np.uint8).reshape(SH, SW, 3)
        yield last                                       # pads with the last frame if the stream runs short
    p.stdout.close()
    p.wait()

def frame_for(f, cx, cy, w):
    SH, SW = f.shape[:2]
    h = w * BH / BW
    if w > SW:
        w, h = SW, SW * BH / BW
    if h > SH:
        h, w = SH, SH * BW / BH
    cx = min(max(cx, w / 2), SW - w / 2)
    cy = min(max(cy, h / 2), SH - h / 2)
    s = BW / w
    x0, y0 = cx - w / 2, cy - h / 2
    if s < 1:   # downscale: area-resample first so UI text doesn't alias, then sub-pixel shift
        small = cv2.resize(f, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        M = np.float32([[1, 0, -x0 * s], [0, 1, -y0 * s]])
        return cv2.warpAffine(small, M, (BW, BH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    M = np.float32([[s, 0, -s * x0], [0, s, -s * y0]])
    img = cv2.warpAffine(f, M, (BW, BH), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    if s > 1.2:  # upscaled UI text: a touch of unsharp
        img = cv2.addWeighted(img, 1.35, cv2.GaussianBlur(img, (0, 0), 1.2), -0.35, 0)
    return img

def render(shot, n, out):
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{BW}x{BH}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "12",
                            "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i, f in enumerate(source_frames(shot["src"], shot["t"], n, shot.get("freeze", False))):
        t = i / FPS
        cx, cy, w = rect_at(shot["keys"], t)
        if shot.get("pop", True):                        # quick scale-in at every cut
            w *= 1 + 0.16 * (1 - ease_out(t / 0.22))
        enc.stdin.write(np.ascontiguousarray(frame_for(f, cx, cy, w)).tobytes())
    enc.stdin.close()
    enc.wait()
    return out
