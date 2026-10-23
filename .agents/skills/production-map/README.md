# REPLICATE — Sistema de produção de filmes generativos

Esta pasta é um kit autônomo para transformar um roteiro em um filme generativo dirigido com continuidade, linguagem cinematográfica e controle de produção.

Ela nasceu de um processo real de longa iteração entre direção, criação de assets, decupagem, geração de vídeo e montagem. O objetivo não é entregar “prompts bonitos”, mas reproduzir o sistema que fez o processo funcionar:

- roteiro como fonte dramática;
- decisões registradas e recuperáveis;
- assets criados apenas quando necessários;
- nomes e `@handles` reais da plataforma auditados;
- direção plano a plano antes do prompt;
- prompts completos e copiáveis;
- feedback transformado em regra;
- continuidade entre conversas, compactações e tarefas paralelas;
- montagem pensada desde a geração.

## O que esta pasta não faz

- Não altera o projeto que serviu de origem.
- Não contém personagens, obras ou decisões específicas de um filme anterior.
- Não depende de uma ferramenta única.
- Não obriga a IA a gerar imagens ou vídeos. O modo padrão é **somente prompts**.

## Estrutura

### `PLAYBOOK/`

Manual de operação do sistema.

1. [`00_COMECE_AQUI.md`](PLAYBOOK/00_COMECE_AQUI.md)
2. [`01_PROTOCOLO_DO_AGENTE.md`](PLAYBOOK/01_PROTOCOLO_DO_AGENTE.md)
3. [`02_FLUXO_MESTRE.md`](PLAYBOOK/02_FLUXO_MESTRE.md)
4. [`03_ASSETS_HANDLES_E_ESTADOS.md`](PLAYBOOK/03_ASSETS_HANDLES_E_ESTADOS.md)
5. [`04_DIRECAO_DECUPAGEM_E_PROMPTS.md`](PLAYBOOK/04_DIRECAO_DECUPAGEM_E_PROMPTS.md)
6. [`05_FEEDBACK_QA_E_ITERACAO.md`](PLAYBOOK/05_FEEDBACK_QA_E_ITERACAO.md)
7. [`06_CONTEXTO_HANDOFF_E_PARALELIZACAO.md`](PLAYBOOK/06_CONTEXTO_HANDOFF_E_PARALELIZACAO.md)
8. [`07_CHECKLISTS.md`](PLAYBOOK/07_CHECKLISTS.md)
9. [`08_ADAPTADOR_DE_PLATAFORMA.md`](PLAYBOOK/08_ADAPTADOR_DE_PLATAFORMA.md)
10. [`09_PADROES_PRATICOS.md`](PLAYBOOK/09_PADROES_PRATICOS.md)

### `PROJETO/`

Arquivos vivos de um novo filme. O usuário coloca o roteiro e a IA preenche os demais progressivamente.

1. [`00_CONFIGURACAO.md`](PROJETO/00_CONFIGURACAO.md)
2. [`01_ROTEIRO_ENTRADA.md`](PROJETO/01_ROTEIRO_ENTRADA.md)
3. [`02_PLANO_GERAL.md`](PROJETO/02_PLANO_GERAL.md)
4. [`03_BIBLIA_VISUAL_CONTINUIDADE.md`](PROJETO/03_BIBLIA_VISUAL_CONTINUIDADE.md)
5. [`04_INVENTARIO_ASSETS.md`](PROJETO/04_INVENTARIO_ASSETS.md)
6. [`05_MAPA_HANDLES_PLATAFORMA.md`](PROJETO/05_MAPA_HANDLES_PLATAFORMA.md)
7. [`06_REGISTRO_VIVO_PRODUCAO.md`](PROJETO/06_REGISTRO_VIVO_PRODUCAO.md)
8. [`07_DECUPAGEM_ATUAL.md`](PROJETO/07_DECUPAGEM_ATUAL.md)
9. [`08_HANDOFF_CONTEXTO.md`](PROJETO/08_HANDOFF_CONTEXTO.md)

## Uso em uma frase

Copie esta pasta para um novo projeto, cole o roteiro em `PROJETO/01_ROTEIRO_ENTRADA.md` e envie à IA a mensagem de inicialização presente em `PLAYBOOK/00_COMECE_AQUI.md`.

## Regra de ouro

O prompt nunca é a fonte de verdade. A fonte de verdade é o conjunto formado por roteiro, bíblia, inventário, mapa de handles e registro vivo.
