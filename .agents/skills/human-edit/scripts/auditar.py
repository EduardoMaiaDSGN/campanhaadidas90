"""Auditoria do corte: re-transcreve cada clipe (com um pouco de contexto) palavra por palavra e mostra o que sobra
fora/entre as palavras: lixo no começo ou no fim, respiros, falsos começos, buracos longos.

  python auditar.py edl.json audio16k.wav [--prompt "jargões"] [--saida auditoria.json]

Atenção: o whisper completa a palavra que ele espera ouvir. Ele acha que "aqui" está inteiro mesmo quando o "i"
foi cortado. Final de palavra se confere no espectrograma (conferir.py espectro), não aqui.
"""
import argparse, json, subprocess, tempfile, wave
import numpy as np
import mlx_whisper

ap = argparse.ArgumentParser()
ap.add_argument("edl")
ap.add_argument("audio16k")
ap.add_argument("--prompt", default="")
ap.add_argument("--saida", default="auditoria.json")
A = ap.parse_args()
EDL = json.load(open(A.edl))
CTX = 0.6   # seconds of context transcribed on each side of a clip
CLIP = tempfile.mktemp(suffix=".wav")

w = wave.open(A.audio16k)
sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768

def db(a, b):
    seg = x[int(a * sr):int(b * sr)]
    return 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9) if len(seg) else -99

def flat(a, b):
    """spectral flatness (0 tonal .. 1 noise): breaths/hiss are flat, voiced speech is not"""
    seg = x[int(a * sr):int(b * sr)]
    if len(seg) < 256:
        return 0
    S = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) + 1e-9
    return float(np.exp(np.mean(np.log(S))) / np.mean(S))

report = []
for i, c in enumerate(EDL["clips"]):
    a, b = max(c["in"] - CTX, 0), c["out"] + CTX
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(a, 0):.3f}", "-to", f"{b:.3f}", "-i", A.audio16k, CLIP], check=True)
    r = mlx_whisper.transcribe(CLIP, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="pt",
                               word_timestamps=True, condition_on_previous_text=False,
                               initial_prompt=A.prompt or None)
    ws = [(q["word"].strip(), q["start"] + a, q["end"] + a, q["probability"]) for s in r["segments"] for q in s["words"]]
    inside = [q for q in ws if (q[1] + q[2]) / 2 >= c["in"] and (q[1] + q[2]) / 2 <= c["out"]]
    before = [q for q in ws if (q[1] + q[2]) / 2 < c["in"]]
    after = [q for q in ws if (q[1] + q[2]) / 2 > c["out"]]
    line = f"#{i:02d} {c['label']:<12} {c['in']:7.2f}-{c['out']:7.2f} | "
    line += " ".join(f"{q[0]}[{q[1]:.2f}-{q[2]:.2f}|{q[3]:.2f}]" for q in inside)
    print(line)
    if before:
        print(f"      before: {' '.join(q[0] + f'[{q[1]:.2f}-{q[2]:.2f}]' for q in before[-3:])}")
    if after:
        print(f"      after : {' '.join(q[0] + f'[{q[1]:.2f}-{q[2]:.2f}]' for q in after[:3])}")
    if inside:
        lead, trail = inside[0][1] - c["in"], c["out"] - inside[-1][2]
        print(f"      lead={lead:.2f}s ({db(c['in'], inside[0][1]):.0f}dB flat={flat(c['in'], inside[0][1]):.2f})"
              f"  trail={trail:.2f}s ({db(inside[-1][2], c['out']):.0f}dB flat={flat(inside[-1][2], c['out']):.2f})")
        for p, q in zip(inside, inside[1:]):
            g = q[1] - p[2]
            if g > 0.10:
                print(f"      gap {g:.2f}s after '{p[0]}' @{p[2]:.2f} ({db(p[2], q[1]):.0f}dB flat={flat(p[2], q[1]):.2f})")
    report.append({"i": i, "label": c["label"], "in": c["in"], "out": c["out"], "words": inside, "before": before, "after": after})
json.dump(report, open(A.saida, "w"), ensure_ascii=False, indent=1)
