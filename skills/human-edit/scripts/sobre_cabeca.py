"""Um vídeo curto sobre fundo preto (personagem, logo animado, mascote) aparecendo sobre a cabeça, sem fundo: o preto
vira transparência. Entra com um pop (como a pasta do Finder) e sai encolhendo. Sobreposição 1080x1920 (PNG em MOV)."""
import subprocess
import numpy as np
from PIL import Image

W, H, FPS = 1080, 1920, 30

def ease_out_back(p, s=1.7):
    p = min(max(p, 0), 1) - 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2

def _frames(video, n, w, h, velocidade):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", video, "-vf",
                          f"setpts=PTS/{velocidade},fps={FPS},scale={w}:{h}:flags=lanczos,tpad=stop_mode=clone:stop=-1",
                          "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    size = w * h * 3
    last = None
    for _ in range(n):
        buf = p.stdout.read(size)
        if len(buf) == size:
            last = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        yield last
    p.stdout.close()
    p.wait()

def render(n, out, video, cx, cy, largura=1000, velocidade=1.0, limiar=14, suave=36):
    """cx, cy: centro do vídeo no quadro 1080x1920. largura: largura do vídeo na tela (px).
    limiar/suave: o preto abaixo de `limiar` some; até `limiar + suave` vai ficando opaco (borda macia)."""
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                            "-of", "csv=p=0", video], capture_output=True, text=True, check=True).stdout.strip().split(",")
    vw, vh = int(probe[0]), int(probe[1])
    w = int(largura) // 2 * 2
    h = int(round(largura * vh / vw)) // 2 * 2
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", out], stdin=subprocess.PIPE)
    dur = n / FPS
    for i, rgb in enumerate(_frames(video, n, w, h, velocidade)):
        t = i / FPS
        s = ease_out_back(t / 0.22) if t < dur - 0.18 else max(0.0, 1 - ((t - (dur - 0.18)) / 0.18) ** 2)
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if rgb is not None and s > 0.02:
            a = np.clip((rgb.max(axis=2).astype(np.float32) - limiar) / suave, 0, 1)
            # a little un-premultiply so dark fringes don't halo
            col = np.clip(rgb.astype(np.float32) / np.maximum(a[..., None], 0.35), 0, 255)
            im = Image.fromarray(np.dstack([col, a * 255]).astype(np.uint8), "RGBA")
            im = im.resize((max(2, int(w * s)), max(2, int(h * s))), Image.LANCZOS)
            frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
        enc.stdin.write(frame.tobytes())
    enc.stdin.close()
    enc.wait()
    return out
