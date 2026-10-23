"""Corte: takes escolhidos (segmento + faixa de palavras da transcrição) -> clipes sem respiro.

Cada fala vira um trecho; as bordas são refinadas no envelope de energia (10 ms); pausas e respiros internos
mais longos que MIN_PAUSE viram jump cuts, protegendo o miolo das palavras e a última consoante.
O rosto nunca recebe zoom: todo clipe sai "wide". Saída: edl.json (entradas/saídas alinhadas ao quadro).
"""
import json, wave
import numpy as np

FPS = 30
HOP = 0.01
PRE, POST = 0.02, 0.03      # air kept before first / after last sound of a beat
SIL = -55.0                 # below this = room tone
MIN_PAUSE = 0.10            # non-speech (silence or breath) longer than this gets cut
MIN_PIECE = 0.20
MERGE_UNDER = 0.30

tr = voiced = sound = envdb = None
N = 0
VOICED_DB, TAIL_DB = -44.0, -45.0     # quiet-room defaults; carregar() raises them over a noisy floor
PISO = None

def carregar(transcricao, audio16k):
    """Load the word-level transcript (mlx-whisper JSON) and the 16 kHz mono s16 wav of the source,
    and compute the 10 ms analysis every cutting function uses."""
    global tr, voiced, sound, envdb, N, SIL, VOICED_DB, TAIL_DB, PISO, MIN_PAUSE
    tr = json.load(open(transcricao))
    w = wave.open(audio16k)
    sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    hop = int(HOP * sr)

    def analyse(x):
        frames = np.array([x[i:i + hop] for i in range(0, len(x) - hop, hop)])
        e = 20 * np.log10(np.sqrt(np.mean(frames ** 2, axis=1)) + 1e-9)
        spec = np.abs(np.fft.rfft(frames * np.hanning(hop), axis=1)) + 1e-9
        return e, np.exp(np.mean(np.log(spec), axis=1)) / np.mean(spec, axis=1)

    envdb, flat = analyse(x)
    PISO = float(np.percentile(envdb, 10))
    if PISO > -50:
        # noisy recording (outdoors, wind, street): the fixed thresholds sit under the noise floor and everything
        # reads as speech. Analyse a high-passed copy (wind rumble out) and let the thresholds ride on its floor.
        from scipy.signal import butter, sosfilt
        envdb, flat = analyse(sosfilt(butter(4, 150, "highpass", fs=sr, output="sos"), x).astype(np.float32))
        PISO = float(np.percentile(envdb, 10))
        SIL, VOICED_DB, TAIL_DB = max(-55.0, PISO + 4), max(-44.0, PISO + 9), max(-45.0, PISO + 5)
        # over noise the closure of a stop (the silence before "c", "p", "t", 60-150 ms) reads as a pause and got cut
        # mid-word; and outdoors he is usually walking with the phone in hand, where a jump cut that removes under
        # ~0.3 s reads as a glitch ("corte estranho"). Only real pauses are cut.
        MIN_PAUSE = 0.32
        print(f"gravação com ruído: piso {PISO:.1f} dB -> voz > {VOICED_DB:.1f}, som > {SIL:.1f}, pausa > {MIN_PAUSE}s")
    voiced = (envdb > VOICED_DB) & (flat < 0.45)  # vowels / voiced consonants
    sound = envdb > SIL                            # anything above room tone (fricatives, decays, breaths)
    N = len(envdb)

def onset_near(t):
    """Start of the first word: first voiced frame near t, plus its initial consonant (<=100ms of sound)."""
    i = max(int(t / HOP) - 5, 0)
    if voiced[i]:
        while i > 0 and voiced[i - 1]:
            i -= 1
    else:
        j = i
        while j < N - 1 and not voiced[j] and (j - i) * HOP < 0.5:
            j += 1
        i = j
    k = 0
    while i > 0 and sound[i - 1] and k < 10:
        i -= 1; k += 1
    return i * HOP

def offset_near(t):
    """End of the last word: last voiced frame near t, then its unvoiced tail (s, ts, st...), bridging
    closures of <=30ms, stopping at silence or at the next word's voicing (<=250ms)."""
    i = min(int(t / HOP), N - 1)
    if voiced[i]:
        while i < N - 1 and voiced[i + 1] and (i - int(t / HOP)) * HOP < 0.35:
            i += 1
    else:
        j = i
        while j > 0 and not voiced[j] and (i - j) * HOP < 0.4:
            j -= 1
        i = j
    end, k, gap = i, 0, 0
    while i < N - 1 and k < 25:
        i += 1; k += 1
        if voiced[i]:
            break
        if sound[i]:
            end, gap = i, 0
        else:
            gap += 1
            if gap > 3:
                break
    return (end + 1) * HOP

def first_word_start(wd):
    # whisper stretches the first word over leading silence; trust its end more
    est = 0.10 + 0.07 * len(wd["word"].strip())
    return max(wd["start"], wd["end"] - est)

def pieces_of(a, b, ws):
    """Cut every non-voiced stretch (silence or breath) that is longer than MIN_PAUSE once the previous
    word's tail (<=120ms) and the next word's initial consonant (<=100ms) are protected."""
    i0, i1 = int(a / HOP), int(b / HOP)
    # word spans that whisper stretched over a pause (much longer than the word can be) protect nothing
    cores = [(q["start"], q["end"]) for q in ws
             if q["end"] - q["start"] <= 1.6 * (0.10 + 0.07 * len(q["word"].strip()))]
    parts, cur, k = [], a, i0
    while k < i1:
        if voiced[k]:
            k += 1
            continue
        j = k
        while j < i1 and not voiced[j]:
            j += 1
        s, e = k, j
        n = 0
        while s < e and envdb[s] > TAIL_DB and n < 12:
            s += 1; n += 1
        n = 0
        while e > s and envdb[e - 1] > TAIL_DB and n < 10:
            e -= 1; n += 1
        cs, ce = s * HOP + 0.02, e * HOP - 0.02
        inside_word = any(min(ce, we - 0.3 * (we - wa)) > max(cs, wa + 0.3 * (we - wa)) for wa, we in cores)
        in_edge_word = bool(ws) and (cs > ws[-1]["start"] or ce < ws[0]["end"])   # final plosive release / first word
        if k > i0 and j < i1 and (e - s) * HOP >= MIN_PAUSE and not inside_word and not in_edge_word:
            parts.append((cur, cs))
            cur = ce
        k = j
    parts.append((cur, b))
    spans = [(q["start"], q["end"]) for q in ws]
    keep = []
    for pa, pb in parts:
        has_word = any(min(pb, we) - max(pa, wa) > 0.04 for wa, we in spans) or (pb - pa) > 0.35
        if has_word or pb - pa >= MIN_PIECE:   # short pieces holding a word are merged below, never dropped
            keep.append((pa, pb))
    # a lone word shorter than MERGE_UNDER flashes by; keep its pause instead of cutting
    merged = []
    for pa, pb in keep:
        if merged and (merged[-1][1] - merged[-1][0] < MERGE_UNDER or pb - pa < MERGE_UNDER):
            merged[-1] = (merged[-1][0], pb)
        else:
            merged.append((pa, pb))
    return merged

def fa(t):
    return round(t * FPS) / FPS

def build(plan):
    clips = []
    for label, picks, emph, *ov in plan:
        ov = ov[0] if ov else {}
        ws = []
        for seg, a, b in picks:
            ws += tr["segments"][seg]["words"][a:b]
        a = ov.get("a", max(onset_near(first_word_start(ws[0])) - PRE, 0))
        b = ov.get("b", offset_near(ws[-1]["end"]) + POST)
        ws = [q for q in ws if q["end"] > a + 0.05 and q["start"] < b - 0.05] or ws
        text = " ".join(q["word"].strip() for q in ws)
        ps = pieces_of(a, b, ws) if not ov.get("nocut") else [(a, b)]
        for ca, cb in ov.get("cuts", []):          # explicit extra cuts (e.g. a dragged hesitation, a restarted phrase)
            # subtract [ca, cb] from every piece, even when it crosses the boundary between two pieces
            ps = [(x, y) for pa, pb in ps for x, y in ((pa, min(pb, ca)), (max(pa, cb), pb)) if y - x > 0.04]
        for n, (pa, pb) in enumerate(ps):
            clips.append({"label": label + (f".{n+1}" if len(ps) > 1 else ""), "in": fa(pa), "out": fa(pb),
                          "emph": emph, "split": bool(ov.get("split")), "text": text if n == 0 else ""})

    # never replay source audio: clamp overlaps with the previous clip
    for p, c in zip(clips, clips[1:]):
        if p["in"] < c["in"] < p["out"]:
            c["in"] = p["out"]

    # framing: the face is never zoomed (user preference) — always the original, widest framing.
    # Rhythm comes from the jump cuts and the inserts, not from punch-ins.
    for c in clips:
        c["zoom"] = "wide"
    return clips

def save(clips, path, src):
    json.dump({"fps": FPS, "src": src, "clips": clips},
              open(path, "w"), ensure_ascii=False, indent=1)
    t = 0
    for c in clips:
        print(f"{t:6.2f}  {c['label']:<13} {c['in']:7.2f}-{c['out']:7.2f} ({c['out']-c['in']:.2f}s) {c['zoom']:<5}{' S' if c['split'] else '  '} {c['text'][:64]}")
        t += c["out"] - c["in"]
    print(f"clips={len(clips)} total={t:.2f}s")
