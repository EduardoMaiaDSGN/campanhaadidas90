# Decupagem e corte

O bruto de um vídeo de fala tem vários takes de cada frase, falsos começos e pausas para pensar. O trabalho aqui
é escolher a melhor versão de cada fala, colar sem respiro e garantir que nenhuma palavra perca um pedaço.

## 1. Transcrever

```
PY=~/Library/Caches/human-edit/venv/bin/python
$PY ~/.claude/skills/human-edit/scripts/transcrever.py BRUTO.MOV _projeto/transcricao.json \
    --prompt "Assunto do vídeo. Nomes: Claude Code, Opus, Figma, a marca dele..."
```

O prompt ajuda o whisper a escrever certo os nomes próprios e os termos técnicos. A saída lista os segmentos
numerados (`#12 [108.17 - 111.37] O primeiro passo é...`). O PLANO usa esses números.

## 2. Mapa fala × takes (decupagem.md)

- Agrupe os segmentos pela **fala** (a mesma frase dita de novo é outro take). Em geral ele grava as falas em
  ordem e repete cada uma de 2 a 6 vezes.
- Para cada fala, escolha o take **completo, fluente, sem tropeço e com energia**. Na dúvida, prefira o último
  take limpo: ele costuma melhorar a cada tentativa.
- **Um segmento do whisper pode esconder um recomeço** ("Hoje o... hoje eu vou te ensinar"). Quando a primeira
  palavra tem uma duração absurda (o whisper "estica" a palavra sobre a pausa) ou o texto repete o começo, ouça o
  trecho (`conferir.py palavra`) e force a entrada (`a`) no recomeço.
- Escreva `decupagem.md` na pasta de entrega: as falas na ordem do vídeo, o take escolhido (tempo) e, numa linha,
  o porquê. Ajuda nas próximas rodadas e mostra a ele o que você ouviu.
- **Gancho:** proponha 3–4 aberturas (promessa, provocação, confissão, take alternativo da mesma frase) com o texto
  de cada uma. Se ele pedir para ver, renderize só a abertura de cada uma com o split (um `projeto.py` com um PLANO
  curto por opção).

## 3. O PLANO

```python
PLANO = [
  # (rótulo, [(segmento, 1a palavra, última exclusiva)], ênfase, ajustes)
  ("hook",   [(0, 0, None)],              True,  {"a": 3.92, "b": 6.434, "split": True}),
  ("passo2", [(28, 1, None), (29, 0, None)], False, {"split": True, "b": 141.57}),
  ("render", [(65, 0, None), (66, 0, None)], False, {"cuts": [(253.47, 253.73)]}),
]
```

- Vários segmentos num item = uma fala que o whisper quebrou em duas.
- Ajustes: `a`/`b` (entrada e saída forçadas, em s da fonte), `nocut` (não corta pausas internas: use em números
  e siglas, como "5.5", ou em falas com respiração natural), `cuts` (cortes extras, por exemplo um "e..."
  arrastado), `split` (o clipe vive dentro de um split; só informativo).
- **Rótulos importam:** os inserts e os efeitos se ancoram neles (`start("opus")`, `end("hook")`). Um item cortado
  em pedaços vira `opus.1`, `opus.2`... e `start("opus")` pega o primeiro.

## 4. O que o cortador faz sozinho (scripts/corte.py)

- Analisa o áudio de 10 em 10 ms (energia + "planura" do espectro) e separa o que é **voz** (vogais e consoantes
  sonoras) do que é **som** (fricativas, finais, respiro) e do que é **silêncio**.
- **Bordas:** a entrada vai até o início da primeira palavra, com a consoante inicial. A saída vai até o fim da
  última palavra, com a cauda surda (s, t, ch), atravessando oclusões curtas.
- **Pausas e respiros** com mais de 0,10 s viram jump cut, protegendo ~120 ms de cauda e ~100 ms de ataque.
  Pausas **dentro de uma palavra** (pelo tempo do whisper, quando confiável) nunca são cortadas, nem na primeira e
  na última palavra. Pedaços minúsculos são fundidos (nada pisca).
- **Nunca repete áudio:** se dois clipes se sobrepõem na fonte, o segundo começa onde o primeiro acaba.
- **Tudo alinhado ao quadro (1/30 s).** Um `b` de 6.434 vira 6.4333.

## 5. Onde o automático erra (e como consertar)

| sintoma | causa | conserto |
|---|---|---|
| sobra um pedaço antes da primeira palavra ("…os melhores") | resto do take anterior / respiro | `a` logo antes da palavra |
| a última consoante some ("cha-", "asse-") | a cauda surda é fraca | `b` no fim da explosão/fricativa (veja o espectrograma) |
| **a vogal final some depois de uma oclusiva** ("aq-") | o cortador para na explosão do k; o "i" vem depois, mais fraco | `b` no fim da vogal, antes da próxima palavra (abaixo) |
| a palavra é seguida de outra colada ("aqui, ó") | não há pausa entre elas | corte no fim da vogal, antes de os formantes começarem a mudar |
| micro-corte no meio da palavra | o tempo do whisper estava errado | `nocut` no item, ou bordas manuais |
| frase dita duas vezes no mesmo clipe | recomeço dentro do segmento | `a`/`b` para ficar com uma |
| "e…" arrastado entre frases | hesitação | `cuts` |

### Conferir o fim de uma palavra (obrigatório em cada fala que termina em vogal fraca)

O whisper **completa a palavra que espera ouvir.** Transcrevendo a frase inteira, ele escreveu "como esses aqui"
três versões seguidas, com o "i" cortado. Só o espectrograma e a transcrição do trecho isolado mostram a verdade:

```
$PY scripts/conferir.py espectro BRUTO.MOV 5.75 6.80 --marcas 6.333 --saida esp.png   # olhe a imagem
$PY scripts/conferir.py palavra FINAL.mp4 2.17 2.72                                  # só o trecho final
```

No espectrograma (0–5 kHz):

- vogal = faixas horizontais escuras (formantes);
- oclusiva = um buraco claro (a oclusão) e depois uma listra vertical (a explosão);
- "aqui" = "a" forte | buraco do k | explosão | "i" fraco, com o 1º formante baixo (~300 Hz) e o 2º alto (~2 kHz).

O corte precisa vir **depois do "i"**, não na explosão. Se outra palavra emenda ("ó"), corte onde o 1º formante
começa a subir e o 2º a cair, com um fade de ~25 ms (o `voz.py` já faz isso nas caudas longas).

`palavra` transcreve só o trecho, sem contexto. Com o "i" cortado saiu "Obrigado."; com o "i" inteiro saiu
"Aqui." Isso é prova; a transcrição da frase inteira não é.

## 6. Gravação externa (vento, rua, parque)

O cortador foi calibrado dentro de casa, com piso de ruído perto de −70 dB. Andando no parque (IMG_4831) o piso fica
em −35 a −40 dB, e com os limiares fixos tudo vira "voz": o corte sai sem nenhum jump cut. O `corte.carregar`
detecta isso sozinho (piso acima de −50 dB) e passa a:

- analisar uma cópia sem o grave do vento (passa-alta de 150 Hz);
- usar limiares que acompanham o piso (voz > piso + 9 dB, som > piso + 4 dB);
- só cortar pausas acima de 0,18 s. Com vento, o silêncio de uma oclusiva ("c", "p", "t") parece pausa e era
  cortado no meio da palavra.

Isso aparece na saída como "gravação com ruído: piso ...". Em gravação de sala nada muda. Mesmo assim:

- **Falsos começos ficam mais frequentes andando** ("Então ele vai te...", "Ele pode es-"): confira as emendas.
- **Palavra "esticada" esconde retake.** Quando ele repete um pedaço ("ele consegue... ele consegue prever",
  "você não precisa estar com... não precisa estar com"), o whisper costuma escrever uma vez só e esticar uma
  palavra sobre as duas tentativas (1–1,6 s numa palavra de 0,3 s). `conferir.py esticadas transcricao.json edl.json`
  lista essas palavras dentro do corte. Transcreva cada uma isolada (`palavra`) e corte a primeira tentativa com
  `cuts`. Isso pegou as duas "falas duplicadas" do IMG_4831.
- **O `auditar.py` desalinha** com vento: ele acusa "palavra perdida antes do corte" que na verdade está dentro do
  clipe. A prova é `conferir.py emendas edl.json`, que transcreve o que se ouve em volta de cada jump cut, e a
  transcrição de cada clipe isolado.

## 7. Checagem tripla (scripts/checar_fala.py, via `projeto.py checar`)

É o passo obrigatório depois de qualquer mudança de corte (veja SKILL.md). Ela junta tudo que já pegou erro de
verdade:

- **retakes escondidos:** a palavra esticada é reouvida em janelas curtas e escalonadas, porque cada janela ouve uma
  tentativa só;
- **repetição em volta de cada emenda e no corte inteiro;**
- **microcortes;**
- **pranchas de bordas** para conferir a olho o fim e o começo de cada clipe.

Transcrever o pedacinho da borda **não** serve como prova. Com 0,5–0,8 s, o whisper completa a palavra cortada ou
alucina em outra língua ("Isn't it?", "Das was ich"). A prova da borda é o espectrograma.

## 8. Auditoria do corte inteiro

```
$PY scripts/auditar.py _projeto/edl.json ~/Library/Caches/human-edit/<NOME>/audio16k.wav --prompt "..."
```

Re-transcreve cada clipe com 0,6 s de contexto e mostra as palavras de dentro, o que sobrou antes e depois, e os
buracos maiores que 0,1 s (com volume e planura, para separar respiro de silêncio). Use para achar repetição,
falso começo e lixo nas bordas. **Não use para validar fim de palavra** (veja acima).

Depois de cada mudança de corte, rode também:

```
$PY scripts/conferir.py emendas _projeto/edl.json
```

Cada linha mostra o que se ouve em ±0,9 s de um jump cut ("em 30 segundos. Basicamente o Dot"). Frase quebrada,
repetida ou com lixo aparece na hora.
