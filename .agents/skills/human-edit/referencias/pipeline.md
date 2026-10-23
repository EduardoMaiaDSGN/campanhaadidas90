# Pipeline: comandos, o projeto.py e os tropeços conhecidos

## Comandos

```
PY=~/Library/Caches/human-edit/venv/bin/python        # depois de scripts/preparar.sh
SK=~/.claude/skills/human-edit/scripts
cd ~/Desktop/<NOME>_edicao/_projeto

$PY $SK/transcrever.py BRUTO.MOV transcricao.json --prompt "jargões"
$PY projeto.py corte              # monta o corte (edl.json) e imprime a linha do tempo (segundos)
$PY projeto.py video              # renderiza a imagem (faixas, telas cheias, sobreposições) -> cache/video.mp4
$PY projeto.py voz-bruta          # áudio bruto do corte atual para mandar isolar + edl_isolada.json (uma vez)
$PY projeto.py som SAIDA.mp4      # remonta a voz limpa do corte atual + efeitos + -14 LUFS, montado no vídeo
$PY projeto.py tudo SAIDA.mp4     # video + som
$PY $SK/auditar.py edl.json CACHE/audio16k.wav --prompt "..."
$PY $SK/conferir.py espectro|palavra|comparar|volume|quadros ...
```

Rode comandos longos em segundo plano. O primeiro `video` leva ~10 min (renderiza todos os clipes). Depois o
cache reaproveita tudo que não mudou: ajuste de sobreposição ou de faixa leva 2–4 min, `som` menos de 1 min.

## Anatomia do projeto.py (modelo em `modelos/projeto.py`; exemplo real em `referencias/exemplo-img4565.py`)

1. `E = Edicao(SRC, pasta_do_projeto, CACHE, transcricao=...)`. A partir daqui o diretório atual é o cache.
   Use caminhos absolutos.
2. `PLANO` e `E.cortar(PLANO)`. A linha do tempo fica disponível em `start(rótulo)`, `end(rótulo)`,
   `tl(tempo_da_fonte)` e `fq(t)` (arredonda para o quadro).
3. Materiais (caminhos), `PICKS`, `PLANOS`, `FAIXAS`, `TELAS_CHEIAS`, `sobreposicoes(E)`, `eventos(E)`.
4. As saídas e o bloco de comandos.

## Cache

- Fica em `~/Library/Caches/human-edit/<NOME>/`. Cada peça é guardada pelo **conteúdo**: o nome do arquivo é um
  hash do que a gerou. Mudou o corte, um tempo, uma key ou a lista de picks: o nome muda e a peça é refeita.
  Nada precisa ser apagado à mão.
- `clipes_<hash>/assembled.mov` é o corte montado, com o rosto sempre no enquadramento original.
- Pode apagar o cache inteiro a qualquer hora: tudo se refaz a partir do `_projeto`.

## Tropeços conhecidos (e o que fazer)

- **"tempo da fonte X não está no corte":** as bordas dos clipes ficam alinhadas a 1/30 s. Se o clipe começa
  em 253.7333, `tl(253.73)` cai fora; use um tempo de dentro (253.75).
- **Vídeo que "acaba antes":** a duração do container mente. Conte os quadros (`ffprobe -count_frames`). Uma
  sobreposição curta deixa aparecer o que está embaixo nos últimos quadros. O `("video", ...)` já completa com o
  último quadro, mas confira.
- **Vídeo de 24 fps na timeline de 30:** o `fps=30` duplica quadros, e ajustar a velocidade usa `setpts`. Até ~4%
  não se percebe.
- **Bruto em 4K (2160×3840):** os clipes descem para 1080×1920 sozinhos (`compor.render_clips`). O primeiro
  render fica mais lento, porque decodificar 4K HEVC pesa.
- **Arquivo pesado demais:** folhagem e câmera andando fazem o crf 17 passar de 50 Mbps (528 MB para 1:14). Use
  `Edicao(..., maxrate="20M")` (já vem no modelo). O Instagram recomprime para poucos Mbps de qualquer jeito.
- **Gravação externa:** o corte se adapta ao ruído sozinho (veja corte.md §6). Isole a voz, que com vento faz muita
  diferença.
- **ffmpeg sem `drawtext`:** todo texto é desenhado com PIL (lettering.py, pasta_mac.py).
- **Detecção de rosto:** é a Vision da Apple (`scripts/faces`, compilado pelo preparar.sh). Haar do OpenCV falha
  em barba e boné; não volte para ele.
- **zsh:** um glob sem resultado aborta o comando inteiro (`rm work/*.mov` com zero arquivos não apaga mais nada).
  Prefira `find ... -delete` ou deixe o cache cuidar disso.
- **Pasta temporária da sessão** é apagada entre sessões: nada importante ali. O `_projeto` no Desktop guarda o
  que é necessário para refazer tudo (projeto.py, transcrição, edl.json, vozes).
- **Áudio do resultado:** costuma vir mudo (trilha de silêncio). Confira com `volumedetect` antes de contar com ele.
- **Whisper:** estica a primeira palavra sobre o silêncio de antes (o cortador já compensa) e completa palavras
  cortadas (veja corte.md). Com `condition_on_previous_text=False`, um erro não contamina os takes seguintes.

## Provar que um ajuste não estragou nada

```
$PY $SK/conferir.py comparar NOVO.mp4 ANTERIOR.mp4 --ignorar 39.2-44.8 62.0-68
```

Compara um quadro a cada 0,7 s fora dos trechos ignorados. PSNR 138 = idêntico. 46–50 = só ruído de
codificação, normal perto de um trecho mexido. Abaixo de 40 = mudou de verdade: investigue antes de mandar.
