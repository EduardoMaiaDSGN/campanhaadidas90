# 04 — DIREÇÃO, DECUPAGEM E PROMPTS

## 1. Comece pela função dramática

Antes de pensar na câmera, responda:

> O que muda para personagem, história ou espectador durante este bloco?

Se nada muda, o plano é cobertura ou tempo morto.

## 2. Estado inicial e final

Todo bloco deve registrar:

- frame ou ação inicial real;
- posição dos personagens;
- estado do cenário;
- estado do prop;
- frame ou ação final real;
- conexão editorial seguinte.

Nunca baseie o início na lembrança do prompt anterior. Baseie no último frame efetivamente gerado.

## 3. Duração de geração versus montagem

- Gere mais tempo quando precisar de alças e fragmentos.
- Não encha o tempo extra com novos acontecimentos.
- Um bloco pode começar com ação já em curso.
- Um bloco no meio do filme não precisa sair do preto nem terminar em pose.
- Divida cenas onde houver corte natural.
- Não divida uma metamorfose contínua se a geometria precisa permanecer idêntica entre clips.

## 4. Decupagem

Para cada plano, defina:

1. tempo aproximado;
2. escala;
3. lente ou comportamento óptico;
4. posição inicial da câmera;
5. movimento físico;
6. blocking;
7. foco;
8. atuação;
9. evento;
10. som;
11. corte.

Use hard cuts quando os planos são realmente diferentes. Não peça morph entre coberturas.

## 5. Linguagem de câmera

Evite a gramática automática:

- plano geral estático;
- push-in genérico;
- close de olho sem função;
- slider lateral sem motivação;
- câmera flutuante;
- drone para qualquer revelação;
- slow motion usado para esconder física ruim.

Prefira:

- câmera já envolvida na ação;
- objeto de primeiro plano revelando espaço;
- tracking que perde e reencontra personagem;
- mudança real de distância;
- parallax;
- oclusão física;
- crane com função;
- dolly e zoom simultâneos quando o efeito serve à narrativa;
- câmera que reage uma fração atrasada ao inesperado;
- movimentos que começam fechados e conquistam escala.

Descreva como o movimento é obtido. “Câmera abre” é ambíguo. “O rig desacelera enquanto o carro continua, aumentando a distância e revelando o prédio” é filmável.

## 6. Acting

Dirija progressão emocional, não adjetivo.

Fraco:

`She is surprised and happy.`

Forte:

```text
Her eyes register the color. Her pace changes by less than half a step. She takes one small breath. Curiosity replaces surprise, and a private smile appears while she continues walking.
```

Use:

- olhar;
- respiração;
- peso;
- mãos;
- tempo de reação;
- mudança de passo;
- microexpressão;
- decisão de continuar.

Evite:

- gasp;
- boca aberta;
- olhos arregalados;
- pausa teatral;
- sorriso fixo;
- atuação publicitária infantil;
- personagem congelado contemplando a arte.

Quando a personagem está encantada, dê ação: tocar, caminhar, correr, acompanhar, desviar, descobrir, brincar.

## 7. Física e transformação

Toda transformação precisa responder:

- onde começa;
- qual material muda;
- como a frente de transformação se move;
- o que preserva identidade;
- o que acontece com peso e contato;
- como a câmera revela o processo;
- qual é o estado final.

Não explique magicamente o que pode ser mostrado materialmente.

Evite repetir o mesmo mecanismo de transição. Se um líquido já realizou uma passagem, não o use automaticamente de novo.

## 8. Som

Por padrão:

```text
No music and no score. Use only diegetic sound: [sons específicos].
```

Descreva matéria:

- tecido;
- sapato;
- pedra;
- ar;
- água;
- pigmento;
- metal;
- respiração;
- reverberação do espaço.

Diálogo deve ser intencional. Se for para ser ininteligível, diga por quê: distância, trânsito, arquitetura ou sobreposição.

## 9. Estrutura recomendada do prompt de vídeo

```text
Create one precisely directed [DURAÇÃO] cinematic sequence.

REFERENCE ROLES
[handle + função e limite de cada referência]

NARRATIVE PURPOSE
[o que o bloco realiza]

OPENING CONTINUITY
[frame/ação/posição inicial]

SHOT 1 — [tempo]
[câmera, blocking, acting, ação, corte]

SHOT 2 — [tempo]
[...]

CAMERA LANGUAGE
[estética e movimentos físicos]

PERFORMANCE
[progressão emocional observável]

CONTINUITY
[identidade, props, contagens, estados]

SOUND
No music and no score. [som diegético]

AVOID
[erros específicos, não lista genérica infinita]
```

## 10. Prompt de still

Estrutura recomendada:

```text
Create/Edit [asset e estado].

REFERENCE ROLES
[controle de cada referência]

ABSOLUTE LOCKS
[câmera, personagem, arquitetura, contagem]

PRIMARY CHANGE
[uma correção principal]

GEOGRAPHY / ANATOMY / MATERIALS
[o que precisa ser verificável]

PHOTOGRAPHIC CAPTURE
[luz, lente, textura, formato]

OUTPUT
[uma imagem, sheet, sem texto etc.]

AVOID
[erros conhecidos]
```

## 11. Formato de entrega

Quando o diretor pedir “manda o prompt”:

- entregue o prompt integral;
- use um único bloco copiável;
- não entregue somente o trecho alterado;
- não inclua notas dentro do prompt;
- use handles exatos;
- não invente referências;
- inclua estética em todo prompt de vídeo;
- inclua som em todo prompt de vídeo;
- preserve a última direção aprovada.

Prompts podem ser entregues no chat. Arquivos `.md` de prompts são opcionais e nunca devem competir com o registro vivo como fonte de verdade.

## 12. Moderação e linguagem

Descreva diretamente o conteúdo visual desejado. Evite inserir no prompt frases meta-legais desnecessárias sobre copyright, personagens protegidos ou franquias quando elas não ajudam a imagem; essas palavras podem causar falsos positivos de plataforma.

Ao usar uma referência artística, traduza-a em:

- composição;
- paleta;
- textura;
- ritmo;
- material;
- escala;
- relação espacial.

Não dependa apenas de “in the style of”.

