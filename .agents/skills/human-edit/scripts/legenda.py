"""Legenda simples: o que é dito no corte, em blocos curtos de uma linha, brancos, centralizados no terço de baixo.

As palavras vêm de uma transcrição do ÁUDIO JÁ CORTADO (o tempo já é o da edição: nada de remapear a fonte, onde o
whisper estica a primeira palavra sobre as pausas). Os blocos ficam num JSON editável (legendas.json no _projeto):
corrija o texto ali (grafia de marcas, palavras que o whisper ouviu errado) e renderize de novo; o tempo não muda.
"""
import json, os, re, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
FONT = "/System/Library/Fonts/SFNS.ttf"

def transcrever_corte(audio, prompt="", lingua="pt"):
    """[{w, a, b}] do áudio do corte (tempo da edição)."""
    import mlx_whisper
    r = mlx_whisper.transcribe(audio, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language=lingua,
                               word_timestamps=True, condition_on_previous_text=False, initial_prompt=prompt or None)
    return [{"w": w["word"].strip(), "a": round(w["start"], 3), "b": round(w["end"], 3)}
            for s in r["segments"] for w in s["words"] if w["word"].strip()]

def _limpa(t):
    t = re.sub(r"[.,;:…]+$", "", t)            # sem pontuação no fim da palavra (? e ! ficam)
    return t.replace("...", "")

def blocos(palavras, correcoes=None, trocas=None, minusculas=True, max_chars=22, max_palavras=4, quebra=0.35):
    """Agrupa palavras em blocos de 1 linha. Quebra em fim de frase, antes de uma frase nova (o whisper começa frase
    com maiúscula), em pausa (> quebra s) e no limite de tamanho. Nunca mistura o fim de uma frase com o começo da outra.
    correcoes: {"palavra como saiu": "como deve ficar"} (sem diferenciar maiúsculas); os valores contam como nomes
    próprios e mantêm a grafia. trocas: {"trecho": "substituto"} no texto final do bloco (ex.: "24 barra 7": "24/7").
    minusculas: tudo em minúscula, menos nomes próprios e siglas (sem maiúscula solta no meio da frase)."""
    cor = {k.lower(): v for k, v in (correcoes or {}).items()}
    nomes = set(cor.values())
    pal = []
    for p in palavras:
        w = p["w"]
        if w.startswith("-") and pal:                  # "e -mail": o whisper separa o hífen
            pal[-1] = {**pal[-1], "w": pal[-1]["w"] + w, "b": p["b"]}
            continue
        core = re.sub(r"[.,;:?!…]+$", "", w)
        maiuscula = core[:1].isupper()
        if core.lower() in cor:
            w = cor[core.lower()] + w[len(core):]
            core = cor[core.lower()]
        sigla = core.isupper() and len(core) > 1        # GPT, PDF; "É" e "E" sozinhos são começo de frase
        nova_frase = bool(pal) and maiuscula and core not in nomes and not sigla
        if minusculas and core not in nomes and not (core.isupper() and len(core) > 1):
            w = w.lower()
        pal.append({**p, "w": w, "nova": nova_frase})
    grupos, cur = [], []                               # (palavras, fechou por fim de frase/pausa)

    def fecha(fim):
        if cur:
            grupos.append((list(cur), fim))
            cur.clear()

    for p in pal:
        if cur:
            txt = " ".join(_limpa(q["w"]) for q in cur + [p])
            if p["nova"] or p["a"] - cur[-1]["b"] > quebra:
                fecha(True)
            elif len(txt) > max_chars or len(cur) >= max_palavras:
                fecha(False)
        cur.append(p)
        if re.search(r"[.?!]$", p["w"]):
            fecha(True)
    fecha(True)
    # sem palavra sozinha no fim da frase: ela puxa a última palavra do bloco anterior ("é uma era | muito louca")
    for k in range(1, len(grupos)):
        (ant, fim_ant), (atual, fim) = grupos[k - 1], grupos[k]
        if len(atual) == 1 and not fim_ant and len(ant) >= 3:
            atual.insert(0, ant.pop())
    out = [{"a": g[0]["a"], "b": g[-1]["b"], "texto": " ".join(_limpa(q["w"]) for q in g).strip()} for g, _ in grupos if g]
    # cada bloco fica até o próximo começar (se o próximo vem logo), senão some 0,25 s depois da última palavra
    for k, bl in enumerate(out):
        nxt = out[k + 1]["a"] if k + 1 < len(out) else None
        bl["b"] = nxt if nxt is not None and nxt - bl["b"] < 0.6 else bl["b"] + 0.25
    for bl in out:
        for k, v in (trocas or {}).items():
            bl["texto"] = bl["texto"].replace(k, v)
    return [bl for bl in out if bl["texto"]]

def _cartela(texto, y, size, peso, sombra):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([100, 28, 400, peso])
    if sombra:                                  # sombra difusa e leve, só para ler sobre fundo claro
        sh = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sh).text((W // 2, y + 2), texto, font=f, fill=int(255 * sombra), anchor="mm")
        black = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        black.putalpha(sh.filter(ImageFilter.GaussianBlur(6)))
        im.alpha_composite(black)
    ImageDraw.Draw(im).text((W // 2, y), texto, font=f, fill=(255, 255, 255, 255), anchor="mm")
    return im

def render(saida, duracao, bls, y=1490, size=52, peso=520, sombra=0.35):   # ele: menor, menos bold, menos sombra; longe do rosto
    """Camada transparente 1080x1920 com a legenda (PNG em MOV). y: centro da linha. Corte seco entre blocos."""
    d = tempfile.mkdtemp(prefix="legenda_", dir=os.path.dirname(os.path.abspath(saida)))
    vazio = os.path.join(d, "vazio.png")
    Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(vazio)
    lst, t = [], 0
    q = lambda x: round(x * FPS)
    for k, bl in enumerate(bls):
        a, b = q(bl["a"]), q(bl["b"])
        if a > t:
            lst.append((vazio, a - t))
        p = os.path.join(d, f"{k:04d}.png")
        _cartela(bl["texto"], y, size, peso, sombra).save(p)
        lst.append((p, max(1, b - max(a, t))))
        t = max(b, t + 1)
    end = q(duracao)
    if end > t:
        lst.append((vazio, end - t))
    with open(os.path.join(d, "lista.txt"), "w") as fh:
        for p, n in lst:
            fh.write(f"file '{p}'\nduration {n / FPS:.6f}\n")
        fh.write(f"file '{lst[-1][0]}'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(d, "lista.txt"),
                    "-vf", f"fps={FPS},format=rgba", "-frames:v", str(end), "-c:v", "png", saida], check=True)
    return saida
