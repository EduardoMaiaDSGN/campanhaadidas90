# Do render ao prompt de vídeo

## Antes de escrever

Inspecione o MP4 aprovado: duração, proporção, movimento, abertura, final, cortes e visibilidade dos espaços onde a ação ocorrerá. Imagens de ambiente fornecem aparência, não um novo ponto de vista. Sheets fornecem identidade, não poses fixas ou múltiplos personagens. Identifique cada arquivo e sua função.

Se o usuário já trouxe um render, entre diretamente nesta etapa quando esse for o pedido. Não exija reconstruir a cena no Blender. Se o render não estiver anexado ou acessível, peça-o; pode organizar as referências enquanto isso, mas não afirme tê-lo analisado.

Use identificadores reais da interface quando conhecidos. Caso contrário, proponha ordem de upload e deixe explícita a correspondência entre @Video 1, @Image 1 etc. Não herde índices, cores, personagens ou telas de exercícios anteriores.

## Estrutura de saída

Prompt em inglês, em um bloco de código, com estes blocos adaptados à cena. Escreva direção de cena fluida e concreta; não um formulário cheio de campos. Evite repetir a mesma restrição em todas as seções.

### REFERENCE DEFINITIONS

Atribua função a cada anexo, incluindo identidades e objetos. Use uma formulação equivalente a:

“@Video 1 supplies only the camera trajectory, framing progression, viewing angles and movement rhythm. The simplified volumes indicate approximate placement and scale. Their shape, poses, stillness and any proxy animation must not determine the human performance. Create the actors’ movement independently from the scene description.”

Descreva aparência pelas imagens, mantendo só os detalhes úteis. Vistas de frente e costas representam o mesmo objeto. Cor de identificação no render não determina figurino. Referência de tela vazia não autoriza inventar conteúdo comercial. Se conteúdo legível for essencial e não estiver definido, peça a referência correspondente.

### LOOK AND CAMERA

Duração e proporção medidas. Aparência solicitada, materiais, luz e continuidade. Descreva em poucas frases o movimento observado e peça sua preservação. Não introduza corte para revelar alguém se o plano aprovado é contínuo. Uma parada de câmera não congela os atores.

### SCENE AND PERFORMANCE

Descreva a história do aluno com atuação espontânea, apropriada à emoção. Não coreografe piscadas, dedos e cotovelos em microetapas. Não limite toda atuação a micromovimentos: caminhar, entrar pela porta, virar-se e cumprimentar podem acontecer se a história pede.

Exemplo de direção: “She reads her phone and breaks into a warm, spontaneous smile. During the orbit, he enters through the doorway, smiles and greets her. She notices him and looks up with a smile, still holding the phone.”

Distribua ações nos momentos em que o enquadramento permite vê-las. Use intervalos apenas quando ajudam, medidos no render; o ritmo da atuação não precisa copiar a timeline de proxies. Um personagem pode entrar mesmo sem proxy correspondente se a câmera e o espaço permitirem. Se a ação pedida não couber, explique a incompatibilidade concreta e proponha ajustar a ação ou voltar à câmera; não invente cortes ou teletransporte.

### CONTINUITY

Selecione restrições relevantes: identidade, figurino, dono do celular, número de pessoas, orientação de tela, permanência de produto e coerência espacial. Não imponha “preserve all motion”, “match every pose”, “keep all subjects static” ou correspondência corporal frame a frame no modo de câmera apenas. Não prometa precisão de texto ou reprodução perfeita.

### AUDIO

Quando houver fala, atribua personagem, texto e idioma. Se o aluno pede “dando oi”, pode escrever uma saudação curta “Oi!” em português brasileiro, sem inventar diálogo longo. Sons de ambiente podem apoiar a ação. Não acrescente música, narração ou legendas sem pedido.

## Diagnóstico de resultados

Se os personagens ficarem robóticos, procure comandos que transfiram movimento ou imobilidade dos proxies. Remova essa transferência e simplifique a direção corporal. Se necessário, proponha reduzir a anatomia e a animação da blocagem e submetê-la novamente à revisão. Não prometa que repetir “natural” eliminará a influência do render.

Se a câmera divergir, verifique instruções concorrentes de enquadramento, imagens de ambiente tratadas como primeiro frame e ações que exigem outra câmera. Se identidade divergir, revise o mapa de referências. Não resolva tudo acumulando negativas.

## Referência metodológica

Estrutura adaptada do fluxo de referências, direção visual, câmera, eventos, continuidade e áudio estudado no tutorial Higgsfield:
https://higgsfield.ai/@adilinthewild/blogs/this-blender-higgsfield-ai-workflow-changes-how-you-make-ai-video

A adaptação dá liberdade de atuação e usa o Blender exclusivamente para câmera por padrão. Não representa uma funcionalidade garantida de isolamento de câmera do Seedance nem uma cópia literal dos prompts do autor.
