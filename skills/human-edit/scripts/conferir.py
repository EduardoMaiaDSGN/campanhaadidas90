"""Instrumentos de conferência. Rode antes de mandar qualquer versão.

  python conferir.py espectro FONTE a b [--marcas 6.333,6.43] [--saida esp.png]   # várias faixas: repita a b
  python conferir.py palavra VIDEO a b                 # o que se ouve SÓ nesse trecho (ex.: a última palavra antes do corte)
  python conferir.py comparar NOVO ANTERIOR [--ignorar 39.2-44.8 ...]   # prova que só mudou o que devia
  python conferir.py volume VIDEO                      # loudness integrado (alvo -14 LUFS) e pico
  python conferir.py quadros VIDEO t1 t2 ... [--saida quadros.png] [--recorte crop=1080:700:0:0]
  python conferir.py emendas edl.json                  # como soa cada jump cut: transcreve ±0,9 s em volta de cada emenda
  python conferir.py esticadas transcricao.json edl.json   # palavras "esticadas" no corte: suspeita de retake escondido

Por que cada um existe:
- espectro: um final de palavra cortado não aparece em transcrição (o whisper completa a palavra). No espectrograma
  se vê a vogal: a explosão do "k" não é o fim do "aqui", o "i" vem depois dela.
- palavra: transcrever só o trecho final, sem contexto, tira a "ajuda" do modelo de linguagem: o "aqui" cortado vira
  "Obrigado." ou lixo, o inteiro vira "Aqui."
- emendas: monta o áudio do corte e transcreve, sem contexto, a janela em volta de cada emenda. É o teste mais fiel de
  "o que se ouve no corte" (frase inteira dos dois lados, sem repetição, sem falso começo). Em gravação externa,
  com vento, o auditar.py desalinha os tempos e acusa palavra perdida que não está; aqui não.
- comparar: PSNR quadro a quadro contra a versão anterior. 138 = idêntico; ~46-50 = só ruído de codificação; abaixo
  disso mudou de verdade. Toda entrega de ajuste deve mostrar que o resto ficou igual.
"""
import argparse, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTE_UI = "/System/Library/Fonts/SFNS.ttf"

def _read(path, ss, dur, sr):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(dur), "-i", path, "-ac", "1", "-ar", str(sr),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def strip(path, a, b, title, marks=(), px_per_s=1400, fmax=5000):
    """Spectrogram strip 0-5 kHz with a time ruler (formants, stop closures and bursts are visible)."""
    SR = 16000
    x = _read(path, a, b - a, SR)
    win, hop = 400, 16          # 25 ms window, 1 ms hop
    cols = []
    for i in range(0, len(x) - win, hop):
        sp = np.abs(np.fft.rfft(x[i:i + win] * np.hanning(win), n=1024))
        cols.append(20 * np.log10(sp + 1e-7))
    S = np.array(cols).T
    S = S[:int(fmax / (SR / 1024))][::-1]
    S = np.clip((S - (S.max() - 75)) / 75, 0, 1)
    img = Image.fromarray((255 * (1 - S)).astype(np.uint8)).resize((int((b - a) * px_per_s), 360)).convert("RGB")
    out = Image.new("RGB", (img.width + 60, img.height + 70), "white")
    out.paste(img, (50, 30))
    d = ImageDraw.Draw(out)
    f = ImageFont.truetype(FONTE_UI, 14)
    d.text((50, 6), title, fill="black", font=f)
    t = np.ceil(a * 20) / 20
    while t <= b:
        X = 50 + int((t - a) * px_per_s)
        major = abs(t * 10 - round(t * 10)) < 1e-6
        d.line([(X, 30 + img.height), (X, 30 + img.height + (10 if major else 5))], fill="black")
        if major:
            d.text((X - 12, 30 + img.height + 12), f"{t:.1f}", fill="black", font=f)
        t += 0.05
    for kHz in range(0, 6):
        Y = 30 + img.height - int(kHz * 1000 / fmax * img.height)
        d.text((4, Y - 8), f"{kHz}k", fill="black", font=f)
    for tm in marks:
        X = 50 + int((tm - a) * px_per_s)
        d.line([(X, 30), (X, 30 + img.height)], fill="red", width=2)
    return out

def espectro(A):
    rs = [(float(A.trechos[i]), float(A.trechos[i + 1])) for i in range(0, len(A.trechos), 2)]
    marks = [float(m) for m in A.marcas.split(",")] if A.marcas else []
    ims = [strip(A.video, a, b, f"{a:.2f}-{b:.2f}  (vermelho = marcas)", [m for m in marks if a <= m <= b]) for a, b in rs]
    W = max(i.width for i in ims)
    canvas = Image.new("RGB", (W, sum(i.height for i in ims)), "white")
    y = 0
    for i in ims:
        canvas.paste(i, (0, y))
        y += i.height
    canvas.save(A.saida)
    print("->", A.saida)

def palavra(A):
    import mlx_whisper
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(A.a), "-t", str(A.b - A.a), "-i", A.video, "-ac", "1", "-ar", "16000",
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.concatenate([np.zeros(8000, np.float32), np.frombuffer(raw, np.float32), np.zeros(16000, np.float32)])
    r = mlx_whisper.transcribe(x, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="pt",
                               condition_on_previous_text=False, temperature=0.0)
    print(f"{A.a:.2f}-{A.b:.2f}: {r['text']!r}")

def _gray(p, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", p, "-frames:v", "1", "-vf", "scale=540:960",
                          "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).astype(float)

def _dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)

def comparar(A):
    skip = [tuple(map(float, s.split("-"))) for s in A.ignorar]
    worst = []
    for t in np.arange(0.2, min(_dur(A.novo), _dur(A.anterior)) - 0.2, 0.7):
        if any(s0 - 0.1 <= t <= s1 + 0.1 for s0, s1 in skip):
            continue
        mse = np.mean((_gray(A.novo, t) - _gray(A.anterior, t)) ** 2)
        worst.append((10 * np.log10(255 ** 2 / max(mse, 1e-9)), t))
    worst.sort()
    print("quadros comparados:", len(worst))
    print("menores PSNR:", [(round(p, 1), round(t, 2)) for p, t in worst[:6]])
    bad = [(round(p, 1), round(t, 2)) for p, t in worst if p < 40]
    print("MUDOU (PSNR < 40):", bad if bad else "nada")

def volume(A):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", A.video, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    summ = r[r.rfind("Summary:"):]
    for line in summ.splitlines():
        if any(k in line for k in ("I:", "Peak:", "LRA:")):
            print(line.strip())

def quadros(A):
    tiles = []
    for t in A.tempos:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{float(t):.3f}", "-i", A.video, "-frames:v", "1",
                              "-vf", (A.recorte + "," if A.recorte else "") + "scale=270:-2", "-f", "image2pipe", "-vcodec", "png", "-"],
                             capture_output=True, check=True).stdout
        import io
        tiles.append(Image.open(io.BytesIO(raw)).convert("RGB"))
    cols = min(4, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    h = max(i.height for i in tiles)
    out = Image.new("RGB", (cols * 280, rows * (h + 10)), "white")
    for k, i in enumerate(tiles):
        out.paste(i, ((k % cols) * 280, (k // cols) * (h + 10)))
    out.save(A.saida)
    print("->", A.saida)

def emendas(A):
    import json, mlx_whisper
    SR = 16000
    edl = json.load(open(A.edl))
    parts, t, joins = [], 0.0, []
    for c in edl["clips"]:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{c['in']:.4f}", "-t", f"{c['out'] - c['in']:.4f}", "-i", edl["src"],
                              "-map", "0:a:0", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).copy()
        n = int(round((c["out"] - c["in"]) * SR))
        x = np.pad(x, (0, max(0, n - len(x))))[:n]
        f = int(0.006 * SR)
        x[:f] *= np.linspace(0, 1, f)
        x[-f:] *= np.linspace(1, 0, f)
        parts.append(x)
        t += c["out"] - c["in"]
        joins.append((t, c["label"]))
    y = np.concatenate(parts)
    for (tj, lab), nxt in zip(joins[:-1], edl["clips"][1:]):
        a, b = max(0, tj - 0.9), tj + 0.9
        seg = np.concatenate([np.zeros(8000, np.float32), y[int(a * SR):int(b * SR)], np.zeros(16000, np.float32)])
        r = mlx_whisper.transcribe(seg, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="pt",
                                   condition_on_previous_text=False, temperature=0.0)
        print(f"{tj:6.2f} {lab:>12} | {nxt['label']:<12} {r['text'].strip()}")

def esticadas(A):
    import json, re
    tr, edl = json.load(open(A.transcricao)), json.load(open(A.edl))["clips"]
    usado = lambda t: any(c["in"] <= t <= c["out"] for c in edl)
    for i, s in enumerate(tr["segments"]):
        for w in s["words"]:
            L = len(re.sub(r"\W", "", w["word"]))
            est, span = 0.10 + 0.07 * L, w["end"] - w["start"]
            if span > 1.6 * est and span > 0.45 and usado((w["start"] + w["end"]) / 2):
                print(f"#{i:<3} {w['word'].strip():<14} {w['start']:7.2f}-{w['end']:7.2f} ({span:.2f}s; esperado ~{est:.2f}s)")

ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
s = sub.add_parser("espectro"); s.add_argument("video"); s.add_argument("trechos", nargs="+"); s.add_argument("--marcas", default=""); s.add_argument("--saida", default="espectro.png")
s = sub.add_parser("palavra"); s.add_argument("video"); s.add_argument("a", type=float); s.add_argument("b", type=float)
s = sub.add_parser("comparar"); s.add_argument("novo"); s.add_argument("anterior"); s.add_argument("--ignorar", nargs="*", default=[])
s = sub.add_parser("volume"); s.add_argument("video")
s = sub.add_parser("emendas"); s.add_argument("edl")
s = sub.add_parser("esticadas"); s.add_argument("transcricao"); s.add_argument("edl")
s = sub.add_parser("quadros"); s.add_argument("video"); s.add_argument("tempos", nargs="+"); s.add_argument("--saida", default="quadros.png"); s.add_argument("--recorte", default="")
A = ap.parse_args()
{"espectro": espectro, "palavra": palavra, "comparar": comparar, "volume": volume, "quadros": quadros, "emendas": emendas, "esticadas": esticadas}[A.cmd](A)
