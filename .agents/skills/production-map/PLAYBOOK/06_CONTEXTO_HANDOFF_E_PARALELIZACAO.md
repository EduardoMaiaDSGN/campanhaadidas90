# 06 — CONTEXTO, HANDOFF E PARALELIZAÇÃO

## 1. Por que o registro vivo existe

Conversas crescem, são compactadas e podem ser reiniciadas. O projeto não pode depender da memória da janela.

Depois de decisões materiais, atualize:

- plano;
- bíblia;
- inventário;
- mapa de handles;
- registro vivo;
- handoff.

## 2. O que entra no registro vivo

- decisão aprovada;
- feedback que muda regra;
- asset aprovado e versão;
- handle confirmado;
- estratégia superseded;
- frame final real;
- duração real;
- fronteira de tarefa;
- próximo passo.

O registro não precisa duplicar prompts integrais. Ele precisa explicar o estado do filme.

## 3. O que não entra

- conversa casual;
- todas as variações rejeitadas em detalhe;
- prompt completo já copiável;
- elogio sem consequência;
- informação temporária sem impacto.

## 4. Handoff para nova conversa

`PROJETO/08_HANDOFF_CONTEXTO.md` deve permitir que uma nova IA responda:

- qual filme é este;
- qual é o estilo;
- quem são os personagens;
- quais são os handles;
- qual bloco terminou;
- qual é o último frame real;
- o que está aprovado;
- o que não pode ser repetido;
- qual é a próxima ação.

## 5. Paralelização

Paralelize somente quando o trabalho puder avançar sem duas tarefas alterarem o mesmo estado.

Boas divisões:

- blocos pares e ímpares;
- stills e animação;
- assets de ambientes e direção de uma sequência independente;
- pesquisa e produção;
- alternativas de final.

Más divisões:

- duas tarefas iterando o mesmo prompt;
- uma tarefa muda a bíblia enquanto outra gera com a versão antiga;
- dois clips que dependem da mesma plataforma em transformação contínua;
- duas pessoas inventando handles separadamente.

## 6. Contrato de propriedade

Registre uma tabela:

| Tarefa | Blocos | Pode editar | Não pode editar | Última sincronização |
|---|---|---|---|---|

Cada tarefa deve:

1. ler o registro antes de iniciar;
2. registrar mudanças imediatamente;
3. não duplicar bloco de outra tarefa;
4. avisar quando absorver ou mover uma fronteira;
5. deixar o próximo frame real documentado.

## 7. Sincronização

Quando uma tarefa altera uma fronteira:

- marque o bloco absorvido;
- indique o novo início da tarefa seguinte;
- remova repetição de entrada;
- registre o frame de passagem;
- atualize os handles usados.

## 8. Prompts históricos

Se prompts forem salvos em arquivos:

- trate-os como arquivo histórico;
- marque `APROVADO`, `REVISAR` ou `SUPERSEDED` fora do conteúdo copiável;
- não assuma que o arquivo mais recente por nome é a última decisão;
- o registro vivo decide.

## 9. Mensagem de recuperação

```text
Leia integralmente Replicate/README.md, Replicate/PLAYBOOK e todos os arquivos preenchidos de Replicate/PROJETO. Trate o registro vivo, a bíblia, o inventário e o mapa de handles como fontes de verdade. Não repita trabalho aprovado. Informe: último bloco aprovado, frame final real, bloco em teste, responsável e próxima ação.
```

