# Direção e implementação de câmera

## Estrutura de raciocínio

Organize internamente: projeto → blocagem → câmera → trechos do movimento → junções → textura → verificação. Execute no Blender; não devolva apenas um prompt de construção quando houver acesso para fazer o trabalho.

Use linguagem concreta: de onde sai, por onde passa, para onde olha, onde desacelera, o que aparece em primeiro plano e como termina. Não imponha nomes técnicos ao aluno. Se ele disser “sobe para trás”, traduza em afastamento com elevação, alvo e abertura do enquadramento coerentes.

- Separe percurso da câmera e alvo invisível de enquadramento. O alvo da câmera não é o olhar do personagem.
- Prefira curvas para arcos e órbitas; use linha reta para deslocamento estritamente vertical. Evite interpolação que produza voltas, overshoot ou reversões inesperadas.
- Defina a lente pelo enquadramento. Aproximar fisicamente não é dar zoom. Mantenha lente fixa quando o pedido não justificar variação.
- Especifique aceleração, desaceleração e pausas conforme o pedido. Uma passagem lenta é diferente de uma parada completa.
- Evite roll acidental, colisões e obstruções do assunto. Não atravesse paredes a menos que a passagem faça parte da intenção.
- Handheld só quando solicitado. Em robo-arm, viagens rápidas podem ter frenagem firme e poses totalmente imóveis. Não misture oscilação com paradas rígidas.
- Em plano-sequência, preserve continuidade de posição e orientação. Havendo cortes pedidos, altere câmera, alvo e lente no frame correto, sem um frame intermediário interpolado.

## Blocos um pouco refinados

O mínimo suficiente depende do enquadramento. Um plano aberto pode usar um único bloco; um close ou OTS pode exigir cabeça e tronco separados, estáticos. Cantos suavizados e uma sugestão de largura dos ombros ajudam a composição. Isso não justifica criar um manequim articulado.

Um telefone independente deve estar onde será segurado no vídeo final. A câmera pode enquadrar sua frente mesmo que esteja suspenso na blocagem. A atuação posterior resolve mãos e postura. Não anime um dedo tocando a tela apenas porque o vídeo final terá um toque.

## Exemplo adaptável

“Uma personagem em blocos simples no centro. Celular estático à frente, em altura de leitura. A câmera começa atrás da parte superior do tronco, mostrando o celular. Afasta-se, percorre uma órbita e aproxima-se pela frente até a região do rosto. O alvo transfere a atenção do celular para a cabeça. Movimento contínuo e suave. Apenas câmera e alvo animados.”

Esse exemplo não fixa duração, lado da órbita ou história para outros projetos.

## Verificação antes da revisão

Confira primeiro, último e pontos relevantes da trajetória pela câmera. Verifique escala, passagem atrás de massas, distância ao celular, espaço acima da cabeça e aproximação final. Percorra a timeline para encontrar mudanças bruscas. Guarde backups após blocagem, animação e refinamentos. Não renderize como forma de validar antes da aprovação: use viewport e inspeção do projeto.

## Origem e adaptação

Baseado no estudo dos exemplos de órbita, OTS, subida vertical, transferência de alvo e robo-arm do tutorial de @adilinthewild:
https://higgsfield.ai/@adilinthewild/blogs/this-blender-higgsfield-ai-workflow-changes-how-you-make-ai-video
https://www.youtube.com/watch?v=OiULPvTJ-0E

A modelagem estática em blocos e a separação estrita entre câmera e atuação são ajustes deste fluxo após resultados com personagens robóticos. O estudo do tutorial foi feito por texto e amostragem visual; não equivale a garantia de aderência do gerador. Não é necessário revisitar o site para cada pedido.
