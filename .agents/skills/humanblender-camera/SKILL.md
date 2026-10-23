---
name: humanblender-camera
description: Cria e ajusta blocagens simples e movimentos de câmera no Blender, revisa a física do movimento antes da aprovação do aluno, renderiza após aprovação e prepara um prompt para Seedance 2.5 usando o render e referências visuais. Use para o fluxo de pré-visualização 3D para vídeo com IA.
---

# HumanBlenderCâmera

Conduza o aluno da ideia de câmera ao render de referência e ao prompt de vídeo. Converse em português, com pedidos simples e respostas curtas. O aluno descreve a intenção; você resolve a implementação. Não exija preenchimento de formulário técnico. Não use uma skill genérica de Seedance para substituir este fluxo.

## Princípio central

**O render fornece a câmera. As imagens fornecem a aparência. A descrição do aluno fornece a atuação.**

Por padrão, o Blender demonstra apenas movimento de câmera e relações espaciais. Blocos estáticos não são instruções para deixar pessoas imóveis no vídeo final. Não copie poses ou gestos de proxies na geração. Uma coreografia de objetos só entra na referência se o aluno a solicitar explicitamente.

## 1. Entender e construir

Verifique quais ferramentas realmente permitem acessar o Blender: integração disponível, Python do Blender ou controle de interface. Use a capacidade disponível mais adequada. A skill não instala Blender nem fornece uma conexão por si só. Se não houver acesso, explique a limitação e forneça, quando possível, um script executável no Blender; nunca declare que uma cena foi criada sem executá-la. Nesse caso, peça o arquivo ou a confirmação da execução antes de avançar.

Leia [direcao-blender.md](references/direcao-blender.md) ao construir ou ajustar a cena.

Entenda assunto, ponto inicial, percurso, enquadramento final e ritmo. Pergunte apenas o que mudar materialmente a intenção. Se a proporção ainda não estiver definida pelo aluno ou pelo contexto, pergunte antes de construir a cena, com opções simples como vertical 9:16, horizontal 16:9 ou quadrado 1:1; aceite outros formatos. Não assuma 16:9 nem pergunte novamente por uma proporção já definida. Sugira uma duração com base na ideia, no percurso da câmera, nas ações previstas e no ritmo desejado, explicando brevemente a escolha; não use uma duração fixa como padrão. Preserve a duração quando o aluno já a tiver especificado. Use 24 fps quando não houver outra preferência ou exigência do projeto e informe essa configuração brevemente.

Crie um novo projeto quando solicitado; preserve o projeto existente em revisões. Salve versões numeradas na pasta do trabalho. Não sobrescreva arquivos alheios nem apague a cena aberta sem preservar o trabalho existente.

Modele pessoas com volumes em bloco, de proporções legíveis: tronco retangular com cantos discretamente suavizados e um volume simples para cabeça quando necessário ao enquadramento. Sem anatomia detalhada, dedos, articulações, rig, expressões ou animação corporal. Use cinza neutro; cores de identificação discretas só quando úteis para distinguir sujeitos ou solicitadas. Sem texturas. Refine a silhueta apenas o suficiente para um OTS ou close funcionar. Objetos são volumes simples; um celular pode ser um retângulo independente na altura necessária ao quadro. Não crie mãos para sustentá-lo.

Adicione chão, paredes, portas e volumes essenciais para profundidade, obstruções e leitura espacial. Não recrie os props finais em detalhe. Por padrão, só câmera e alvo invisível são animados.

Execute a construção e, após concluir a modelagem e a animação da câmera, faça a revisão de física descrita em [revisao-fisica.md](references/revisao-fisica.md), antes de entregar ao aluno para conferir e aprovar. A revisão respeita a intenção, o percurso, a composição e o estilo solicitados; por padrão, refina apenas câmera e alvo. Revise também movimentos de objetos somente quando já tiverem sido solicitados explicitamente.

Salve o .blend refinado e deixe a cena pronta para reprodução pela câmera no Blender. Verifique o percurso pela viewport, transformações e timeline, sem disparar render de imagem, animação ou playblast antes da aprovação. Em ajustes posteriores, revise novamente apenas os trechos afetados e suas transições antes de devolver ao aluno.

## 2. Revisar sem renderizar

Entregue um link clicável para o .blend usando seu caminho absoluto. Informe duração e um resumo curto do movimento. Diga: “Está pronto para você conferir no Blender. Reproduza pela câmera e me diga o que quer ajustar.” Não renderize nesta etapa.

Aplique feedbacks preservando o que já foi aceito. Salve nova versão e volte a disponibilizar para revisão. Não interprete um pedido de ajuste, silêncio ou elogio ambíguo como aprovação final. “Aprovado”, “pode renderizar” ou equivalente claro libera o render; não solicite uma segunda confirmação. Se disser “aprovado, mas mude o final”, faça a mudança e volte à revisão, a menos que também autorize explicitamente renderizar a versão ajustada.

## 3. Renderizar após aprovação

Avise brevemente que vai renderizar e execute. Exporte uma referência simples em MP4, com dimensões, fps e duração do projeto aprovado. Use iluminação e qualidade suficientes para ler os volumes, sem gastar em acabamento que será substituído. Se necessário, renderize sequência de imagens e converta para MP4.

Verifique que o arquivo existe, é reproduzível, tem duração e resolução esperadas e corresponde à versão aprovada. Inspecione amostras do início, percurso e final, e as junções se houver. Não apresente um render antigo como novo. Se falhar, informe a causa e o estado real.

Entregue o MP4 com link clicável para caminho absoluto, o caminho completo identificável e uma prévia quando suportada. Não basta dizer que terminou ou exibir somente a prévia.

Na mesma resposta, peça: “Agora me envie o ambiente, os personagens e os props que quer usar, e descreva o que acontece na cena, incluindo falas se houver.” Use mensagem normal para solicitar anexos. Se esses materiais já estiverem disponíveis, aproveite-os e pergunte apenas pelo que falta.

## 4. Preparar o prompt de geração

Leia [prompt-video.md](references/prompt-video.md). Inspecione o render aprovado real e as referências recebidas. Meça duração, proporção e fps quando as ferramentas permitirem; não herde tempos do planejamento nem invente o conteúdo de um arquivo ausente.

Escreva o prompt estruturado em inglês, pronto para copiar no Seedance 2.5, salvo preferência diferente do aluno. Explique a ordem dos anexos em português. A geração do vídeo e o upload não fazem parte desta entrega, salvo pedido explícito.

## Estado entre etapas

Mantenha um registro curto na pasta do trabalho: etapa atual, intenção, configurações, última versão do .blend, resultado da revisão de física e eventuais limitações de verificação, aprovação e a versão a que se refere, MP4 correspondente e mapa de referências. Atualize após uma mudança de etapa. Retome do estado real sem reconstruir trabalho aprovado. Não grave dados pessoais desnecessários nem caminhos do autor desta skill nos projetos dos alunos.

## Limites da entrega

Não prometa reprodução perfeita pelo gerador. Não diga que instalação, conexão, render ou geração ocorreram sem evidência. Preserve preferências explícitas do aluno, inclusive idioma, cores, duração e movimentos adicionais autorizados.
