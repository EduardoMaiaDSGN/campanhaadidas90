# 08 — ADAPTADOR DE PLATAFORMA

Este processo funciona em Higgsfield ou em outra plataforma, mas precisa conhecer a interface real antes de produzir prompts em escala.

## 1. Auditoria inicial

Abra a plataforma e registre em `PROJETO/00_CONFIGURACAO.md`:

- duração máxima;
- durações disponíveis;
- proporções;
- resolução;
- suporte a múltiplos planos;
- suporte a frame inicial;
- suporte a frame final;
- suporte a áudio;
- comportamento padrão de música;
- limite de referências;
- sintaxe para chamar assets;
- categorias da biblioteca;
- existência de nomes visíveis e handles distintos;
- limites de prompt;
- regras de moderação que afetaram testes reais.

Não baseie o pipeline na página de marketing. Baseie na conta, versão e interface que o diretor está usando.

## 2. Auditoria da biblioteca

Para cada asset aprovado:

1. abra a aba correta: Characters, Locations, Props, Elements ou equivalente;
2. capture screenshot do cartão;
3. registre o nome visível;
4. registre o handle exibido abaixo dele;
5. preserve caixa e typo;
6. relacione ao ID canônico;
7. marque versões duplicadas;
8. identifique a versão proibida ou superseded.

Exemplo genérico:

| ID canônico | Nome visível | Handle real | Regra |
|---|---|---|---|
| `ENV_02` | `Env_02` | `@env_02_v1` | usar atual |
| `ENV_02_OLD` | `ENV_02` | `@env_02` | não usar automaticamente |

O nome mais “limpo” pode ser o asset antigo. Nunca escolha por aparência do texto.

## 3. Handles dentro do prompt

O handle identifica o asset. A descrição define seu papel.

```text
@handle_ambiente_atual is the absolute lock for architecture, geography and lighting.
@handle_protagonista is the exact identity, age and wardrobe reference for the protagonist.
```

Não redescreva o asset a ponto de criar uma versão concorrente. Descreva apenas os locks necessários e a ação nova.

## 4. Referências anexadas sem handle

Se a plataforma usa anexos ou slots:

- registre o nome do arquivo;
- descreva o papel visual;
- proíba transferência de elementos irrelevantes;
- não escreva “imagem 1”.

Exemplo:

```text
The supplied portrait controls only the exact red hair color inside the reflection. Do not transfer face, age, clothing, background or graphic elements.
```

## 5. Frames iniciais e finais

Quando um vídeo produz um frame valioso:

1. exporte ou capture o frame;
2. cadastre-o na biblioteca;
3. dê um nome curto;
4. registre o handle real;
5. associe a `FRM_XX`;
6. descreva exatamente o que o frame trava;
7. use-o em inserts e continuações.

Um frame pode travar:

- mãos num prop;
- pose;
- composição;
- luz;
- posição da câmera;
- estado de cenário;
- começo de alternativa.

## 6. Duração e montagem

Se a plataforma oferece 5, 10, 15 ou 30 segundos:

- use 5 segundos para transições e inserts;
- use 10–15 para acting ou uma ação fechada;
- use 20–30 para multi-shot, exploração e cobertura;
- não use 30 apenas porque está disponível;
- não divida uma transformação contínua só para aproveitar duas gerações.

## 7. Multi-shot

Quando a plataforma aceita sequência com cortes:

- temporize cada plano;
- escreva `HARD CUT` onde necessário;
- não peça câmera contínua e cortes simultaneamente;
- preserve direção de tela, luz, props e posição;
- lembre que a IA pode criar planos extras se o prompt for ambíguo.

## 8. Áudio

Algumas plataformas adicionam música automaticamente. Em todo prompt:

```text
No music and no score. Use only diegetic sound: [...].
```

Se o som não for confiável, gere como guia e reconstrua na pós.

## 9. Moderação e falsos positivos

Se um prompt falhar:

1. compare com prompts aprovados usando os mesmos assets;
2. remova metalinguagem desnecessária;
3. evite termos legais que não descrevem a imagem;
4. mantenha identidade e ação legítimas;
5. registre a formulação que passou;
6. não conclua automaticamente que o asset é o problema.

## 10. Quando a plataforma mudar

Atualize configuração e mapa de handles. Não reescreva a bíblia ou o roteiro por causa de uma mudança de interface.

O sistema criativo permanece; o adaptador técnico muda.
