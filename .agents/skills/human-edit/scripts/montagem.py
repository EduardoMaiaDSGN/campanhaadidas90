"""Montagem rápida dos inserts (3 cortes/s): faixa 4:3 do split ou tela cheia 9:16."""
import json, os, subprocess, sys
import numpy as np

FPS, CUT = 30, 10                       # 10 frames per cut = 3 cuts per second
BW, BH = 1080, 810                       # 4:3 band

def gray_frames(f, a, b):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(a,0):.3f}", "-i", f, "-t", f"{b-a:.3f}",
                          "-vf", f"fps={FPS},scale=96:54", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 54, 96).astype(np.float32)

def best_start(f, t, search=0.15):
    """Most animated 10-frame window near t that doesn't straddle a hard cut."""
    a = max(t - search, 0)
    fr = gray_frames(f, a, t + search + CUT / FPS + 0.1)
    if len(fr) < CUT + 2:
        return t
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    cut = d > max(25, 6 * np.median(d) + 1e-3)
    best, bi = -1, 0
    for i in range(0, len(d) - CUT + 1):
        if cut[max(i - 2, 0):i + CUT].any():
            continue
        s = d[i:i + CUT - 1].mean()
        if s > best:
            best, bi = s, i
    return a + bi / FPS

def vf(mode):
    if mode and mode[0] == "fit":
        return (f"fps={FPS},split[a][b];[a]scale={BW}:{BH}:force_original_aspect_ratio=increase,crop={BW}:{BH},"
                f"gblur=sigma=40[bg];[b]scale={BW}:-2:flags=lanczos,unsharp=5:5:0.6[fg];"
                f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,format=yuv420p")
    return (f"fps={FPS},scale={BW}:{BH}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={BW}:{BH},unsharp=5:5:0.6,setsar=1,format=yuv420p")

_dims = {}
def vertical(f):
    if f not in _dims:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                              "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip().split(",")
        _dims[f] = (int(out[0]), int(out[1]))
    w, h = _dims[f]
    return h > w

def vf_full(f):
    if vertical(f):
        return (f"fps={FPS},scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,"
                f"unsharp=5:5:0.6,setsar=1,format=yuv420p")
    return (f"fps={FPS},split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"gblur=sigma=60,eq=brightness=-0.06:saturation=1.15[bg];[b]scale=1080:-2:flags=lanczos,unsharp=5:5:0.6[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,format=yuv420p")

def build(n_frames, out, picks, work="montage_parts", first=0, full=False):
    """picks: [(video path, approx time s[, "fit"]), ...]; cut k uses picks[(first + k) % len(picks)]."""
    os.makedirs(work, exist_ok=True)
    lens = [CUT] * (n_frames // CUT)
    rest = n_frames % CUT
    if rest >= 6 or not lens:
        lens.append(rest)
    else:
        lens[-1] += rest                # never end on a 1-5 frame flash
    parts = []
    for k, frames in enumerate(lens):
        f, t, *mode = picks[(first + k) % len(picks)]
        s = best_start(f, t)
        p = f"{work}/{k:02d}.mov"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-i", f, "-an",
                        "-vf", vf_full(f) if full else vf(mode),
                        "-frames:v", str(frames), "-c:v", "libx264", "-preset", "fast", "-crf", "12", p], check=True)
        parts.append(p)
        print(f"  cut {k:02d} {os.path.basename(f)[:24]:<24} t={s:6.2f}s ({frames}f)")
    with open(f"{work}/list.txt", "w") as fh:
        fh.writelines(f"file '{os.path.basename(p)}'\n" for p in parts)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/list.txt",
                    "-c", "copy", out], check=True)
    return out
