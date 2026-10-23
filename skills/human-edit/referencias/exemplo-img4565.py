"""Projeto de edição real (aprovado, v16): IMG_4565, tutorial da skill Human Motion Design, 5:38 bruto -> 1:07.

Exemplo completo de projeto.py: todas as decisões de uma edição de verdade, com o porquê ao lado.
Rodar:  python projeto.py corte | video | voz-bruta | voz | som | tudo
"""
import os, sys
sys.path.insert(0, os.path.expanduser("~/.claude/skills/human-edit/scripts"))
from edicao import Edicao
from som import Eventos

AQUI = os.path.dirname(os.path.abspath(__file__))
NOME = "IMG_4565"
SRC = os.path.expanduser("~/Downloads/IMG_4565.MOV")
ENTREGA = os.path.expanduser(f"~/Desktop/{NOME}_edicao")
CACHE = os.path.expanduser(f"~/Library/Caches/human-edit/{NOME}")
SFX = os.path.expanduser("~/Documents/sfx/33OTB-SFX")

E = Edicao(SRC, AQUI, CACHE, transcricao="transcript2.json")
start, end, tl, fq = E.start, E.end, E.tl, E.fq

# ---------------- PLANO: (rótulo, [(segmento, 1a palavra, última exclusiva)], ênfase, ajustes) ----------------
# ajustes: a/b = entrada/saída forçadas (s da fonte); split = clipe vive dentro do split; nocut = não corta pausas
# internas; cuts = cortes extras [(a, b)]. Cada ajuste aqui veio de um problema ouvido de verdade.
PLANO = [
    ("hook",       [(0, 0, None)],                                 True,  {"a": 3.92, "b": 6.434, "split": True}),  # o "i" de "aqui" vai até 6.43 (depois da explosão do k); o "ó" começa em 6.45
    ("dor",        [(8, 0, None)],                                 False, {"split": True, "a": 76.85}),  # um respiro antes do "Você" (ele pediu)
    ("resolver",   [(10, 0, None)],                                False, {"a": 86.10, "b": 87.24}),
    ("passo1",     [(16, 0, None)],                                False, {"split": True}),
    ("ajuda",      [(21, 0, None)],                                False),
    ("passo2",     [(28, 1, None), (29, 0, None), (30, 0, None)],  False, {"split": True, "a": 136.74, "b": 141.57}),  # termina em "Pinterest", sem o "e... traz"
    ("ativar",     [(33, 0, None)],                                False, {"split": True, "b": 152.70}),  # mantém o "t" de "chat"
    ("claude",     [(36, 0, None)],                                False, {"split": True}),
    ("importante", [(39, 0, None)],                                True),
    ("opus",       [(45, 0, None)],                                False, {"split": True, "a": 182.80, "nocut": True}),  # sem micro-corte no "5.5"
    ("assets",     [(48, 0, None)],                                False, {"split": True, "a": 195.28, "b": 197.87}),  # pula o "E depo-" abortado; mantém o "-ts"
    ("lista",      [(50, 0, None)],                                False, {"split": True, "b": 202.79}),  # para antes do "tu-"
    ("marca",      [(54, 0, None)],                                False),
    ("story",      [(56, 0, None), (57, 0, None)],                 False, {"split": True, "a": 218.27}),  # o segundo "aí"
    ("token",      [(58, 0, None)],                                False),
    ("estatico",   [(62, 0, None), (63, 0, None)],                 False),
    ("render",     [(65, 0, None), (66, 0, None)],                 False, {"cuts": [(253.47, 253.73)]}),  # encurta o "e..." arrastado
    ("animado",    [(71, 0, None)],                                False, {"a": 280.90, "b": 283.16}),  # só a segunda tentativa
    ("animado2",   [(74, 0, None)],                                False, {"a": 290.62}),
    ("cta",        [(79, 0, None)],                                False, {"nocut": True}),
    ("comenta",    [(86, 0, None)],                                True),   # o take limpo de "comenta skill" (sem "e-skill")
]
E.cortar(PLANO)

# ---------------- materiais ----------------
MOT_DIR = os.path.expanduser("~/Dropbox/BLACK INSERTS/HUMAN/motionAnimação board - Oct 11th 2026 (14 images)")
M = {int(f.split(".")[0]): os.path.join(MOT_DIR, f) for f in os.listdir(MOT_DIR) if f.endswith(".mp4")}
GRAV = os.path.expanduser("~/Desktop/Gravação de Tela 2026-10-11 às 16.56.08.mov")   # sem WhatsApp, seletor de perfil, Google
RESULTADO = os.path.expanduser("~/Movies/resiult2.mov")      # o motion final (4:3, 24 fps, 367 quadros, trilha muda)
RESULTADO_DUR = 367 / 24
QUADROS = [os.path.expanduser(f"~/Documents/fable/human-output/motion-design/human-motion-skill/storyboard/prancha/quadros/{q}.jpg")
           for q in ("01-scroll", "02-estatico", "03-tudo-move", "04-tres-verbos", "05-sem-limites",
                     "06-ideia", "07-continuo", "08-storyboard", "09-humanos", "10-marca")]

# montagem da faixa (3 cortes/s): (arquivo, tempo aproximado[, "fit"]); momentos mais fortes, paletas alternadas
PICKS = [(M[n], t, *m) for n, t, *m in [
    (2, 4.6), (10, 42.45), (11, 35.85), (4, 3.2, "fit"), (3, 2.0), (1, 1.2), (6, 3.0, "fit"), (9, 4.0, "fit"),
    (5, 13.6), (13, 53.6), (4, 12.6, "fit"), (12, 21.0), (10, 29.0, "fit"),
    (11, 4.4), (10, 13.3), (10, 27.4, "fit"), (13, 37.1), (9, 30.5), (10, 15.2), (13, 4.5), (12, 6.5, "fit"),
    (10, 80.0), (7, 2.6), (5, 9.6), (2, 10.0), (13, 61.0), (9, 16.3, "fit"), (12, 26.0), (8, 2.5), (13, 1.0, "fit")]]
# tela cheia: tipográficos e bonitos (ele trocou os 3D por tipográficos)
PICKS_CHEIA = [(M[n], t) for n, t in [
    (2, 0.9), (10, 27.4), (5, 13.6), (2, 8.4), (6, 3.0), (4, 10.6), (13, 61.0), (13, 53.6),
    (9, 4.0), (2, 12.2), (4, 12.6), (10, 13.3), (11, 4.4), (10, 29.0), (10, 15.2), (13, 4.5), (2, 25.3),
    (10, 80.0), (5, 9.6), (9, 30.5), (13, 37.1)]]

# ---------------- planos da gravação de tela (zoom acompanhando a fala) ----------------
# keys: (âncora, cx, cy, largura do recorte 4:3 em px da gravação); âncora "S" início, "E" fim, ou um tempo da fala
FIGMA = 236.0      # página do Figma com ícones, paleta e frames (quadro congelado)
PLANOS = {k: {"src": GRAV, **v} for k, v in {
    "drop":   {"t": None, "sync": (68.45, 151.26),  # as referências caem no chat no "joga"
               "keys": [("S", 1180, 905, 1000), (151.05, 1180, 905, 1000), (151.45, 1035, 1040, 640), ("E", 1035, 1040, 600)]},
    "agents": {"t": 217.0,  # card de 4 agentes com as bolinhas azuis (ele gosta da interface do Claude)
               "keys": [("S", 914, 740, 440), (160.45, 914, 740, 400), (160.95, 1000, 860, 560), ("E", 1000, 865, 520)]},
    "agents_start": {"t": 147.0, "keys": [("S", 914, 985, 440), ("E", 914, 985, 400)]},
    "opus":   {"t": None, "sync": (5.0, 185.94),  # o seletor para no Ultracode no "UltraCode" (sem cortar o rótulo)
               "keys": [("S", 1300, 995, 760), (183.25, 1300, 995, 760), (183.75, 1440, 1085, 540),
                        (184.70, 1460, 1110, 480), (185.90, 1470, 1115, 450), ("E", 1470, 1115, 430)]},
    "assets": {"t": FIGMA, "freeze": True,  # página inteira -> paleta no "assets"
               "keys": [("S", 1130, 700, 1400), (196.75, 1130, 700, 1400), (197.30, 625, 670, 540), ("E", 625, 672, 480)]},
    "logo":   {"t": FIGMA, "freeze": True, "keys": [("S", 1100, 420, 520), ("E", 1100, 420, 470)]},
    "imagem": {"t": FIGMA, "freeze": True, "keys": [("S", 1586, 985, 440), ("E", 1590, 990, 400)]},
    "textos": {"t": FIGMA, "freeze": True, "keys": [("S", 1586, 690, 440), ("E", 1600, 680, 400)]},
    "fundos": {"t": FIGMA, "freeze": True, "keys": [("S", 1093, 701, 520), ("E", 1093, 701, 470)]},
}.items()}

# ---------------- split: (início, [(fim do segmento, conteúdo)], entra deslizando, sai deslizando) ----------------
FAIXAS = [
    (0.5,               [(end("hook"), ("montagem", PICKS, 0))], True, False),   # 0.5 s só de rosto, depois o split; corte seco pra tela cheia
    (start("ativar"),   [(end("ativar"), "drop"), (end("claude"), "agents")], False, False),   # vem direto da tela cheia
    (start("opus"),     [(end("opus"), "opus"), (end("assets"), "assets"), (tl(200.98), "logo"), (tl(201.62), "imagem"),
                         (tl(202.10), "textos"), (end("lista"), "fundos")], True, False),
    (start("story"),    [(tl(220.20), "agents_start")], True, False),   # corte seco pro storyboard em tela cheia
    (start("token.2"),  [(start("cta"), ("video", RESULTADO, 0.0, RESULTADO_DUR / (start("cta") - start("token.2"))))], True, False),
    # ^ o resultado inteiro, só no split (nunca tela cheia), de "salva o seu tempo" até o CTA; sai no corte, sem deslizar
]
TELAS_CHEIAS = [
    (end("hook"), tl(79.60), ("montagem", PICKS_CHEIA, 0)),        # "você já deve ter visto... motion com o Claude"
    (tl(138.15), end("passo2"), ("montagem", PICKS_CHEIA, 8)),     # "faz uma pesquisa lá no Pinterest"
]

def sobreposicoes(E):
    return [
        E.grade_storyboard(tl(220.20), tl(222.48), QUADROS),       # "montar um storyboard" -> "pra te mostrar | mais ou menos"
        E.pasta_mac(tl(109.40), tl(110.75), "human-motion-design"),  # "essa skill aqui que eu fiz"
        E.lettering(start("cta"), end("comenta"), ["Comente “SKILL”", "pra receber agora na sua DM"]),  # entra no corte
    ]

# ---------------- efeitos sonoros (sutis, com cadência) ----------------
def eventos(E):
    ev = Eventos()
    WH = ["Light Airy Whoosh.wav", "Light Airy Whoosh 2.wav", "Light Airy Whoosh 3.wav"]
    ev.ev(0.5, WH[0], -24, "peak")                                   # o split entra
    ev.ticks(0.5, end("hook"))                                        # clique a cada corte da montagem
    ev.ev(end("hook") + 0.04, "Swoosh 05 - mid high.wav", -25, "peak", gate=end("hook"))   # nunca em cima do "aqui"
    ev.ticks(end("hook"), tl(79.60))
    ev.ev(tl(79.60), "Swoosh 02 - high.wav", -30, "peak")
    ev.ev(fq(tl(109.40)), "Instant Camera Button 1.wav", -27)         # a pasta aparece
    ev.ev(fq(tl(110.75)) - 0.12, "Swoosh 01 - high.wav", -34, "peak")
    ev.ev(tl(138.15), "Swoosh 05 - mid high.wav", -26, "peak")        # tela cheia do Pinterest
    ev.ticks(tl(138.15), end("passo2"))
    ev.ev(start("ativar"), WH[1], -27, "peak")
    ev.ev(tl(151.26), "Click.wav", -27)                               # as referências caem no chat
    ev.ev(end("ativar"), "Swoosh 03 - high.wav", -33, "peak")
    ev.ev(start("opus"), WH[2], -25, "peak")
    ev.ev(tl(185.94), "Instant Camera Button 1.wav", -28)             # o seletor para no Ultracode
    ev.ev(end("opus"), "Swoosh 01 - high.wav", -33, "peak")
    ev.ev(tl(197.30) - 0.25, "Swoosh 03 - high.wav", -34, "peak")     # zoom na paleta
    for s in (200.98, 201.62, 202.10):                                # logo / imagem / textos / fundos
        ev.ev(tl(s), "Click.wav", -31)
    ev.ev(fq(start("cta")), "Light Airy Whoosh 2.wav", -31, "peak")   # corte pro CTA
    ev.ev(start("story"), WH[0], -25, "peak")
    ev.ev(tl(220.20), "Swoosh 05 - mid high.wav", -28, "peak")        # entra o storyboard
    for i in (0, 3, 6, 9):                                            # cliques leves enquanto os quadros montam
        ev.ev(fq(tl(220.20)) + 0.05 + 0.06 * i + 0.1, "Click.wav", -37)
    ev.ev(tl(222.48) - 0.04, "Swoosh 02 - high.wav", -33, "peak")     # volta pro rosto
    ev.ev(start("token.2"), WH[1], -26, "peak")                       # entra o resultado
    vel = RESULTADO_DUR / (start("cta") - start("token.2"))
    rt = lambda r: fq(start("token.2")) + r / vel                     # tempo do resultado -> edição
    ev.ev(rt(12.29), "Light Airy Whoosh 3.wav", -33, "peak")          # flash do "Built by humans"
    ev.ev(rt(13.83), "Low Pan Impact.wav", -32, "peak")               # o logo HUMAN pousa
    return ev

# ---------------- saídas ----------------
VIDEO = os.path.join(CACHE, "video.mp4")           # só imagem (o som entra no passo "som")
VOZ = os.path.join(AQUI, "voz.wav")                # voz limpa do corte atual
ISOLADA = os.path.join(AQUI, "voz_isolada.wav")    # a voz isolada (Magnific) de um corte anterior
BRUTA = os.path.join(AQUI, "voz_bruta.wav")        # o áudio bruto desse mesmo corte (para realinhar)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "corte"
    final = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ENTREGA, f"{NOME}_corte.mp4")
    if cmd in ("video", "tudo"):
        E.video(VIDEO, FAIXAS, TELAS_CHEIAS, PLANOS, sobreposicoes)
    if cmd == "voz-bruta":
        E.voz_bruta(BRUTA)
    if cmd in ("som", "tudo"):
        if os.path.exists(ISOLADA):                # com a isolada, remonta a voz do corte atual
            E.voz(VOZ, ISOLADA, BRUTA)
        E.som(VIDEO, VOZ, final, eventos(E), SFX)  # neste projeto, voz.wav já é a voz limpa do corte aprovado
