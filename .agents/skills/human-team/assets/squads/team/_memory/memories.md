# Squad Memory: Time Criativo

## Pacing
- Em campanhas completas, o fundador prefere fluxo continuo sem checkpoints intermediarios. Pausar somente para acoes irreversiveis ou que envolvem custo real (chamar Higgsfield CLI pago, publicar, comprar dominio).
- Quando o brief e generoso, nao re-confirmar a cada agente — entregar pacote completo e oferecer ajustes pontuais depois.

## Estilo de Escrita
- Tom premium, calmo, contido. Frases curtas. Pausa em vez de exclamacao.
- Voz emocional sem ser sentimental. Senior sem ser frio.
- Quando a marca for pet/lifestyle premium: evitar "amiguinho", "peludinho", "patinhas", "fofo", "pequeno", "apaixone-se".

## Design Visual
- Em pet/lifestyle premium: paleta neutra (cream, off-white, tan, char) com 1 cor de assinatura saturada (ex: Petti Brick `#9C3B2A`) como diferencial.
- Tipografia editorial (Cormorant Garamond / Romain Grotesque) + sans neogrotesca (Inter / Söhne).
- Fotografia natural, golden hour ou janela lateral, sem fundo branco.
- Continuidade visual do produto e critica entre renders IA — sempre gerar "character reference anchor" antes de batch.

## Estrutura de Conteudo
- Campanhas de lancamento de marca + produto funcionam melhor em 3 ondas: Teaser (curiosidade sem nomear) → Reveal (apresentar marca + produto + lista de espera) → Sell (loja abre, conversao).
- Cronograma backward a partir da data de lancamento, com Art Bible como gargalo critical-path.

## Proibicoes Explicitas
- Sem emoji em copy de marcas premium.
- Sem clipart, cartoon, mascote, ilustracao infantil.
- Sem caps gritante, exclamacao gratuita, hype.
- Sem produto em fundo branco vazio.
- Sem nomear concorrente diretamente.

## Tecnico
- KV, anuncio com lettering e peca principal com texto aplicado: usar Higgsfield CLI + `gpt_image_2`, sempre enviando referencia de KV com imagem + lettering por `--image` quando houver KV final.
- Imagem solta sem lettering, textura, fundo e asset secundario: usar Higgsfield CLI + Nano Banana 2 (`nano_banana_2`).
- Prompts de KV seguem `pipeline/data/gpt-image-kv-system.md`; prompts de imagem solta seguem formato Human Image: CAMERA / LENS / LIGHT / SUBJECT / FOREGROUND / MIDGROUND / BACKGROUND / WARDROBE TONAL BEHAVIOR / MAKEUP SURFACE PHYSICS / POST BEHAVIOR / COMPOSITIONAL GEOMETRY / MOOD & ART DIRECTION.
- Camera trava em IMAX MK IV 65mm (cenas contemplativas) ou ARRI Alexa 35 (cenas com movimento).

## Prompt Engineering Higgsfield Nano Banana 2 (aprendizados v1 -> v2 da run Petlove Copa 2026)
- **Instrucoes negativas falham em ~40% das geracoes.** "no TV screen visible" foi ignorado. Solucao: substituir por instrucao POSITIVA do que se quer no lugar.
- **Repeticao em sinonimo aumenta aderencia.** Para "olhos fechados" usar "eyes softly closed, eyelids gently shut, sleeping peacefully" — tres formulacoes em uma frase.
- **Referencias cinematograficas familiares ao modelo elevam densidade visual.** "shot on Portra 400 medium format film", "Hoyte van Hoytema cinematography", "warm tungsten domestic light".
- **Posturas e expressoes especificas funcionam melhor que estados emocionais abstratos.** "head resting on hand, eyes closed, slumped shoulders" > "defeated posture".
- **Para evitar fantasia em pet, usar instrucao positiva do tecido.** "Natural fur uncovered" + descricao de tecidos permitidos (cachecol, lenço, cobertor) em vez de "no costume".
- **TV glow como assinatura visual em vez de banir TV.** "warm flickering amber-blue light from television off-frame, screen completely outside the frame" — captura o ambiente domestico brasileiro sem violar ambush rules.
