# Legenda

`E.legendas(CORRECOES, prompt=..., trocas=...)` dentro de `sobreposicoes(E)` gera a legenda do vídeo inteiro.

## Como funciona

1. Transcreve o **áudio já cortado**. O tempo já é o da edição, e o que foi cortado não aparece.
2. Quebra em blocos de **uma linha**: no máximo 22 caracteres e 4 palavras, quebrando no fim de frase, antes de uma
   frase nova e em pausas. Nunca mistura o fim de uma frase com o começo da outra. Palavra sozinha no fim da frase
   puxa uma do bloco anterior ("é uma era | muito louca").
3. Grava os blocos em `_projeto/legendas.json`. **Revise o texto ali**: grafia de marcas e palavras que o whisper
   ouviu errado. Enquanto o corte não mudar, o arquivo editado é respeitado. Se o corte mudar, a legenda é refeita e a
   anterior vai para `legendas_antigas.json`, para copiar as correções.
4. Renderiza uma camada transparente por cima da grade de cor. Os blocos entram e saem no corte seco, sem animação.

## Ajustes do texto

- `correcoes={"dots": "Dots", "codec": "Codex", "mit": "Meet", "para": "pra", "está": "tá"}`: troca por palavra, sem
  diferenciar maiúsculas. Os valores contam como nomes próprios e mantêm a grafia. Ele fala "pra", "tá", "tô"; o
  whisper escreve "para", "está", "estou". A legenda acompanha a fala.
- `trocas={"24 barra 7": "24/7"}`: troca por trecho, no texto final do bloco.
- `minusculas=True` (padrão): tudo em minúscula, menos nomes próprios e siglas. Evita a maiúscula solta no meio da
  frase quando o bloco quebra.
- O hífen que o whisper separa ("e -mail") é colado sozinho.

## Estilo (padrão aprovado: use direto, sem perguntar)

Ele aprovou a legenda do IMG_4831 v3 e pediu: "quando for botar legenda, pode botar essa como padrão já". Os valores
abaixo já são o padrão de `E.legendas(...)`; só mude se ele pedir.

Branca, SF Pro com peso 520, 52 px, centralizada, com o centro da linha em y = 1490: no peito, abaixo da barba
mesmo quando o split empurra o rosto para baixo, e acima da interface do Reels. Ele pediu: "toma cuidado para a
legenda não ficar muito em cima do rosto". Tem uma **sombra difusa bem leve** (0.35, blur 6): sem ela, a letra branca some sobre roupa
clara e céu. É o único texto com sombra; o CTA continua sem. A primeira versão (58 px, peso 620, sombra 0.55,
y 1330) ele achou grande, bold e com sombra demais: "um pouquinho menor, menos bold, com menos sombra, mais para
baixo". Para mudar, passe para `E.legendas(...)`: `y`, `size`, `peso`,
`sombra` (0 = sem).
