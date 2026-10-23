# Inserts: o que existe e como declarar no projeto.py

Todo insert se ancora na fala: `start("rotulo")`, `end("rotulo")` ou `tl(tempo_da_fonte)` (o momento exato de
uma palavra no bruto). Assim, se o corte muda, os inserts andam junto.

## Pedir e conhecer os materiais

- Diga para qual fala é cada material ("quando você falar de assets, mostra a paleta do Figma"). Ele costuma
  mandar: motions de referência (para montagem), uma gravação de tela do processo, o resultado final, o
  storyboard, prints.
- **Gravação de tela:** faça folhas de contato (`conferir.py quadros GRAV.mov t1 t2 ...`) para achar os momentos.
  Anote o tempo de cada coisa (o seletor de modelo, o arquivo caindo no chat, o card de agentes, a paleta) e os
  trechos proibidos (WhatsApp, seletor de perfil, Google, qualquer dado pessoal).
- **Motions de referência:** folha de contato de cada arquivo (1 quadro/s) e escolha os momentos mais fortes:
  tipografia grande, luz, mudança de cor. `best_start` acha sozinho a janela de 10 quadros mais animada perto do
  tempo indicado, sem atravessar um corte do próprio vídeo.
- **Storyboard:** procure os quadros originais em alta (por exemplo `.../storyboard/prancha/quadros/*.jpg`, num
  projeto do Human Motion Design). Um print de 1200 px fica borrado em tela cheia.
- **Resultado:** confira a duração real em quadros (`ffprobe -count_frames`); a duração do container pode mentir.

## Buscar material na internet (quando ele pede "pega umas propagandas, uns prints, um vídeo")

1. **Comece pela página oficial do produto** (ex.: openai.com/pt-BR/index/introducing-dots). Ela costuma ter o filme
   de lançamento, gravações de tela da interface, cards do produto em uso em alta (3840 px) e animações dos
   personagens. Liste a mídia da página pelo navegador (`<video>`, `<iframe>` do Vimeo/YouTube, `<img>` grandes,
   `performance.getEntriesByType('resource')` para o que carregou sozinho).
2. **Antes de baixar, peça ok** com a lista: arquivo, fonte e tamanho (`yt-dlp --simulate`, `curl -I`).
3. **Baixe para `<NOME>_edicao/_materiais/`.** `yt-dlp` para YouTube e Vimeo (no Vimeo embutido, use
   `--referer https://site-oficial/`). Se o YouTube der 403, o mesmo filme costuma estar embutido na página oficial
   pelo Vimeo.
4. **Posts de gente usando** (X, Instagram) pedem login: não entre na conta dele. Peça que ele faça login no
   navegador lateral, que autorize usar o Chrome dele ou que mande os links/prints. Product Hunt e afins podem ter
   verificação anti-robô: pule.
5. **Assista tudo antes de escolher:** folha de contato de cada vídeo (`ffmpeg ... fps=1/3,tile=7x7`) e uma grade
   de coordenadas sobre cada card/print para posicionar os zooms (os `keys` usam pixels do arquivo original).
6. Prefira o que **mostra a fala**: o card do dot fazendo uma proposta em "mandar uma proposta", o rascunho no
   Gmail em "ver tudo no meu e-mail", a agenda no celular em "baseado na sua agenda".

## Faixa do split (`FAIXAS`)

```python
FAIXAS = [
  # (início, [(fim do segmento, conteúdo), ...], entra deslizando, sai deslizando)
  (0.5, [(end("hook"), ("montagem", PICKS, 0))], True, False),
  (start("opus"), [(end("opus"), "opus"), (end("assets"), "assets"), (tl(200.98), "logo")], True, False),
  (start("token.2"), [(start("cta"), ("video", RESULTADO, 0.0, vel))], True, False),
]
```

Conteúdos possíveis de um segmento:

- `("montagem", PICKS, primeiro)`: 3 cortes/s. `PICKS = [(arquivo, tempo[, "fit"])]`. "fit" põe o quadro 16:9
  inteiro sobre uma cópia desfocada (para quando a tipografia não cabe no recorte 4:3). `primeiro` é o índice
  inicial na lista, para duas montagens não repetirem os mesmos momentos.
- `"nome_do_plano"`: um plano da gravação de tela, de `PLANOS` (abaixo).
- `("video", arquivo, a_partir_de, velocidade[, "fit"])`: um vídeo pronto tocando na faixa. Por padrão preenche a
  faixa 4:3 cortando as laterais (16:9 perde ~12% de cada lado); `"fit"` mostra o quadro inteiro sobre uma cópia
  desfocada. Para o resultado inteiro
  terminar no corte: `vel = duração_real / (fim - início)`, mantendo `vel` entre 0,96 e 1,04.
- uma função `f(n_quadros, saida)` que renderiza algo próprio na faixa (1080×810, 30 fps).

O rosto desce sozinho em cada clipe que cai dentro de uma faixa (medido pela detecção de rosto, com
`cap_gap=-12`).

## Planos de gravação de tela (`PLANOS`)

```python
PLANOS = {k: {"src": GRAV, **v} for k, v in {
  "opus": {"t": None, "sync": (5.0, 185.94),        # o momento 5.0 s da gravação cai na palavra 185.94 da fala
           "keys": [("S", 1300, 995, 760), (183.25, 1300, 995, 760), (183.75, 1440, 1085, 540), ("E", 1470, 1115, 430)]},
  "assets": {"t": 236.0, "freeze": True,             # quadro congelado da gravação
             "keys": [("S", 1130, 700, 1400), (197.30, 625, 670, 540), ("E", 625, 672, 480)]},
}.items()}
```

- `keys`: `(âncora, cx, cy, largura)`. A âncora é `"S"` (início do segmento), `"E"` (fim) ou um tempo da fala, e
  é nesse momento que o recorte chega ali. `cx, cy` é o centro do recorte, `largura` a largura do recorte 4:3, em
  pixels da gravação. Entre as keys o movimento é suavizado. Cada corte tem um "pop" (zoom rápido de 16% assentando
  em 0,22 s).
- `t`: onde a gravação começa. `sync=(t_gravação, t_fala)` em vez de `t` faz o momento da gravação coincidir com
  a palavra (o arquivo caindo no chat exatamente no "joga").
- `freeze`: usa um único quadro (telas paradas, como Figma ou uma página).
- **Leitura:** largura de ~400–600 px numa tela de 2048 deixa o texto da interface grande e nítido. Confira que
  nenhum rótulo importante encosta na borda.

## Tela cheia (`TELAS_CHEIAS`)

```python
TELAS_CHEIAS = [
  (end("hook"), tl(79.60), ("montagem", PICKS_CHEIA, 0)),   # vertical preenche; 16:9 inteiro sobre desfoque
  (tl(138.15), end("passo2"), ("montagem", PICKS_CHEIA, 8)),
]
```

Corte seco na entrada e na saída; cobre o rosto e a faixa. Também aceita `("video", arquivo, a_partir_de, vel)`
e um arquivo já renderizado. Um 4º elemento `True` coloca por cima da grade de cor (para fundos claros e limpos).

## Sobreposições (função `sobreposicoes(E)`)

Rodam depois do corte montado, porque algumas precisam saber onde está o rosto. Devolvem a lista.

- `E.grade_storyboard(a, b, QUADROS)`: o storyboard em grid 100%, 2 colunas (usa só linhas completas: 10 quadros
  dão 2×5). Os quadros montam um a um e o grid faz um push-in lento. Fica por cima da grade de cor.
- `E.pasta_mac(a, b, "nome-da-skill")`: a pasta azul do Finder sobre a cabeça, com o nome embaixo. ~1,2 s.
- `E.sobre_cabeca(a, b, video_fundo_preto, largura=1000)`: um vídeo curto em fundo preto (personagens, logo
  animado, mascote) aparece sobre a cabeça, sem fundo (o preto vira transparência), com pop de entrada e saída.
  Ele adorou ver "as carinhas se mexendo" (os dots se transformando em cima da cabeça dele em "o dot é seu agente
  pessoal"). **Nada em cima do rosto:** o padrão (640 px de largura, centro 320 px acima do topo do boné) deixa folga
  mesmo quando a cabeça sobe; com 1000 px o personagem encostou no boné e virou "chapéu".
- Um card ou print estático também pode ser plano de tela: `{"src": "card.png", "t": 0, "freeze": True, "keys": [...]}`.
  O mesmo vale para um vídeo de interface (`"src": "video.mp4"` sem freeze), com zoom acompanhando a fala.
- `E.lettering(a, b, ["linha 1", "linha 2"])`: o CTA no estilo aprovado. Opções: `base` (y da primeira linha,
  padrão 290), `size` (52), `peso` (470), `escurecer` (0.13; 0 tira o escurecido do topo).

## Ordem que funciona num tutorial (do vídeo aprovado)

1. Gancho: rosto 0,5 s → split com montagem → tela cheia de motions na fala da dor.
2. Cada passo que tem tela: split com a gravação de tela sincronizada à fala.
3. Um momento visual forte no meio (storyboard em tela cheia, ~2 s).
4. O resultado inteiro no split, terminando no corte para o CTA.
5. CTA: rosto, lettering discreto no topo entrando no corte.

Entre os blocos, deixe trechos só de rosto: o contraste entre rosto e insert também é ritmo.
