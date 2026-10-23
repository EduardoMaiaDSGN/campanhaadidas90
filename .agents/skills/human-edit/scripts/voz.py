"""Voz limpa para um corte novo, a partir da voz já isolada de um corte anterior (sem pagar outro isolamento).
Trechos da fonte que o corte antigo já tinha vêm do áudio isolado; o que é novo vem da fonte bruta (finais de
palavra) ou vira silêncio (ar a mais no começo de um clipe).

  python voz.py --src FONTE.MOV --edl-antiga edl_isolada.json --isolada voz_isolada.wav \
                --edl-nova edl.json --saida voz.wav [--bruta voz_bruta.wav]

--bruta: o áudio bruto do MESMO corte que foi isolado; com ele cada clipe é realinhado (o isolado pode
escorregar alguns ms). Sem ele, nenhum realinhamento.
"""
import argparse, json, subprocess
import numpy as np

SR = 48000
S = lambda x: int(round(x * SR))
ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--edl-antiga", required=True)
ap.add_argument("--isolada", required=True)
ap.add_argument("--edl-nova", required=True)
ap.add_argument("--saida", required=True)
ap.add_argument("--bruta")
A = ap.parse_args()
old_edl, iso_wav, new_edl, out, raw_old_wav, SRC = A.edl_antiga, A.isolada, A.edl_nova, A.saida, A.bruta, A.src

def read(path, extra=()):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, *extra, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()

iso = read(iso_wav)
src = read(SRC)
_w = SR // 100                                     # 10 ms frames of the raw source: its noise floor
_db = 20 * np.log10(np.sqrt(np.mean(src[:len(src) // _w * _w].reshape(-1, _w) ** 2, axis=1)) + 1e-9)
PISO = float(np.percentile(_db, 10))

def so_pausa(seg):
    """True when a new piece is just a pause (nothing above the noise floor): it goes back as silence, not as raw
    audio (outdoors the raw pause is wind and street, an audible puff between two clean isolated words)."""
    n = len(seg) // _w
    if n == 0:
        return True
    return float(np.max(20 * np.log10(np.sqrt(np.mean(seg[:n * _w].reshape(n, _w) ** 2, axis=1)) + 1e-9))) < PISO + 8
raw_old = read(raw_old_wav) if raw_old_wav else None

def local_offset(t0, t1):
    """samples to add to an iso read position so it lines up with the raw old cut around [t0, t1]"""
    if raw_old is None:
        return 0
    s, e = S(t0), S(t1)
    A, B = np.abs(raw_old[s:e]), np.abs(iso[s:e])
    n = min(len(A), len(B))
    if n < SR // 4:
        return 0
    A, B = A[:n], B[:n]
    best, bk = -1, 0
    for k in range(-720, 721, 2):           # +-15 ms
        v = np.dot(A[:n - k], B[k:]) if k >= 0 else np.dot(A[-k:], B[:n + k])   # iso[i + k] <-> raw[i]
        if v > best:
            best, bk = v, k
    return bk

def timeline(clips):
    t = 0.0
    for c in clips:
        c["t0"] = t
        t += c["out"] - c["in"]
    return clips

old = timeline(json.load(open(old_edl))["clips"])
for o in old:                                   # per old clip: where its audio really sits in the isolated file
    o["shift"] = local_offset(o["t0"], o["t0"] + o["out"] - o["in"])
new = timeline(json.load(open(new_edl))["clips"])

total = S(sum(c["out"] - c["in"] for c in new))
y = np.zeros(total, np.float32)
fade = S(0.005)
report = []
for c in new:
    a, b = c["in"], c["out"]
    covered = []
    for o in old:
        lo, hi = max(a, o["in"]), min(b, o["out"])
        if hi - lo > 1e-4:
            covered.append((lo, hi, o))
    covered.sort(key=lambda q: q[0])
    cur = a
    pieces = []
    for lo, hi, o in covered:
        if lo - cur > 1e-4:
            pieces.append((cur, lo, None))
        pieces.append((lo, hi, o))
        cur = hi
    if b - cur > 1e-4:
        pieces.append((cur, b, None))
    for lo, hi, o in pieces:
        dst = S(c["t0"] + lo - a)
        n = S(hi - lo)
        if o is not None:
            seg = iso[S(o["t0"] + lo - o["in"]) + o["shift"]:][:n]
            kind = "iso"
        elif lo <= a + 1e-4:                         # new air at the start of a clip: keep it clean
            seg = np.zeros(n, np.float32)
            kind = "silence"
        elif so_pausa(src[S(lo):][:n]):              # a pause put back in the cut: clean silence
            seg = np.zeros(n, np.float32)
            kind = "silence"
        else:                                        # new word tail: raw source, faded in under the iso audio
            seg = src[S(lo):][:n].copy()
            r = min(fade, len(seg))
            seg[:r] *= np.linspace(0, 1, r)
            if hi >= b - 1e-4:                       # tail at the end of a clip
                # a long tail holds a whole phoneme (the "i" of "aqui"): full level, fade only the last 25 ms;
                # a short one is just decay (and may hold the onset of the next sound): let it die out across its length
                r = min(len(seg), S(0.025)) if hi - lo > 0.12 else len(seg)
                seg[len(seg) - r:] *= np.cos(np.linspace(0, np.pi / 2, r)) ** 2
            kind = "raw"
        y[dst:dst + len(seg)] = seg[:max(0, min(len(seg), total - dst))]
        report.append(f"{c['label']:<12} {lo:8.3f}-{hi:8.3f} {kind}")
y.astype(np.float32).tofile(out + ".f32")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", out + ".f32",
                "-c:a", "pcm_s16le", out], check=True)
print("\n".join(r for r in report if not r.endswith("iso")))
print(f"done -> {out} ({total / SR:.2f}s)")
