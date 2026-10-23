# Som: voz tratada e efeitos sutis

O som final sai do `projeto.py som`. Ele pega a voz limpa do corte (`voz.wav`) e passa pela cadeia de EQ.
Depois soma os efeitos dos `eventos(E)`, normaliza para −14 LUFS e junta tudo no vídeo, sem recodificar a imagem.

## Voz

### Cadeia (scripts/som.py, CADEIA_VOZ)

high-pass 80 Hz → −2,5 dB em 250 Hz (tira o embolado) → +3 dB em 3,2 kHz (presença) → +4 dB acima de 6,5 kHz e
exciter (o "agudinho" que a voz do iPhone pedia) → de-esser → compressor 3:1. Loudnorm em duas passadas para
**−17 LUFS em mono**: a conversão mono→estéreo soma +3 LU, então o arquivo entregue fica em **−14 LUFS** (o
padrão do Instagram), com pico perto de −4 dBTP.

### Isolamento (uma vez, quando o corte estabilizar)

Áudio de celular tem sala e ruído; o EQ sozinho não resolve. O isolamento por IA (Magnific `audio_isolate`,
ElevenLabs Voice Isolator) resolve, mas **gasta créditos**: cerca de 270 por 1 minuto de corte. Por isso ele é
feito só uma vez, e as versões seguintes reaproveitam a voz isolada.

1. `projeto.py video` e depois `projeto.py voz-bruta`. Saem `voz_bruta.wav`, o áudio bruto do corte atual, e
   `edl_isolada.json`, o corte a que esse áudio corresponde.
2. `simulate_cost` do `audio_isolate` → **diga o custo e peça ok.**
3. Suba o arquivo: `creations_request_upload` → `curl -X PUT` na URL devolvida → `creations_finalize_upload`.
4. `audio_isolate` com o arquivo e espere a criação ficar pronta. (`audio_clean_speech` não estava liberado na
   conta dele.)
5. Baixe o resultado e converta para wav 48 kHz mono: `_projeto/voz_isolada.wav`. Não rode `voz-bruta` de novo
   depois disso: ela e o `edl_isolada.json` precisam continuar sendo do corte que foi isolado.
6. A partir daí, todo `projeto.py som` remonta o `voz.wav` do corte atual sozinho.

### Recortes depois do isolamento (scripts/voz.py, chamado pelo `som`)

- Cada pedaço de fonte que o corte isolado já tinha vem do áudio isolado. Cada clipe é realinhado contra a voz
  bruta, porque o isolado pode escorregar até ~8 ms.
- O que é novo vem da fonte bruta, com fade de 5 ms. Exemplo: o "i" de um "aqui" que antes estava cortado.
  - Uma **cauda longa** (> 0,12 s, que tem uma vogal inteira) fica em volume cheio e só os últimos 25 ms descem.
  - Uma **cauda curta** é só decaimento e desce inteira. Ela também pode conter o começo da próxima palavra.
- Ar novo no começo de um clipe vira silêncio. Uma pausa devolvida ao corte, sem nada acima do piso de ruído,
  também vira silêncio: na rua, a pausa bruta é vento, e soaria como um sopro entre duas palavras limpas.
- Se o corte mudar muito (falas novas inteiras), vale isolar de novo, avisando o custo.

**Antes do isolamento** (v1, v2), o `som` usa a voz bruta do corte atual. A cadeia de EQ já melhora bastante.

## Efeitos sonoros

Biblioteca dele: `~/Documents/sfx/33OTB-SFX/`. Os níveis são **pico em dBFS antes do reforço**: o som.py soma
+8 dB nos whooshes e +10 dB nos cliques (`Click.wav`, `Instant Camera Button 1.wav`). Com os números abaixo,
os efeitos ficam com pico em ~−16 dBFS, cerca de 11 dB abaixo das partes fortes da voz: presentes no
celular, sem aparecer demais.

| momento | arquivo | nível | alinhamento |
|---|---|---|---|
| faixa do split entra | Light Airy Whoosh (1, 2 ou 3, alternando) | −24 a −27 | peak no início |
| cada corte de montagem | Click.wav (`ev.ticks(a, b)`) | −34 | start |
| entra tela cheia | Swoosh 05 - mid high | −25 a −28 | peak no corte |
| sai tela cheia / troca de plano | Swoosh 01/02/03 - high | −30 a −34 | peak no corte |
| momento de interface (arquivo cai, seletor para) | Click.wav / Instant Camera Button 1 | −27 a −28 | start |
| itens de uma lista na tela | Click.wav | −31 | start |
| pasta do Finder aparece / some | Instant Camera Button 1 / Swoosh 01 | −27 / −34 | start / peak |
| storyboard montando | Click.wav, 4 cliques leves | −37 | start |
| CTA entra | Light Airy Whoosh 2 | −31 | peak no corte |
| logo pousando no resultado | Low Pan Impact | −32 | peak |

```python
def eventos(E):
    ev = Eventos()
    ev.ev(0.5, "Light Airy Whoosh.wav", -24, "peak")
    ev.ticks(0.5, end("hook"))
    ev.ev(end("hook") + 0.04, "Swoosh 05 - mid high.wav", -25, "peak", gate=end("hook"))
    return ev
```

- `"peak"` põe o momento mais forte do som no tempo dado. É o certo para whooshes em cortes.
- **`gate=tempo`** silencia o som antes desse tempo. Use no whoosh que entra logo depois de uma fala: a subida
  do whoosh (os ~150 ms antes do pico) tapa a última sílaba. Foi metade do problema do "aqui".
- Cadência: um efeito a cada 1–3 s nos trechos com insert. Trechos só de rosto podem ficar sem efeito.
- Para medir: `stems=pasta` no `som.mixar` salva voz e efeitos separados; compare o nível dos dois no trecho
  suspeito.
