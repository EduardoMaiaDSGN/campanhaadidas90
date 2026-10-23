# 03 — ASSETS, HANDLES E ESTADOS

## 1. O que merece virar asset

Crie um asset quando ele:

- reaparece;
- precisa ser reconhecido instantaneamente;
- será combinado em vários vídeos;
- possui geometria ou anatomia difícil;
- define a geografia de uma cena;
- contém um prop narrativo;
- possui contagens que não podem variar;
- terá estados antes/depois;
- costuma ser reinterpretado pela ferramenta;
- será usado como frame inicial ou final.

Não crie asset quando for:

- figurante irrelevante;
- objeto genérico de uso único;
- composição redundante de assets já aprovados;
- frame intermediário sem transformação nova;
- detalhe que a plataforma resolve de forma estável no prompt.

## 2. IDs canônicos

Use uma taxonomia estável no projeto:

| Prefixo | Tipo |
|---|---|
| `CH_` | personagem |
| `GRP_` | grupo ou figuração recorrente |
| `ENV_` | ambiente |
| `ART_` | obra, imagem interna ou universo visual |
| `CRT_` | criatura |
| `OBJ_` | objeto ou prop |
| `FX_` | efeito recorrente |
| `AUD_` | voz ou áudio |
| `FRM_` | frame de continuidade promovido a asset |

Exemplo de versão:

`ENV_03B_v02_APROVADO`

O ID canônico organiza o projeto. Ele não substitui o nome ou handle da plataforma.

## 3. Estados

Use somente estados claros:

- `A criar`
- `Em direção`
- `Gerando`
- `Em teste`
- `Revisar`
- `Aprovado`
- `Superseded`
- `Dispensado`

Nunca apague uma versão aprovada ao testar outra. Marque a relação entre versões.

## 4. Character sheets

Um character sheet útil deve resolver:

- frente;
- três-quartos;
- perfil;
- costas;
- corpo inteiro;
- rosto neutro;
- microexpressões relevantes;
- figurino completo;
- props recorrentes;
- materiais e escala.

Não produza sheets separados para props que já estejam perfeitamente legíveis e estáveis no sheet principal, salvo se o prop tiver close narrativo ou transformação.

## 5. Criaturas e anatomia

Para criaturas difíceis:

- escreva a anatomia como sistema de apoios e anexos;
- indique pontos de ligação ao corpo;
- determine contagens em todas as vistas;
- exija silhuetas separadas;
- diferencie design de estudo anatômico;
- trave cabeça, olhos, raízes de chifres, cauda e materiais;
- faça a escala relativa a um personagem ou ambiente.

“Seis pernas” é fraco. “Três pares portantes presos sob peito, caixa torácica central e pelve” é verificável.

## 6. Ambientes

Environment plates devem:

- existir sem protagonistas;
- ter geografia caminhável;
- possuir rotas e portas claras;
- preservar espaço para inserir personagens;
- ter escala e direção de luz;
- evitar aparência de archviz;
- incluir apenas figurantes genéricos necessários;
- registrar obras visíveis quando sua continuidade importar.

## 7. Estados antes/depois

Quando um ambiente ou obra será transformado:

1. aprove o estado base;
2. use o estado base como lock absoluto;
3. preserve câmera, crop, arquitetura e luz;
4. altere somente o estado narrativo;
5. produza alinhamento suficiente para metamorfose ou corte.

Não peça “uma versão parecida”. Peça “o mesmo espaço, mesma câmera, mesma composição, novo estado”.

## 8. Mundo navegável

Uma obra bonita não é automaticamente um set caminhável.

Ao converter arte em mundo:

- defina escala humana;
- crie piso contínuo;
- crie rota de 1,5–2 m quando necessário;
- preserve headroom;
- crie profundidades mensuráveis;
- garanta contato de pés;
- mantenha design e paleta pela matéria física;
- remova brushstroke ou flatness quando o objetivo for live-action;
- deixe espaço para câmera e blocking.

## 9. Mapa de handles

Antes de cada prompt de vídeo, consulte `PROJETO/05_MAPA_HANDLES_PLATAFORMA.md`.

Registre:

- ID canônico;
- nome visível;
- handle exato;
- tipo;
- versão;
- estado;
- screenshot ou evidência;
- duplicidades;
- observações de caixa e sufixo.

### Regras absolutas

- Preserve erros da plataforma.
- Preserve maiúsculas e minúsculas.
- Preserve sufixos.
- Não transforme nome visível em handle por suposição.
- Não use a versão antiga porque o nome parece mais simples.
- Não invente handle para “manter o prompt fluido”.
- Se o handle não foi confirmado, use o arquivo anexado ou aguarde a auditoria.

## 10. Referências dentro do prompt

Não escreva apenas “imagem 1” ou “imagem 2”.

Declare o papel:

```text
@handle_ambiente_aprovado is the absolute lock for architecture, camera and lighting.
@handle_protagonista is the exact identity and wardrobe reference for the protagonist.
The supplied artwork controls only palette and material language, never camera or composition.
```

Uma referência pode controlar somente:

- identidade;
- cor;
- material;
- anatomia;
- câmera;
- composição;
- geografia;
- estado inicial;
- estado final.

Explique o limite para impedir transferência indevida.

## 11. Frames promovidos

Promova um frame gerado a `FRM_` quando ele:

- é o último frame real de um bloco;
- é o primeiro frame desejado de uma continuação;
- contém mãos, props ou poses difíceis de recriar;
- resolve composição e continuidade;
- será usado em inserts alternativos.

Registre seu handle como qualquer outro asset.
