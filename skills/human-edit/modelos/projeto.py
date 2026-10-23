"""Projeto de edição: <NOME> (<assunto do vídeo>).

Copie para ~/Desktop/<NOME>_edicao/_projeto/projeto.py e preencha as seções na ordem do fluxo.
Exemplo completo e aprovado: ~/.claude/skills/human-edit/referencias/exemplo-img4565.py
Rodar: ~/Library/Caches/human-edit/venv/bin/python projeto.py corte | video | voz-bruta | voz | som SAIDA | tudo SAIDA
"""
import os, sys
sys.path.insert(0, os.path.expanduser("~/.claude/skills/human-edit/scripts"))
from edicao import Edicao
from som import Eventos

AQUI = os.path.dirname(os.path.abspath(__file__))
NOME = "NOME_DO_VIDEO"                                   # ex.: IMG_4700
SRC = os.path.expanduser("~/Downloads/NOME_DO_VIDEO.MOV")
ENTREGA = os.path.expanduser(f"~/Desktop/{NOME}_edicao")
CACHE = os.path.expanduser(f"~/Library/Caches/human-edit/{NOME}")
SFX = os.path.expanduser("~/Documents/sfx/33OTB-SFX")

PROMPT = ""                                              # jargões/nomes do vídeo (transcrição, legenda, checagem)
CORRECOES = {}                                           # grafia na legenda: {"como saiu": "como fica"}
E = Edicao(SRC, AQUI, CACHE, transcricao="transcricao.json", maxrate="20M")   # teto de bitrate: folhagem/movimento estoura o arquivo
# grade="eq=contrast=0.95:brightness=-0.008:saturation=1.04,vignette=angle=PI/6"  # menos contraste (luz de sol forte)
start, end, tl, fq = E.start, E.end, E.tl, E.fq

# ---------------- 1. PLANO (depois da decupagem) ----------------
# (rótulo, [(segmento, 1a palavra, última exclusiva)], ênfase, ajustes {a, b, nocut, cuts, split})
# Comente o porquê de cada ajuste: é o que salva a próxima rodada.
PLANO = [
    ("hook",   [(0, 0, None)], True,  {"split": True}),
    # ("passo1", [(5, 0, None)], False, {"split": True}),
    # ("cta",    [(40, 0, None)], False, {"nocut": True}),
]
E.cortar(PLANO)

# ---------------- 2. materiais ----------------
MOT_DIR = ""        # pasta dos motions de referência (montagens)
GRAV = ""           # gravação de tela
# M = {i: os.path.join(MOT_DIR, f) for i, f in enumerate(sorted(os.listdir(MOT_DIR))) if f.endswith(".mp4")}
PICKS = []          # [(arquivo, tempo[, "fit"])] para a faixa: momentos fortes, paletas alternando
PICKS_CHEIA = []    # [(arquivo, tempo)] para tela cheia: tipográficos, de impacto

# ---------------- 3. planos da gravação de tela ----------------
PLANOS = {k: {"src": GRAV, **v} for k, v in {
    # "nome": {"t": 12.0, "keys": [("S", cx, cy, largura), (tempo_da_fala, cx, cy, largura), ("E", cx, cy, largura)]},
    # "nome2": {"t": None, "sync": (t_gravacao, t_fala), "keys": [...]},
    # "nome3": {"t": 236.0, "freeze": True, "keys": [...]},
}.items()}

# ---------------- 4. split e tela cheia ----------------
FAIXAS = [
    # (0.5, [(end("hook"), ("montagem", PICKS, 0))], True, False),      # abertura: 0.5 s de rosto, depois o split
]
TELAS_CHEIAS = [
    # (end("hook"), tl(12.3), ("montagem", PICKS_CHEIA, 0)),
]

def sobreposicoes(E):
    return [
        # E.grade_storyboard(tl(...), tl(...), QUADROS),
        # E.pasta_mac(tl(...), tl(...), "nome-da-skill"),
        # E.legendas(CORRECOES, prompt=PROMPT),   # legenda simples, no estilo aprovado (padrão de legenda.md)
        # E.lettering(start("cta"), end("cta"), ["Comente “PALAVRA”", "pra receber na sua DM"]),
    ]

# ---------------- 5. efeitos sonoros ----------------
def eventos(E):
    ev = Eventos()
    # ev.ev(0.5, "Light Airy Whoosh.wav", -24, "peak")
    # ev.ticks(0.5, end("hook"))
    return ev

# ---------------- saídas ----------------
VIDEO = os.path.join(CACHE, "video.mp4")
BRUTA = os.path.join(AQUI, "voz_bruta.wav")       # o áudio bruto do corte que foi mandado isolar
ISOLADA = os.path.join(AQUI, "voz_isolada.wav")   # a voz isolada (Magnific) desse mesmo corte
VOZ = os.path.join(AQUI, "voz.wav")               # a voz limpa do corte atual (remontada a cada som)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "corte"
    final = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ENTREGA, f"{NOME}_corte.mp4")
    if cmd == "checar":                            # checagem tripla da fala: obrigatória antes de toda entrega
        E.checar(prompt=PROMPT)
    if cmd in ("video", "tudo"):
        E.video(VIDEO, FAIXAS, TELAS_CHEIAS, PLANOS, sobreposicoes)
    if cmd == "voz-bruta":                         # para mandar isolar (depois disso, não rode de novo)
        E.voz_bruta(BRUTA)
    if cmd in ("som", "tudo"):
        if os.path.exists(ISOLADA):                # voz isolada remontada para o corte atual
            E.voz(VOZ, ISOLADA, BRUTA)
            voz = VOZ
        else:                                      # antes do isolamento: a bruta do corte atual (o EQ já ajuda)
            voz = os.path.join(CACHE, "voz_previa.wav")
            E.voz_bruta(voz, para_isolar=False)
        E.som(VIDEO, voz, final, eventos(E), SFX)
