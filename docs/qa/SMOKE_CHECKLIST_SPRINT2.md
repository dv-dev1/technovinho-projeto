# Smoke checklist - Sprint 2

Card Trello: **[Pedro] Sprint 2 - QA: casos de teste CRUD e disponibilidade**

Checklist rapido para rodar apos cada merge relevante em `develop`. Tempo alvo: 15 minutos.

## Preparacao

- [ ] Atualizar `develop`: `git checkout develop && git pull --ff-only`.
- [ ] Subir stack: `docker compose up --build -d`.
- [ ] Confirmar API: `GET http://localhost:8000/api/health`.
- [ ] Confirmar UI: abrir `http://localhost:8501`.
- [ ] Autenticar como `admin`.
- [ ] Autenticar como `client`.

## CRUD servicos

- [ ] Admin cria um servico ativo com duracao e preco validos.
- [ ] Servico criado aparece na listagem.
- [ ] Admin edita preco ou nome do servico.
- [ ] Cliente nao consegue criar servico.
- [ ] Payload invalido de servico retorna erro claro.

## CRUD profissionais

- [ ] Admin cria profissional vinculado a usuario `barber`.
- [ ] Profissional aparece na listagem com nome, email, especialidade e status.
- [ ] Duplicar o mesmo `user_id` retorna erro.
- [ ] Admin inativa profissional.
- [ ] Filtro/listagem de profissionais ativos nao retorna profissional inativo.

## Disponibilidade

- [ ] Admin cria faixa semanal valida para um profissional ativo.
- [ ] Faixa criada aparece apos recarregar a tela.
- [ ] Faixa com fim menor ou igual ao inicio e bloqueada.
- [ ] Faixa sobreposta no mesmo dia e bloqueada.
- [ ] Admin remove faixa e ela some da listagem.

## Agendamento

- [ ] Cliente cria agendamento em um slot valido.
- [ ] Agendamento aparece em `Meus agendamentos`.
- [ ] Agendamento fora da grade e bloqueado.
- [ ] Segundo agendamento sobreposto e bloqueado.
- [ ] UI mostra mensagem amigavel em erro de API.

## Fechamento

- [ ] Registrar evidencias em print ou resposta HTTP.
- [ ] Atualizar `docs/qa/SPRINT2_QA_MATRIX.md` com status real dos casos executados.
- [ ] Abrir issue para bug P0/P1.
- [ ] Comentar no card Trello o resumo: casos executados, falhas e bloqueios.
