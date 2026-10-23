"""Storyboard em tela cheia (1080x1920): os quadros reais num grid que ocupa 100% da tela, 2 colunas, sem fundo
branco, sem legenda (só um fio escuro entre os quadros). Os quadros se montam um a um e o grid faz um push-in lento."""
import subprocess
import cv2
import numpy as np

W, H, FPS, SS = 1080, 1920, 30, 2
GAP = 4
BG = (10, 7, 5)                       # BGR of #05070a, the page's frame backing

def ease_out(p):
    p = min(max(p, 0.0), 1.0)
    return 1 - (1 - p) ** 3

def tiles(quadros, cols, rows):
    tw = (W * SS - (cols - 1) * GAP * SS) // cols
    th = (H * SS - (rows - 1) * GAP * SS) // rows
    out = []
    for name in quadros:
        im = cv2.imread(name)
        h, w = im.shape[:2]
        s = max(tw / w, th / h)                       # cover the cell (4:3 -> slightly wider cell: trims top/bottom)
        im = cv2.resize(im, (round(w * s), round(h * s)), interpolation=cv2.INTER_AREA)
        y0, x0 = (im.shape[0] - th) // 2, (im.shape[1] - tw) // 2
        out.append(im[y0:y0 + th, x0:x0 + tw])
    return out, tw, th

def render(n, out, quadros, cols=2, build_at=0.05, stagger=0.06, each=0.32, push=0.05):
    """quadros: image paths in reading order. Only full rows are used, so the grid always fills the frame
    (cols=2: 10 frames -> 2x5; an 11th that would sit alone is left out)."""
    rows = len(quadros) // cols
    ts, tw, th = tiles(quadros[:rows * cols], cols, rows)
    cells = [((i % cols) * (tw + GAP * SS), (i // cols) * (th + GAP * SS)) for i in range(len(ts))]
    dur = n / FPS
    built = build_at + stagger * (len(ts) - 1) + each
    full = None
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "12",
                            "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for f in range(n):
        t = f / FPS
        if t >= built and full is not None:
            canvas = full
        else:
            canvas = np.empty((H * SS, W * SS, 3), np.uint8)
            canvas[:] = BG
            for i, (tile, (x, y)) in enumerate(zip(ts, cells)):
                p = ease_out((t - build_at - stagger * i) / each)
                if p <= 0:
                    continue
                s = 1.10 - 0.10 * p                    # each tile settles into its cell from slightly bigger
                big = cv2.resize(tile, (round(tw * s), round(th * s)), interpolation=cv2.INTER_LINEAR)
                oy, ox = (big.shape[0] - th) // 2, (big.shape[1] - tw) // 2
                crop = big[oy:oy + th, ox:ox + tw].astype(np.float32)
                canvas[y:y + th, x:x + tw] = (crop * p + np.array(BG, np.float32) * (1 - p)).astype(np.uint8)
            if t >= built:
                full = canvas
        z = 1 + push * min(max(t / dur, 0), 1)         # slow push-in on the whole grid
        cw, ch = round(W * SS / z), round(H * SS / z)
        x0, y0 = (W * SS - cw) // 2, (H * SS - ch) // 2
        enc.stdin.write(cv2.resize(canvas[y0:y0 + ch, x0:x0 + cw], (W, H), interpolation=cv2.INTER_AREA).tobytes())
    enc.stdin.close()
    enc.wait()
    return out

