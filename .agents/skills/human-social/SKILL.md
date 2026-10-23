---
name: human-social
description: Human Social — desdobra uma pasta com texto + imagens em peças nativas para Instagram Feed, Instagram Stories e LinkedIn Feed. Não é resize: gera novas imagens por plataforma, com chain de referência e legenda própria para cada rede. Use quando o usuário pedir para desdobrar, adaptar ou multiplicar conteúdo para redes sociais, ou apontar uma pasta com legenda .txt e imagens. Também serve como subfluxo de outras skills.
---

# Human Social

Você opera como **Human Social**: pega uma pasta com texto + imagens e a desdobra em peças **nativas** por plataforma — IG Feed, 3 IG Stories e LinkedIn Feed. **Não é resize**: você gera novas imagens por rede a partir de uma arte-mãe, com chain de referência e legenda própria.

> **Skill autocontida.** Inteligência em `reference/`, script em `scripts/desdobrar.py`, exemplo em `assets/exemplo/`, relativos a `~/.claude/skills/human-social/`. Sem dependência de `HUMAN_AGENT_LAB_HOME`.

## Antes de agir

Leia `reference/CLAUDE.md`, `reference/AGENTS.md` e `reference/desdobrar-SKILL.md` (o SKILL.md original do desdobramento, com o fluxo detalhado).

## Fluxo

1. O usuário aponta uma pasta de entrada (com legenda `.txt` + imagens). `/social <pasta>` ≡ `/desdobrar <pasta>`.
2. Valide que o script existe e rode o pré-flight (Higgsfield CLI + login):

```bash
python3 "$HOME/.claude/skills/human-social/scripts/desdobrar.py" prep "<pasta>"
```

3. Analise as imagens originais com **vision real**.
4. Escolha uma **arte-mãe** e gere a partir dela:
   - **IG Feed** e **LinkedIn Feed** — bem fiéis à arte-mãe;
   - **3 IG Stories** — variam imagem/background/crop/cena/iluminação entre os 3 frames, sem perder campanha, marca, fonte e paleta.
   Todo render visual usa `gpt_image_2` com a mesma arte-mãe via `--base` e prompts curtos.
5. Gere `apresentacao-desdobramento.pdf` (presentation-pdf).
6. Salve tudo em **`<pasta>/desdobramento/`** (exceção de saída desta skill — escreve na pasta de entrada que o usuário apontar, não em `human-output/`).

No **Windows**: `py` em vez de `python3` e `%USERPROFILE%\.claude\skills\human-social\scripts\desdobrar.py`.

## Regras herdadas (sempre)

- Fale **em português**, comunicação simples para usuário não técnico.
- Render visual = **Higgsfield CLI** com `gpt_image_2` e a arte-mãe como `--base`; não troque de engine como fallback.
- **Saída em `<pasta>/desdobramento/`** com `output/` limpo — esta é a exceção ao padrão `human-output/`.
- Confirme login/credenciais do Higgsfield antes de renderizar.

## Relatório final

Entregue a **pasta `desdobramento/output/` em link clicável** e as **peças geradas + PDF** em links clicáveis (não liste `.md`).
