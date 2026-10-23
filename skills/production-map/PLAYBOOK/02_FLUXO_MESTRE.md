# 02 — FLUXO MESTRE

## Visão geral

O processo possui nove etapas. Elas são progressivas, mas podem voltar uma casa quando um teste revela informação nova.

## Etapa 0 — Configuração técnica

Preencha `PROJETO/00_CONFIGURACAO.md`.

Defina, quando possível:

- modo `PROMPTS_ONLY` ou `ASSISTED_GENERATION`;
- gerador de stills;
- gerador de vídeo;
- suporte a `@handles`;
- duração máxima por clip;
- suporte a frame inicial e final;
- suporte a múltiplos planos;
- áudio;
- proporção e resolução;
- idioma de prompt;
- política de música.

Sem isso, a IA corre o risco de desenhar um processo impossível para a plataforma.

## Etapa 1 — Intake do roteiro

Resultado esperado:

- logline;
- arco emocional;
- macroestrutura;
- lista provisória de sequências;
- ponto de vista;
- diálogo e som;
- decisões realmente abertas;
- riscos.

Não produza assets ainda.

## Etapa 2 — Plano geral

Preencha `PROJETO/02_PLANO_GERAL.md` com:

- duração alvo;
- blocos narrativos;
- duração aproximada de montagem;
- ordem de produção;
- dependências;
- ferramentas;
- estratégia de edição;
- critérios de aprovação.

As durações de geração não precisam ser iguais às durações de montagem. Um clip de 20–30 segundos pode existir para fornecer 10–15 segundos úteis e alças de edição.

## Etapa 3 — Bíblia visual e de continuidade

Preencha `PROJETO/03_BIBLIA_VISUAL_CONTINUIDADE.md`.

Trave:

- identidade física;
- figurino;
- props;
- escala;
- anatomia;
- paleta;
- materiais;
- geografia;
- direção de luz;
- linguagem de câmera;
- atuação;
- regras de som;
- diferença entre realidade e subjetividade;
- elementos proibidos.

Uma regra deve ser observável. “Bonito” não é regra; “luz lateral suave, preto natural e halation discreta” é.

## Etapa 4 — Arquitetura de assets

Preencha `PROJETO/04_INVENTARIO_ASSETS.md`.

Crie assets somente quando houver justificativa de continuidade. Priorize:

1. protagonista;
2. personagens recorrentes;
3. criatura ou objeto de geometria difícil;
4. ambientes-base;
5. obras ou props narrativos;
6. estados transformados;
7. frames de continuidade.

Não crie uma composição estática de personagem + ambiente quando os dois assets aprovados podem ser combinados diretamente no vídeo sem introduzir estado novo.

## Etapa 5 — Produção de stills e estados

Ordem recomendada:

1. retrato de identidade, se necessário;
2. character sheet completo;
3. asset de criatura/prop difícil;
4. environment plate sem protagonistas;
5. obra ou objeto isolado;
6. estado alternativo com câmera travada;
7. mundo navegável derivado;
8. frame mestre somente quando ele resolve continuidade real.

Cada aprovação atualiza inventário, bíblia e registro.

## Etapa 6 — Auditoria da biblioteca da plataforma

Antes dos vídeos:

1. abra a biblioteca real da ferramenta;
2. capture nomes visíveis e handles;
3. registre caixa, sufixos e erros exatamente;
4. associe cada item ao ID canônico;
5. marque duplicidades e versões antigas;
6. nunca invente o que não foi visto.

O ID interno do projeto e o `@handle` da plataforma são coisas diferentes.

## Etapa 7 — Decupagem dirigida

Para cada bloco:

1. função dramática;
2. estado inicial real;
3. estado final real;
4. duração de montagem;
5. duração de geração;
6. número e ritmo dos planos;
7. câmera, lente e foco;
8. blocking;
9. acting;
10. transformação e física;
11. som;
12. conexão com blocos anterior e seguinte;
13. assets e handles confirmados.

Só depois escreva o prompt.

## Etapa 8 — Geração, feedback e montagem

Depois de cada teste:

- aprove ou rejeite por critérios específicos;
- preserve os trechos bons;
- produza inserts quando uma sequência funciona, mas precisa de cobertura;
- promova um bom frame final ou inicial para asset da plataforma;
- evite regenerar 30 segundos se um insert de 5 segundos resolve;
- evite dividir uma transformação contínua entre duas gerações quando sua geometria não sobreviverá ao corte;
- divida em gerações quando houver um corte editorial natural entre ambientes ou ações.

## Etapa 9 — Fechamento

Antes da montagem final, confirme:

- todos os blocos aprovados;
- frames de transição;
- handles congelados;
- diálogos separados;
- ausência de música gerada;
- continuidade de personagem;
- continuidade de luz e geografia;
- material para inserts;
- som e título adicionados fora dos clips, quando aplicável.

