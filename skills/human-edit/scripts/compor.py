"""Compositor: EDL -> vídeo vertical final (clipes, faixa do split, telas cheias, grade de cor).

1. per clip: face-centred punch-in crop, exact frame count, de-clicked audio
2. concat clips (stream copy)
3. optional split-screen composite over the opening (montage band on top)
4. light grade + audio master (HPF, light denoise, comp, 2-pass loudnorm -14 LUFS) + H.264
"""
import json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
import cv2
import numpy as np

W, H = 1080, 1920
SCALE = {"wide": 1.0, "punch": 1.18, "close": 1.38}
FACE_Y = 0.42                     # face centre sits at this height of a cropped frame
GRADE = "eq=contrast=1.06:brightness=-0.008:saturation=1.04,vignette=angle=PI/6"
ACHAIN = "highpass=f=75,afftdn=nf=-30:nr=8,acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=2"

FACES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "faces")   # Apple Vision face detector (faces.swift)

def run(cmd):
    subprocess.run(cmd, check=True)

def vision_faces(video, times, tag):
    """Face centres (cx, cy in 1080x1920 px) at the given times, via Apple Vision; None where no face."""
    d = tempfile.mkdtemp(prefix=f"faces_{tag}_", dir=".")
    paths = []
    for i, t in enumerate(times):
        p = f"{d}/{i:02d}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                        "-vf", "scale=540:960", p], check=True)
        paths.append(p)
    out = subprocess.run([FACES, *paths], capture_output=True, text=True, check=True).stdout.split("\n")
    res = []
    for line in out:
        parts = line.split()
        if len(parts) == 5:
            res.append((2 * float(parts[1]), 2 * float(parts[2]), 2 * float(parts[4])))
    shutil.rmtree(d, ignore_errors=True)
    return res

def face_center(src, t0, t1, tag="src"):
    pts = vision_faces(src, np.linspace(t0 + 0.1, t1 - 0.1, 4), tag)
    if not pts:
        return W * 0.45, H * 0.5
    return tuple(np.median(np.array(pts)[:, :2], axis=0))

def crop_for(zoom, fc):
    s = SCALE[zoom]
    if s == 1.0:
        return None
    cw, ch = int(W / s) // 2 * 2, int(H / s) // 2 * 2
    x = int(np.clip(fc[0] - cw / 2, 0, W - cw))
    y = int(np.clip(fc[1] - FACE_Y * ch, 0, H - ch))
    return cw, ch, x, y

def face_y(video, t0, t1, n=7):
    """(highest face-centre y = 10th percentile, median face-box height) of a framed clip in the assembled
    timeline, canvas px. Placing by the highest point keeps the cap clear of the band when the head moves up."""
    pts = vision_faces(video, np.linspace(t0 + 0.06, t1 - 0.06, n), "out")
    if not pts:
        return None
    a = np.array(pts)
    return float(np.percentile(a[:, 1], 10)), float(np.median(a[:, 2]))

def _dims(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                          "-of", "csv=p=0", path], capture_output=True, text=True, check=True).stdout.strip().split(",")
    return int(out[0]), int(out[1])

def render_clips(edl, workdir):
    src, fps = edl["src"], edl["fps"]
    os.makedirs(workdir, exist_ok=True)
    fit = "" if _dims(src) == (W, H) else f"scale={W}:{H}:flags=lanczos,"   # 4K iPhone source -> 1080x1920 canvas

    def one(i, c):
        dur = c["out"] - c["in"]
        n = round(dur * fps)
        fc = face_center(src, c["in"], c["out"], tag=f"c{i}") if SCALE[c["zoom"]] != 1.0 else (W / 2, H / 2)
        cr = crop_for(c["zoom"], fc)
        vf = (f"crop={cr[0]}:{cr[1]}:{cr[2]}:{cr[3]},scale={W}:{H}:flags=lanczos," if cr else fit) + "setsar=1"
        af = (f"afade=t=in:d=0.006,afade=t=out:st={dur - 0.012:.3f}:d=0.012,"
              f"apad,atrim=0:{n / fps:.6f}")
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{c['in']:.4f}", "-i", src,
             "-map", "0:v:0", "-map", "0:a:0", "-frames:v", str(n), "-vf", vf, "-af", af,
             "-r", str(fps), "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p",
             "-c:a", "pcm_s16le", "-ar", "48000", f"{workdir}/{i:03d}.mov"])
        return i, fc, cr

    with ThreadPoolExecutor(6) as ex:
        for i, fc, cr in ex.map(lambda a: one(*a), enumerate(edl["clips"])):
            print(f"  clip {i:02d} face=({fc[0]:.0f},{fc[1]:.0f}) crop={cr}", flush=True)
    with open(f"{workdir}/list.txt", "w") as f:
        for i in range(len(edl["clips"])):
            f.write(f"file '{i:03d}.mov'\n")
    out = f"{workdir}/assembled.mov"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{workdir}/list.txt", "-c", "copy", out])
    return out

def runs_filter(runs, band_h, fulls=(), ramp=0.2):
    """runs: [(t0, t1, band_file, anim_in, anim_out, pushes)], pushes = [(a, b, px)] per framed clip in the run.
    Face layer pushed down (per clip, so every take sits at the same height) + band sliding in from the top."""
    def k_of(t0, t1, ain, aout):
        k = f"(1-pow(1-min(max((t-{t0:.4f})/{ramp},0),1),3))" if ain else "1"
        if aout:
            k = f"min({k},(1-pow(1-min(max(({t1:.4f}-t)/{ramp},0),1),3)))"
        return k
    def win(a, b):
        return f"gte(t,{a - 0.001:.4f})*lt(t,{b - 0.001:.4f})"
    ks = [k_of(r[0], r[1], r[3], r[4]) for r in runs]
    face = "0"
    for r, k in zip(reversed(runs), reversed(ks)):
        for a, b, px in reversed(r[5]):
            face = f"if({win(a, b)},{px}*{k},{face})"
    fc = [f"color=black:s={W}x{H}:r=30[cv]",
          f"[cv][0:v]overlay=x=0:y='{face}':eval=frame:shortest=1[f0]"]
    for i, (r, k) in enumerate(zip(runs, ks)):
        fc.append(f"[{i + 1}:v]setpts=PTS-STARTPTS+{r[0]:.4f}/TB[b{i}]")
        fc.append(f"[f{i}][b{i}]overlay=x=0:y='-{band_h}+{band_h}*{k}':enable='{win(r[0], r[1])}':eval=frame:eof_action=pass[f{i + 1}]")
    last = f"f{len(runs)}"
    post = []
    for j, f in enumerate(fulls):                   # full-screen inserts: hard cut in and out, cover face and band
        a, b = f[0], f[1]
        if len(f) > 3 and f[3]:                     # clean graphics (light paper): composite after the grade
            post.append((j, a, b))
            continue
        k = 1 + len(runs) + j
        fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{a:.4f}/TB[x{j}]")
        fc.append(f"[{last}][x{j}]overlay=x=0:y=0:enable='{win(a, b)}':eof_action=pass[g{j}]")
        last = f"g{j}"
    fc.append(f"[{last}]{GRADE}[gr]")
    last = "gr"
    for j, a, b in post:
        k = 1 + len(runs) + j
        fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{a:.4f}/TB[x{j}]")
        fc.append(f"[{last}][x{j}]overlay=x=0:y=0:enable='{win(a, b)}':eof_action=pass[p{j}]")
        last = f"p{j}"
    fc.append(f"[{last}]null[v]")
    return ";".join(fc)

def finalize(inp, out, runs=(), band_h=810, fulls=(), maxrate=None):
    inputs = ["-i", inp]
    for r in runs:
        inputs += ["-i", r[2]]
    for f in fulls:
        inputs += ["-i", f[2]]
    if runs or fulls:
        vmap = ["-filter_complex", runs_filter(runs, band_h, fulls), "-map", "[v]", "-map", "0:a"]
    else:
        vmap = ["-vf", GRADE]
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", inp, "-vn",
                        "-af", ACHAIN + ",loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(["ffmpeg", "-v", "error", "-y", *inputs, *vmap, "-af", ACHAIN + "," + ln + ",aresample=48000",
         "-c:v", "libx264", "-preset", "slow", "-crf", "17", *(["-maxrate", maxrate, "-bufsize", f"{2 * int(maxrate.rstrip('M'))}M"] if maxrate else []),
         "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
         "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out])

if __name__ == "__main__":
    edl = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "edl.json"))
    out = sys.argv[2] if len(sys.argv) > 2 else "final.mp4"
    finalize(render_clips(edl, "clips"), out)
    print("done ->", out)
