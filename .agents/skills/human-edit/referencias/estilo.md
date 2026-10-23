# Estilo de edição HUMAN: o que ele aprovou e o que ele recusou

Cada regra veio de uma correção numa edição real (IMG_4565, 16 versões até a aprovação). O porquê está junto,
porque o que vale é o raciocínio por trás, não a regra decorada.

## Ritmo e corte

- **Dinâmico de verdade.** Tire todos os respiros e pausas. Jump cut é bem-vindo ("é legal ter jump cut, ele é
  bem dinâmicozinho"). O vídeo é para social: cada pausa é um convite para rolar a tela.
- **Palavra comida é o pior erro.** O fim da palavra precisa estar lá: o "i" de "aqui", o "t" de "chat", o "ts" de
  "assets". Ele percebe e se irrita, e a repetição desgasta a confiança mais que qualquer outro erro. Entre um
  corte apertado e a palavra inteira, fique com a palavra inteira.
- **Às vezes, um respiro de propósito.** "Faltou um pouquinho de tempo antes do 'você já deve ter visto'": antes de
  uma virada de assunto ou de uma frase de impacto, deixe ~0,2 s de ar.
- **Sem lixo de fala.** Falso começo ("E depo-", "Aí, aí"), frase dita duas vezes ("eu não era muito" ×2), palavra
  errada ("comenta e-skill"), restos antes da primeira palavra: escolha o take limpo ou force a entrada (`a`) depois
  do tropeço.
- **Micro-corte dentro de palavra soa como bug** ("transforma", "mostrar", "5.5"): se aparecer, use `nocut` nesse
  trecho ou ajuste as bordas.

## Gancho

- Ofereça opções antes de fechar: uma promessa ("Hoje eu vou te ensinar a fazer X como esses aqui"), uma provocação
  (a dor do público), uma confissão. Mostre também takes alternativos da mesma frase. Ele escolheu a promessa, mas
  pediu "outra versão da frase", o que significa trocar o take.
- **Abertura:** 0,5 s só do rosto, depois o split desce com uma montagem de motions a 3 cortes/s (10 quadros por
  corte), só momentos muito legais, alternando paletas. A montagem segue um pouco depois da frase do gancho ("quero
  que mostre um pouco mais de tempo de motions bonitos depois do gancho") e vira tela cheia na fala seguinte.
- **Sem título clickbait no começo.** Ele testou um título estilo Stories e tirou ("não dá tempo").

## Rosto e enquadramento

- **Nunca zoom no rosto.** Sem close, sem punch-in, sem "deszoom": é sempre o enquadramento original, o mais
  aberto possível. "Sempre que tiver meu rosto, eu não quero zoom." Isso vale até para dar ritmo: o ritmo vem dos
  cortes e dos inserts.
- **No split, o rosto desce** para a metade de baixo, e a borda da faixa fica "quase comendo um pouquinho do boné"
  (`cap_gap = -12`). A descida é medida em cada clipe (detecção de rosto), para todo take ficar na mesma altura.

## Split screen

- Faixa de insert em cima, **4:3 (1080×810)**, não 16:9: "pega um pouquinho mais da tela".
- **Entrada:** desliza de cima em 0,2 s, com ease-out. **Saída:** corte seco quando a próxima coisa é outra
  (tela cheia, CTA, outro bloco). Deslizar para cima só quando acaba no meio de uma fala e o rosto continua. No fim do
  resultado ele pediu explicitamente para não subir: "pode só cortar quando for entrar no CTA".
- **O conteúdo da faixa acompanha a fala.** Cada segmento começa quando ele fala daquilo.

## Gravação de tela

- **Recorte bem fechado,** com zoom/scale que anda junto com a fala: o seletor de modelo quando ele diz o modelo, as
  referências caindo no chat quando ele diz "joga", a paleta quando ele diz "assets", cada item quando ele lista
  ("logo, imagem, textos, backgrounds").
- **Rótulo importante nunca cortado na borda** ("aqui é ruim cortar esse ultracode").
- **Ele gosta da interface do Claude:** o card de agentes trabalhando com as bolinhas azuis vale como insert
  ("é bonitinha").
- **Print de passagem dura ~1 s** ("esse ative a skill tem que aparecer um segundinho só").
- **Nada privado:** pule WhatsApp, o seletor de perfil do Chrome, Google e qualquer dado pessoal da gravação.

## Tela cheia

- Use para dar dinamismo, sem fechar no rosto: motions bonitos, o storyboard do que está sendo construído.
- **Prefira o tipográfico com impacto ao 3D** (ele trocou uma lente e um diamante 3D por peças tipográficas).
- Vídeo 16:9 ou 4:3 em tela cheia fica inteiro no meio, sobre uma cópia desfocada dele mesmo. Vídeo vertical
  preenche a tela.
- **Storyboard:** grid de quadros ocupando 100% da tela, 2 colunas, sem fundo branco, sem título nem legenda
  (ele recusou a versão "página de storyboard", com papel e legendas). Dura pouco: ~2 s. Começa em "montar um
  storyboard" e acaba antes do fim da frase ("sai do storyboard antes, ficou muito tempo").
  Os quadros se montam um a um, com cliques leves.

## O resultado (o vídeo pronto do projeto)

- **Nunca em tela cheia.** Toca **inteiro**, só no split ("mostra o resultado inteiro antes de entrar no CTA").
- Encaixe o início para ele terminar exatamente no corte para o CTA. Ajuste de velocidade só imperceptível
  (≤ ~4%). Se não couber, comece a faixa mais cedo, numa fala que combine; não acrescente tempo morto.
- A trilha costuma vir muda: dê som com 1–2 acentos sutis nos momentos fortes (o flash, o logo pousando).

## Grafismos e texto

- **Nada com "cara de IA":** cards genéricos, gradientes, ícones inventados, fontes feias. Para ilustrar uma
  skill, um arquivo ou um projeto, use a **pasta azul do Finder do Mac**, sem fundo, sobre a cabeça, aparecendo e
  sumindo (~1,2 s), com o nome embaixo como no Mac. Ele recusou cinco versões antes dessa.
- **CTA discreto:** branco, SF Pro com peso 470 (um toque acima do regular; ele pediu "bem levemente mais bold"
  depois de ver o regular), cerca de 52 px num quadro de 1080. As duas linhas têm o mesmo tamanho, centralizado, na
  parte de cima. Sem negrito, sem sombra, sem caixa. **Entra no corte, sem fade** e no mesmo quadro em que começa a
  fala do CTA. Antes ele achou chamativo demais um CTA com negrito condensado, sombra e linhas de tamanhos
  diferentes; também achou pequeno demais um de 40 px alinhado à esquerda.
- **Texto branco sobre fundo claro:** escureça bem de leve o topo do quadro (degradê com alpha ~0.13; com 0.42 ele
  disse "sombra muito forte"). Nunca sombra na letra. Avise quando o fim da frase ficar mais apagado.
- **Copy do CTA:** use a frase dele. Não reescreva sem ele pedir.

## Som

- **Voz:** a do iPhone saiu abafada e com sala. Isolamento por IA, EQ com mais agudo ("falta um agudinho"),
  de-esser e compressor, a −14 LUFS.
- **Efeitos sonoros: sutis, com cadência no vídeo todo, "não pode estar na cara"**. Mas precisam ser audíveis no
  celular: na primeira mixagem ele perguntou "os sound fx não entraram?".
  - Whoosh nas entradas e saídas de faixa e nas telas cheias.
  - Um clique em cada corte de montagem e nos momentos de interface (arquivo caindo, seletor parando, item de lista,
    pasta aparecendo).
  - **O clique é o favorito** ("gostei do cliquezinho, dá pra aumentar"): fica 2 dB acima dos outros.
- **Nunca deixe um whoosh subir em cima da última sílaba antes de um corte.** Ele mascara o fim da palavra.

## Entrega

- Versões numeradas, mensagem curta: o que mudou, item por item, e o que ficou igual.
- Pasta do projeto salva no Desktop (`_projeto/`), para qualquer ajuste futuro não depender da sessão.

## Edição padrão (sem inserts)

Quando ele pede "sem inserts, mais padrão" (IMG_4831, vídeo andando no parque):

- Só o rosto, sempre no enquadramento original, com jump cuts. Sem split, sem tela cheia e sem efeitos sonoros: o
  whoosh e o clique existem para os inserts, e num corte só de rosto ficariam soltos.
- Voz isolada mesmo assim (com vento, faz muita diferença), avisando o custo.
- Legenda simples (veja `legenda.md`): uma linha, minúscula, branca, discreta (52 px, peso 520, sombra bem leve),
  no terço de baixo.
- **Andando com o celular, micro jump cut parece defeito.** Um corte que tira menos de ~0,3 s faz a imagem dar um
  pulinho sem motivo ("0:30 corte estranho"). Deixe a pausa curta; corte só pausa de verdade (o corte já faz isso
  em gravação externa).
- **Contraste:** em luz de sol forte, a grade padrão (contraste 1,06) ficou dura: "tira um pouquinho de contraste
  geral" → 0,95 (`Edicao(..., grade=...)`).

## A fala é a base (o que mais o irrita)

Fala duplicada e palavra cortada são os erros que ele não quer apontar nunca mais: "eu quero só jogar e não quero que
tenha esses erros". A checagem tripla da fala (SKILL.md) é obrigatória antes de toda entrega, até zerar.

## Aprendizados novos

<!-- Acrescente aqui, com data e o porquê, cada correção de gosto que valha para os próximos vídeos. -->
