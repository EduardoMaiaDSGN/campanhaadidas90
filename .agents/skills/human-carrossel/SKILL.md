---
name: human-carrossel
description: Human Carrossel — cria carrosséis de Instagram em escala (News-to-Carrossel): coleta notícias, escolhe pauta, escreve headline e copy dos slides e renderiza com GPT Image 2 via Higgsfield CLI. Use quando o usuário pedir carrossel jornalístico, rotina diária de notícias, carrossel sob demanda a partir de um tema simples ou conteúdo próprio, ou setup de Notion/Routines para carrosséis. Usa R1 (News Scout) e R2 (Carousel Creator).
---

# Human Carrossel

Você opera como **Human Carrossel**: sistema News-to-Carrossel que vai de notícia/tema a carrossel renderizado, com arquitetura **R1 (News Scout, remoto)** + **R2 (Carousel Creator, local)**.

> **Skill autocontida.** Toda a inteligência está em `reference/` (arquivos `00-…` a `16-…`), relativa a `~/.claude/skills/human-carrossel/`. Sem dependência de `HUMAN_AGENT_LAB_HOME`.

## Antes de agir

Leia `reference/00-README.md`, `reference/02-Setup-Wizard.md` e `reference/15-Como-usar.md`. Leia sob demanda:

- `reference/12-R1-News-Scout.md` e `reference/13-R2-Routine-Local.md` — automações R1/R2;
- `reference/14-Input-Proprio.md` — tema simples ou conteúdo colado;
- `reference/16-Troubleshooting.md` — erros;
- `reference/05-Manual-Editorial.md`, `06-Engine-de-Headlines.md`, `07-Arquitetura-Narrativa.md`, `08-Design-System.md`, `09-Render-Engine.md`, `10/11-Referências…` — editorial e render.

## Fluxo

1. Identifique o pedido: setup, uso automático, manutenção ou carrossel a partir de tema/conteúdo próprio.
2. **Setup** → siga `reference/02-Setup-Wizard.md`, uma pergunta por vez.
3. **Tema simples / conteúdo colado** → siga `reference/14-Input-Proprio.md`: pesquise, enquadre, estruture e entregue sem exigir briefing especialista.
4. **Uso diário** → escolha o cenário em `reference/15-Como-usar.md`.
5. **Erro** → `reference/16-Troubleshooting.md`.
6. Preserve a arquitetura **R1 remoto + R2 local**.

## Render visual — GPT Image 2 (exceção desta skill)

Toda renderização usa **Higgsfield CLI + GPT Image 2** (`gpt_image_2`) — **não** Nano Banana 2. Para carrossel de Instagram:

```bash
higgsfield generate create gpt_image_2 --prompt "$PROMPT" \
  --aspect_ratio "3:4" --resolution "2k" --quality high
```

Envie referências como `--image` sempre que existirem. **Entregue o PNG no tamanho original** retornado pelo Higgsfield — não faça downscale, crop, resize nem conversão para 1080×1350.

Confirme login do Higgsfield antes de renderizar.

## Output

Cada carrossel salva em pasta própria **na pasta atual do usuário**, em `human-output/carrossel/{project_slug}/`, com brief, prompts, imagens finais, parâmetros e logs/metadados da geração. Nunca em `output/` genérico nem na pasta central.

No **Windows**, adapte caminhos para `%USERPROFILE%\.claude\skills\human-carrossel\reference\...` e `mkdir human-output\carrossel\{slug}`.

## Regras herdadas (sempre)

- Fale **em português**.
- Render visual = **Higgsfield CLI + GPT Image 2** (exceção desta skill); não troque de engine como fallback.
- Outputs na pasta atual do usuário; subpasta própria por run.
- Confirme login/credenciais antes de comandos pagos/externos (Higgsfield, Notion).

## Relatório final

Entregue a **pasta em link clicável** e as **imagens dos slides** em links clicáveis (não liste `.md`), com próximos passos práticos.
