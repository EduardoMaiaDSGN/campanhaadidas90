"""Som final: voz isolada -> EQ com mais agudo, de-esser e compressor; efeitos sonoros sutis nos eventos da edição;
loudnorm em 2 passadas (-17 LUFS em mono, que vira -14 no estéreo) e mux no vídeo (o vídeo é copiado, não recodificado).

Um evento = (tempo s, arquivo da biblioteca, pico dBFS, alinhamento, gate)
  alinhamento "peak": o momento mais forte do som cai no tempo; "start": o som começa no tempo.
  gate: nada do som antes desse tempo (8 ms de fade depois); serve para um whoosh nunca subir em cima da última
  sílaba antes de um corte.
"""
import json, os, re, subprocess, tempfile
import numpy as np

SR = 48000
# 80 Hz high-pass, -2.5 dB na lama (250 Hz), +3 dB de presença (3.2 kHz), +4 dB de agudo (shelf 6.5 kHz) e exciter:
# o "agudinho" que a voz do iPhone pedia; de-esser e compressor deixam a voz uniforme sem chiar no "s".
CADEIA_VOZ = ("highpass=f=80,equalizer=f=250:t=q:w=1.2:g=-2.5,equalizer=f=3200:t=q:w=1.0:g=3,highshelf=f=6500:g=4,"
              "aexciter=amount=2:drive=5:freq=5500:ceil=16000,"
              "deesser=i=0.45,"
              "acompressor=threshold=-20dB:ratio=3:attack=6:release=110:makeup=2.5")
CLIQUES = {"Click.wav", "Instant Camera Button 1.wav"}     # ele gostou dos cliques: ficam 2 dB acima do resto

class Eventos(list):
    """Lista de eventos sonoros com atalhos."""
    def ev(self, t, arquivo, db, alinhamento="start", gate=None):
        self.append((t, arquivo, db, alinhamento, gate))

    def ticks(self, a, b, arquivo="Click.wav", db=-34, fps=30, cada=10):
        """Um clique em cada corte de uma montagem (a cada `cada` quadros), sem o primeiro (que já tem whoosh)."""
        n = round(b * fps) - round(a * fps)
        for k in range(1, n // cada + (1 if n % cada >= 6 else 0)):
            self.ev(a + k * cada / fps, arquivo, db)

def _load(lib, name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(lib, name), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32).copy()
    return a / (np.abs(a).max() + 1e-9)          # peak-normalise; gains are absolute peak dBFS

def _peak_at(a):
    env = np.convolve(np.abs(a), np.ones(480) / 480, mode="same")
    return int(np.argmax(env))

def _lu(x):   # rough loudness: RMS of the loudest 10% of 50 ms windows, dBFS
    w = SR // 20
    r = np.sqrt(np.array([np.mean(x[i:i + w] ** 2) for i in range(0, len(x) - w, w)]) + 1e-12)
    r = np.sort(r)[-max(1, len(r) // 10):]
    return 20 * np.log10(np.mean(r))

def mixar(video, voz, saida, eventos, lib, duracao, stems=None):
    """voz: wav da voz limpa (isolada) do corte; duracao: duração da timeline (s); stems: pasta para salvar voz/sfx (npy)."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", voz, "-af", CADEIA_VOZ, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    voice = np.frombuffer(raw, np.float32).copy()
    n = int(duracao * SR) + SR
    mix = np.zeros(n, np.float32)
    mix[:len(voice)] += voice[:n]
    sfx = np.zeros(n, np.float32)
    cache = {}
    for t0, f, db, align, gate in eventos:
        a = cache.setdefault(f, _load(lib, f))
        s = int(t0 * SR) - (_peak_at(a) if align == "peak" else 0)
        a2 = a[max(0, -s):]
        s = max(s, 0)
        e = min(n, s + len(a2))
        boost = 10 if f in CLIQUES else 8
        piece = a2[:e - s] * 10 ** ((db + boost) / 20)
        if gate is not None:                        # mute everything before the gate, 8 ms fade-in after it
            g = np.clip((np.arange(s, e) / SR - gate) / 0.008, 0, 1)
            piece = piece * g
        sfx[s:e] += piece
    print(f"{len(eventos)} efeitos")
    print(f"voz: pico {20*np.log10(np.abs(mix).max()+1e-9):.1f} dBFS, forte {_lu(mix):.1f} | "
          f"efeitos: pico {20*np.log10(np.abs(sfx).max()+1e-9):.1f} dBFS, "
          f"forte(ativo) {_lu(sfx[np.abs(sfx) > 1e-4]) if (np.abs(sfx) > 1e-4).any() else -99:.1f}")
    if stems:
        np.save(os.path.join(stems, "stem_voz.npy"), mix)
        np.save(os.path.join(stems, "stem_sfx.npy"), sfx)
    mix += sfx
    tmp = tempfile.NamedTemporaryFile(suffix=".f32", delete=False, dir=os.path.dirname(os.path.abspath(saida)))
    np.clip(mix, -1, 1).astype(np.float32).tofile(tmp.name)
    base = ["-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp.name]
    # -17 in mono: the mono -> stereo pan adds +3 LU, so the delivered file lands on -14 LUFS (Instagram)
    r = subprocess.run(["ffmpeg", "-hide_banner", *base, "-af", "loudnorm=I=-17:TP=-4.5:LRA=9:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))
    ln = (f"loudnorm=I=-17:TP=-4.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, *base, "-map", "0:v", "-map", "1:a",
                    "-af", ln + ",aresample=48000,pan=stereo|c0=c0|c1=c0", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                    "-shortest", "-movflags", "+faststart", saida], check=True)
    os.unlink(tmp.name)
    print("pronto ->", saida)
