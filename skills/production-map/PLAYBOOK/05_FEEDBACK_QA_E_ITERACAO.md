# 05 — FEEDBACK, QA E ITERAÇÃO

## 1. O ciclo correto

1. gerar;
2. assistir sem defender o prompt;
3. nomear o que funcionou;
4. nomear o erro principal;
5. decidir se é revisão, insert ou nova estratégia;
6. atualizar regra e estado;
7. enviar prompt integral;
8. testar novamente.

## 2. Preserve o que funcionou

Uma revisão deve conter uma seção de lock explícito quando necessário:

```text
Preserve the approved face, wardrobe, camera, crop, lighting, material and successful movement. Correct only the leg anatomy and scale.
```

Não redesenhe um asset inteiro para corrigir um detalhe.

## 3. Classificação de erros

### Identidade

- rosto mudou;
- idade mudou;
- cabelo mudou;
- figurino mudou;
- personagem duplicou.

### Continuidade

- prop apareceu cedo;
- bolsa abriu sem ação;
- estado anterior voltou;
- luz e direção mudaram;
- frame inicial não corresponde.

### Geografia

- personagem atravessa rua inexistente;
- pai e filha separados por veículo;
- porta muda de posição;
- cenário é redesenhado.

### Anatomia e contagem

- membro oculto ou removido;
- pés duplicados;
- figura extra;
- objeto contado de forma errada.

### Câmera

- movimento genérico;
- ação fora de quadro;
- câmera abre por zoom digital;
- ausência de parallax;
- corte tratado como morph.

### Acting

- surpresa exagerada;
- sorriso permanente;
- reação antes do evento;
- personagem passiva;
- pai suspeito sem motivo.

### Física

- pés deslizam;
- peso desaparece;
- material flutua;
- líquido não molha;
- transformação não tem frente.

### Plataforma

- handle errado;
- referência aplicada à função errada;
- duração excedida;
- moderação disparada;
- áudio ou música automática.

## 4. Quando fazer insert

Faça um insert quando:

- a sequência principal funciona;
- falta cobertura de uma ação;
- a transição precisa de 5–10 segundos;
- um acting precisa de close;
- a montagem precisa respirar;
- existe um frame de continuidade estável.

Não regenere o bloco inteiro por reflexo.

## 5. Quando unir numa geração

Una quando:

- plataforma, ponte, objeto ou transformação precisa permanecer idêntica;
- a geometria não sobreviverá a duas gerações;
- a ação depende de continuidade de corpo e câmera;
- o segundo clip repetiria tempo de entrada.

## 6. Quando dividir

Divida quando:

- existe hard cut natural;
- muda o ambiente;
- o frame final pode virar asset;
- um bloco ficou sobrecarregado;
- a plataforma não suporta a duração;
- você precisa de alternativas de final.

## 7. Alternativas para montagem

Quando o filme estiver funcionando, gere “brisas” alternativas:

- três finais com a mesma entrada;
- inserts de acting;
- opções de transição;
- cobertura longa, macro e aérea;
- som e imagem com o mesmo ponto de corte.

Mantenha o início idêntico com um `FRM_` ou handle compartilhado.

## 8. QA antes de aprovar

### Narrativa

- A ação é entendida sem explicação externa?
- O bloco muda alguma coisa?
- A emoção acontece depois do estímulo?

### Continuidade

- Mesmo personagem?
- Mesmo prop?
- Mesmo estado?
- Mesmo lado e direção?
- O frame inicial é verdadeiro?

### Câmera

- Movimento motivado?
- Lente coerente?
- Escala legível?
- Corte limpo?
- Existe alça de edição?

### Acting

- Reação proporcional?
- Personagem continua agindo?
- Mãos, olhos e respiração coerentes?

### Física

- Pés tocam?
- Objetos têm peso?
- Contagens corretas?
- Materiais se comportam corretamente?

### Som

- Sem música automática?
- Sons pertencem à matéria?
- Diálogo controlado?

### Plataforma

- Handles exatos?
- Referências limitadas ao papel correto?
- Nenhum texto ou watermark?

## 9. Critério de aprovação

“Legal” pode liberar uma etapa criativa, mas o registro deve traduzir a aprovação em algo verificável:

- asset aprovado;
- versão escolhida;
- correção ainda pendente;
- arquivo/handle;
- próxima dependência.

