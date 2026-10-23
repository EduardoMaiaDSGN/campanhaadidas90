# Human Edit

Edição de vídeos falados para Reels, TikTok e Shorts, no padrão que aprovamos no vídeo da skill Human Motion
Design (IMG_4565, 16 versões até ficar do jeito certo).

## Como usar

Mande o vídeo bruto e diga "edita esse vídeo". Junto, se tiver:

- motions de referência para as montagens;
- a gravação de tela do processo;
- o resultado final (o vídeo pronto do projeto);
- o storyboard;
- a frase do CTA.

O Claude faz a decupagem, te manda opções de gancho e entrega versões numeradas na pasta
`~/Desktop/<NOME>_edicao/`. Você responde com os tempos do que quer mudar ("0:26 sobra algo antes de 'os
melhores'"), do mesmo jeito que fizemos.

## O que já vem no padrão

- Corte sem nenhum respiro, com jump cuts, sem comer o fim das palavras (conferido no espectrograma).
- Rosto sempre no enquadramento original, sem zoom.
- Gancho com 0,5 s de rosto e depois o split com montagem de motions a 3 cortes/s.
- Split 4:3 em cima, com a faixa quase comendo um pouquinho do boné. Gravação de tela com zoom acompanhando a fala.
- Tela cheia de vez em quando. Storyboard em grid 100% de 2 colunas.
- O resultado final inteiro, só no split, até o CTA.
- Pasta do Finder para ilustrar a skill.
- CTA discreto: branco, sem sombra, sem caixa, entrando no corte.
- Voz isolada e com EQ mais agudo, a −14 LUFS. Efeitos sonoros sutis, com cliques.

O isolamento de voz usa créditos do Magnific: o Claude mostra o custo e pede ok antes.

## Onde está cada coisa

- `SKILL.md`: as instruções para o Claude.
- `referencias/estilo.md`: o gosto, regra por regra, com o motivo. **As correções novas que valem para os
  próximos vídeos entram aqui**, na seção "Aprendizados novos".
- `referencias/corte.md`, `insertos.md`, `som.md`, `pipeline.md`: o como.
- `referencias/exemplo-img4565.py`: a edição aprovada inteira, refeita com a skill. Ela reproduz o v16 quadro a
  quadro e amostra a amostra.
- `scripts/`: as ferramentas. Na primeira vez, o Claude roda `scripts/preparar.sh`.
- `modelos/projeto.py`: o ponto de partida de cada vídeo novo.

Requisitos: Mac com Apple Silicon, ffmpeg e uv (Homebrew), Xcode Command Line Tools. A biblioteca de efeitos
fica em `~/Documents/sfx/33OTB-SFX/`.
