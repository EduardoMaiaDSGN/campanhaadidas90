"""Checagem tripla da fala. Rode a cada mudança de corte e antes de toda entrega: fala duplicada, palavra cortada e
corte estranho são a base da edição e não podem chegar até ele.

  python checar_fala.py edl.json transcricao.json audio16k.wav [--prompt "jargões"] [--aceitos checagem_aceitos.json]
                        [--saida checagem_fala.md]

1. BORDAS: em cada entrada/saída de clipe, a fala continua do outro lado do corte? (fim de vogal comido, como o "i"
   do "aqui"; começo de palavra cortado; emenda colada entre dois takes).
2. RETAKES ESCONDIDOS: palavras que o whisper "esticou" (uma palavra de 0,3 s com 1–1,6 s) escondem uma tentativa
   repetida ("ele consegue... ele consegue prever"). Cada uma é ouvida de novo, isolada.
3. ESCUTA: transcreve sem contexto a janela de cada emenda e o corte inteiro e procura a mesma sequência de palavras
   duas vezes em poucos segundos. Também aponta microcortes (< 0,3 s tirados: pulinho na imagem).

Saída: um relatório com cada ponto marcado como REPETIÇÃO, CORTADA, VERIFICAR ou MICROCORTE. Nada vai para ele com
ponto em aberto: conserte (a/b/cuts/nocut) ou, se for fala intencional (ênfase, "plano Pro... plano Pro"), registre
em checagem_aceitos.json com o motivo.
"""
import argparse, json, os, re, sys, unicodedata
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corte

SR = 16000
STOP_RAW = set("""a o e é de do da dos das um uma uns umas que pra pro para no na nos nas em se me te eu ele ela você
vocês tá to tô vai lá aí isso esse essa com por mais não né ou só the of and ah é""".split())

def _norm(w):
    w = unicodedata.normalize("NFKD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if not unicodedata.combining(c)))

STOP = {re.sub(r"[^a-z0-9]", "", "".join(c for c in unicodedata.normalize("NFKD", w) if not unicodedata.combining(c)))
        for w in STOP_RAW}   # sem acento, como as palavras comparadas

def transcrever(x, prompt=""):
    import mlx_whisper
    seg = np.concatenate([np.zeros(8000, np.float32), x.astype(np.float32), np.zeros(16000, np.float32)])
    r = mlx_whisper.transcribe(seg, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="pt",
                               word_timestamps=True, condition_on_previous_text=False, temperature=0.0,
                               initial_prompt=prompt or None)
    ws = [(w["word"].strip(), w["start"] - 0.5) for s in r["segments"] for w in s["words"] if w["word"].strip()]
    return r["text"].strip(), ws

def repeticoes(ws, janela=6.0, nmin=2, nmax=6):
    """[(t1, t2, 'trecho')] sequências de n palavras (nem todas 'vazias') que aparecem duas vezes em `janela` s."""
    norm = [(_norm(w), t) for w, t in ws]
    norm = [(w, t) for w, t in norm if w]
    hits = []
    for n in range(nmax, nmin - 1, -1):
        for i in range(len(norm) - n + 1):
            g = [w for w, _ in norm[i:i + n]]
            if all(w in STOP for w in g) or (n == 2 and min(len(w) for w in g) < 3):
                continue
            for j in range(i + n, len(norm) - n + 1):
                if norm[j][1] - norm[i][1] > janela:
                    break
                if [w for w, _ in norm[j:j + n]] == g:
                    if not any(a <= norm[i][1] <= b and " ".join(g) in txt for a, b, txt in hits):
                        hits.append((norm[i][1], norm[j][1], " ".join(g)))
    return hits

def censo(y, a, b, prompt="", win=1.6, hop=0.4):
    """Escuta [a, b] em janelas curtas e escalonadas. O whisper funde uma tentativa repetida quando ouve as duas de
    uma vez ("ele consegue... ele consegue" vira um "consegue" só); cada janela curta ouve uma tentativa, e a mesma
    palavra aparecendo em dois momentos diferentes denuncia a repetição. Devolve [(palavra, t)] sem duplicar instâncias."""
    achadas = []
    for w0 in np.arange(a, max(a + 0.01, b - win + hop), hop):
        w1 = min(b, w0 + win)
        _, ws = transcrever(y[int(w0 * SR):int(w1 * SR)], prompt)
        nn = [_norm(x) for x, _ in ws]
        if nn and max(nn.count(x) for x in nn) > 3:          # janela alucinada ("vamos lá, vamos lá, ...")
            continue
        for x, t_ in ws:
            if 0 <= t_ <= (w1 - w0) - 0.1:                     # palavra cortada na borda da janela não conta
                achadas.append((_norm(x), w0 + t_))
    achadas.sort(key=lambda q: q[1])
    uni = []
    for x, t_ in achadas:                                     # mesma palavra a < 0,35 s = a mesma instância
        if x and not any(x == u and abs(t_ - tu) < 0.45 for u, tu in uni[-12:]):
            uni.append((x, t_))
    return uni

def repetidas(uni, dmin=0.6, dmax=4.0):     # < 0,6 s é a mesma palavra ouvida em duas janelas (tempo do whisper oscila)
    """palavras de conteúdo (>= 4 letras, fora da lista vazia) que voltam entre dmin e dmax s depois"""
    hits = []
    for i, (x, t_) in enumerate(uni):
        if len(x) < 4 or x in STOP:
            continue
        for y_, ty in uni[i + 1:]:
            if ty - t_ > dmax:
                break
            if y_ == x and ty - t_ >= dmin:
                hits.append((t_, ty, x))
                break
    return hits

def _prancha(src, bordas, saida, w=620, h=150, fmax=5000):
    """Espectrogramas lado a lado (fim | começo), corte em vermelho, título com a palavra esperada."""
    from PIL import Image, ImageDraw, ImageFont
    f = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 15)
    tiles = []
    for titulo, a, b, cut in bordas:
        x = src[max(0, int(a * SR)):int(b * SR)]
        win, hop = 400, 32
        cols = [20 * np.log10(np.abs(np.fft.rfft(x[i:i + win] * np.hanning(win), n=1024)) + 1e-7)
                for i in range(0, max(1, len(x) - win), hop)]
        S = np.array(cols).T[:int(fmax / (SR / 1024))][::-1]
        S = np.clip((S - (S.max() - 70)) / 70, 0, 1)
        im = Image.fromarray((255 * (1 - S)).astype(np.uint8)).resize((w, h)).convert("RGB")
        t = Image.new("RGB", (w, h + 24), "white")
        t.paste(im, (0, 24))
        d = ImageDraw.Draw(t)
        d.text((4, 3), titulo[:78], fill="black", font=f)
        X = int((cut - a) / (b - a) * w)
        d.line([(X, 24), (X, h + 24)], fill="red", width=2)
        tiles.append(t)
    cols_n, por_pagina = 2, 12                      # páginas pequenas: dá para ler cada borda de verdade
    paginas = []
    for pg in range(0, max(1, len(tiles)), por_pagina):
        bloco = tiles[pg:pg + por_pagina]
        rows = (len(bloco) + cols_n - 1) // cols_n
        out = Image.new("RGB", (cols_n * (w + 10), max(1, rows) * (h + 34)), "white")
        for k, t in enumerate(bloco):
            out.paste(t, ((k % cols_n) * (w + 10), (k // cols_n) * (h + 34)))
        nome = saida.replace(".png", f"_{pg // por_pagina + 1}.png")
        out.save(nome)
        paginas.append(nome)
    return paginas

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("edl"); ap.add_argument("transcricao"); ap.add_argument("audio16k")
    ap.add_argument("--prompt", default="")
    ap.add_argument("--aceitos", default="")
    ap.add_argument("--saida", default="")
    ap.add_argument("--sem-escuta", action="store_true", help="só as checagens de áudio (rápido, sem whisper)")
    ap.add_argument("--so-bordas", action="store_true", help="só bordas e microcortes (com escuta)")
    A = ap.parse_args()
    A.escuta_bordas = not A.sem_escuta
    if A.so_bordas:
        A.sem_escuta = True
    edl = json.load(open(A.edl))["clips"]
    corte.carregar(A.transcricao, A.audio16k)
    import wave
    w = wave.open(A.audio16k)
    src = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    aceitos = json.load(open(A.aceitos)) if A.aceitos and os.path.exists(A.aceitos) else []

    # linha do tempo + áudio do corte
    t, parts, mapa = 0.0, [], []
    for c in edl:
        a, b = int(round(c["in"] * SR)), int(round(c["out"] * SR))
        x = src[a:b].copy()
        f = int(0.006 * SR)
        x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
        parts.append(x)
        mapa.append((t, t + (c["out"] - c["in"]), c))
        t += c["out"] - c["in"]
    y = np.concatenate(parts)
    def src_t(tl):
        for a, b, c in mapa:
            if a <= tl < b:
                return c["in"] + tl - a
        return None
    def tl_of(s):
        for a, b, c in mapa:
            if c["in"] <= s < c["out"]:
                return a + s - c["in"]
        return None
    def aceito(s, txt):
        return next((x for x in aceitos if abs(x.get("fonte", -99) - (s or -1)) < 1.5 and _norm(x.get("texto", "")) in _norm(txt)), None)

    achados = []   # (tempo na edição, tipo, tempo na fonte, detalhe)
    H = corte.HOP
    V, N = corte.voiced, corte.N
    def voz(a, b):
        i0, i1 = max(0, int(a / H)), min(N, int(b / H))
        return bool(V[i0:i1].any()) if i1 > i0 else False

    # 1. BORDAS: prancha com o espectrograma de cada saída e entrada de clipe, o corte em vermelho e a palavra esperada.
    #    É conferida a olho, uma por uma: vogal (faixas horizontais escuras) continuando logo depois da linha vermelha
    #    = palavra comida (era o "i" do "aqui", depois da explosão do "k"). Transcrever o pedacinho não serve: o
    #    whisper completa a palavra ou alucina em outra língua. Além da prancha, a fala que continua a < 60 ms do corte
    #    vira um ponto a conferir.
    tr = json.load(open(A.transcricao))
    palavras = [(w_["start"], w_["end"], w_["word"].strip()) for s_ in tr["segments"] for w_ in s_["words"] if w_["word"].strip()]
    bordas = []   # (titulo, inicio, fim, corte)
    for k, (a, b, c) in enumerate(mapa):
        nxt = mapa[k + 1][2] if k + 1 < len(mapa) else None
        prv = mapa[k - 1][2] if k > 0 else None
        noclip = [w for pa, pb, w in palavras if min(pb, c["out"]) - max(pa, c["in"]) > 0.5 * (pb - pa)]
        if k > 0 and not (prv is not None and abs(prv["out"] - c["in"]) < 0.02):
            bordas.append((f"{int(a // 60)}:{a % 60:04.1f} começo de '{c['label']}' — esperado: {' '.join(noclip[:2])}", c["in"] - 0.4, c["in"] + 0.6, c["in"]))
            if voz(c["in"] - 0.06, c["in"]):
                achados.append((a, "VERIFICAR", c["in"], f"'{c['label']}' começa em {c['in']:.2f} com fala logo antes: confira na prancha de bordas "
                                                f"se não cortou o começo de \"{noclip[0] if noclip else '?'}\" (ou se é emenda colada de propósito)"))
        if not (nxt is not None and abs(nxt["in"] - c["out"]) < 0.02):
            bordas.append((f"{int(b // 60)}:{b % 60:04.1f} fim de '{c['label']}' — esperado: {' '.join(noclip[-2:])}", c["out"] - 0.6, c["out"] + 0.4, c["out"]))
            if voz(c["out"], c["out"] + 0.06):
                achados.append((b, "VERIFICAR", c["out"], f"'{c['label']}' termina em {c['out']:.2f} e a fala continua logo depois: confira na prancha "
                                                f"se o fim de \"{noclip[-1] if noclip else '?'}\" está inteiro (ou se o que vem é a palavra seguinte, cortada de propósito)"))
    if A.saida:
        prancha = os.path.splitext(A.saida)[0] + "_bordas.png"
        for pg in _prancha(src, bordas, prancha):
            print("prancha de bordas ->", pg)

    # 3a. MICROCORTES (pulinho na imagem): salto < 0,3 s dentro da mesma fala. Só pesa com câmera na mão andando
    #     (gravação externa); sentado e parado o microcorte não aparece.
    for (a0, b0, c0), (a1, b1, c1) in (zip(mapa, mapa[1:]) if corte.PISO is not None and corte.PISO > -50 else []):
        gap = c1["in"] - c0["out"]
        if c0["label"].split(".")[0] == c1["label"].split(".")[0] and 0.02 < gap < 0.30:
            achados.append((b0, "MICROCORTE", c0["out"], f"tira só {gap:.2f}s entre '{c0['label']}' e '{c1['label']}' "
                                              f"(com câmera na mão vira um pulinho; prefira manter a pausa)"))

    emendas = []   # (tempo, 'a'|'b', o que se ouve) — o relatório lista todas, para ler como fala corrida
    if not A.sem_escuta:
        # 2. RETAKES ESCONDIDOS
        tr = json.load(open(A.transcricao))
        for s in tr["segments"]:
            for w_ in s["words"]:
                L = len(re.sub(r"\W", "", w_["word"]))
                est, span = 0.10 + 0.07 * L, w_["end"] - w_["start"]
                mid = (w_["start"] + w_["end"]) / 2
                tl = tl_of(mid)
                if span > 1.6 * est and span > 0.45 and tl is not None:
                    a, b = max(0, tl - span / 2 - 1.2), min(len(y) / SR, tl + span / 2 + 1.2)
                    txt, ws = transcrever(y[int(a * SR):int(b * SR)], A.prompt)
                    rep = [r[2] for r in repeticoes([(x, a + t_) for x, t_ in ws], janela=4.0)]
                    rep += [f"{x} ({t1:.1f}s e {t2:.1f}s)" for t1, t2, x in repetidas(censo(y, a, b, A.prompt))]
                    tipo = "REPETIÇÃO" if rep else "PAUSA"
                    achados.append((tl, tipo, w_["start"], f"palavra esticada '{w_['word'].strip()}' ({span:.2f}s; fonte {w_['start']:.2f}) "
                                              f"→ ouvido: \"{txt}\"" + (f" — repete: {'; '.join(rep)}" if rep else
                                              " — ouvida em janelas curtas, sem repetição: era pausa")))
        # 3b. ESCUTA DAS EMENDAS
        for (a0, b0, c0), (a1, b1, c1) in zip(mapa, mapa[1:]):
            if abs(c1["in"] - c0["out"]) < 0.02:
                continue
            a, b = max(0, b0 - 1.4), min(len(y) / SR, b0 + 1.4)
            txt, ws = transcrever(y[int(a * SR):int(b * SR)], A.prompt)
            emendas.append((b0, f"{c0['label']}|{c1['label']}", txt))
            reps = [(t1, g) for t1, t2, g in repeticoes([(x, a + t_) for x, t_ in ws], janela=3.0)]
            reps += [(t1, f"{x} ({t1:.1f}s e {t2:.1f}s)") for t1, t2, x in repetidas(censo(y, a, b, A.prompt), dmax=2.6)]
            for t1, g in reps:
                achados.append((t1, "REPETIÇÃO", src_t(t1), f"emenda '{c0['label']}'|'{c1['label']}': \"{g}\" duas vezes → ouvido: \"{txt}\""))
        # 3c. ESCUTA DO CORTE INTEIRO (janelas de 8 s com sobreposição)
        vistos = set()
        for a in np.arange(0, len(y) / SR, 4.0):
            b = min(len(y) / SR, a + 8.0)
            txt, ws = transcrever(y[int(a * SR):int(b * SR)], A.prompt)
            for t1, t2, g in repeticoes([(x, a + t_) for x, t_ in ws], janela=6.0):
                key = (round(t1), g)
                if key not in vistos:
                    vistos.add(key)
                    achados.append((t1, "REPETIÇÃO", src_t(t1), f"\"{g}\" duas vezes ({t1:.1f}s e {t2:.1f}s) → trecho: \"{txt}\""))

    # junta, marca aceitos, ordena
    linhas, abertos = [], 0
    for tl, tipo, s, det in sorted(achados, key=lambda q: q[0]):
        ok = aceito(s, det)
        st = f"OK (aceito: {ok['motivo']})" if ok else ("ok (pausa)" if tipo == "PAUSA" else tipo)
        abertos += 0 if (ok or tipo == "PAUSA") else 1
        mm = f"{int(tl // 60)}:{tl % 60:04.1f}"
        linhas.append(f"| {mm} | {st} | {det} |")
    rel = ["# Checagem da fala", "", f"Corte: {A.edl} — {len(edl)} clipes, {len(y)/SR:.1f}s", "",
           f"**{abertos} ponto(s) em aberto.**" + (" Nada pode ser entregue até resolver." if abertos else " Tudo certo."), "",
           "| tempo | status | detalhe |", "|---|---|---|", *linhas]
    if emendas:
        rel += ["", "## O que se ouve em cada jump cut (leia como fala corrida)", "",
                *[f"- {int(t_ // 60)}:{t_ % 60:04.1f} `{lab}` — {txt}" for t_, lab, txt in emendas]]
    rel += ["", "Pranchas de bordas: confira TODAS as páginas (vogal continuando logo depois da linha vermelha = palavra comida)."]
    out = "\n".join(rel)
    if A.saida:
        open(A.saida, "w").write(out + "\n")
    print(out)

if __name__ == "__main__":
    main()
