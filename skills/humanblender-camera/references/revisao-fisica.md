# Revisão de física antes da aprovação

Leia após construir a blocagem e animar a câmera, antes de apresentar o .blend ao aluno. O objetivo é um movimento fisicamente convincente dentro do estilo pedido, preservando percurso, composição, acontecimentos e enquadramento final. Corrija problemas de execução sem redesenhar a cena. Se uma correção exigir mudar a intenção ou a duração solicitada, explique a incompatibilidade e peça a decisão do aluno.

## Câmera e alvo

- Identifique a lógica de operação compatível com o pedido: câmera na mão, gimbal, dolly, slider, grua, drone ou braço robótico. Use essa lógica para orientar aceleração, frenagem e rotação; não é necessário modelar o equipamento.
- Inspecione curvas e transformações para detectar arrancadas, paradas, mudanças de direção, overshoot ou variações de aceleração involuntárias. Ajuste tangentes e keyframes desnecessários conforme distância, ritmo e energia do movimento. Não aplique o mesmo easing a todos os trechos.
- Coordene deslocamento e orientação do alvo para evitar trancos no enquadramento. Use antecipação, aceleração, percurso, desaceleração e acomodação quando fizerem sentido; nem todo trecho precisa de todas essas fases.
- Respeite a intenção mecânica ou estilizada: velocidade constante, rotação uniforme, curvas simétricas, enquadramento travado e paradas firmes podem ser deliberados. Não os trate como defeitos por si só. Em cortes pedidos, preserve a troca instantânea de câmera, alvo e lente.
- Imperfeições só entram se compatíveis com o estilo solicitado. Não acrescente tremor aleatório, respiração, atraso de acompanhamento ou pequenas correções de enquadramento como receita universal. Handheld continua dependendo de pedido explícito. Não adicione oscilação às poses imóveis de um braço robótico.
- Confira escala, lente, paralaxe e passagem junto a volumes de primeiro plano. Preserve a distinção entre deslocamento físico e zoom; não altere a lente para disfarçar um percurso inadequado. Verifique colisões e obstruções involuntárias, respeitando passagens impossíveis que tenham sido pedidas como efeito.

## Objetos e personagens

No fluxo padrão, os proxies ficam estáticos. Não crie rig, animação corporal, mãos, cabelo, roupa ou movimentos secundários para cumprir esta revisão. Um celular suspenso pode ser uma marcação intencional de onde será segurado; não o faça cair nem construa uma mão para sustentá-lo.

Quando houver coreografia de objetos explicitamente solicitada, revise apenas esses movimentos: peso aparente, aceleração, gravidade, contato, colisão e acomodação após impacto. Evite atravessamentos, deslizamentos ou flutuação não intencionais. Movimentos secundários devem decorrer da ação e caber no escopo autorizado, sem acrescentar simulação ou detalhe desnecessário. A atuação humana continua sendo definida pela descrição do aluno no prompt de vídeo.

## Verificação e entrega para revisão

Confira início, final, mudanças de direção, aproximações e junções pela câmera. Observe primeiro o comportamento da câmera e depois os objetos animados, quando existirem. Avalie o movimento em reprodução no tempo correto pela viewport quando disponível; imagens isoladas não demonstram ritmo ou inércia. Se a reprodução estiver lenta, não confunda atraso da viewport com a velocidade prevista da animação.

Complemente com amostragem da timeline e inspeção de curvas; consulte velocidade e aceleração quando ajudarem a localizar um problema. Se não conseguir avaliar a reprodução, registre essa limitação sem declarar que assistiu ao movimento. Não renderize nem exporte playblast nesta etapa e não exija gráficos técnicos como entrega ao aluno.

Salve a versão revisada, registre brevemente o que foi corrigido e prossiga para a revisão do aluno. A aprovação deve se referir a essa versão. Esta checagem acontece antes da aprovação e não autoriza alterar silenciosamente um movimento já aprovado para render.

## Origem

Adaptação do documento fornecido pelo usuário “REVISÃO DE FÍSICA ASTRA E BLENDER” (Physical Realism Pass), limitada ao fluxo de blocagem e câmera desta skill. O documento “PROMPT BASE BLENDER” não integra esta adaptação.
