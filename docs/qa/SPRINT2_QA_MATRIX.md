# Sprint 2 - QA: casos de teste CRUD e disponibilidade

Card Trello: **[Pedro] Sprint 2 - QA: casos de teste CRUD e disponibilidade**

Esta matriz consolida os casos de teste da Sprint 2 para validar CRUD de servicos, CRUD de profissionais, grade de disponibilidade e agendamento. O objetivo e dar rastreio para a APS e orientar o smoke manual apos cada merge em `develop`.

## Escopo

| Area | Rotas/telas principais | Objetivo QA |
|---|---|---|
| CRUD servicos | `GET /api/services`, `POST /api/services`, `PATCH /api/services/{id}`, tela `Servicos` | Validar cadastro, edicao, permissao admin e payload invalido |
| CRUD profissionais | `GET /api/professionals`, `POST /api/professionals`, `PATCH /api/professionals/{id}`, tela `Profissionais` | Validar profissional vinculado a usuario barbeiro, unicidade e filtro de ativos |
| Disponibilidade | `GET/POST /api/professionals/{id}/availability`, `GET/DELETE /api/availability`, tela `Disponibilidade` | Validar grade semanal, conflito de faixa e remocao |
| Agendamento | `POST /api/appointments`, `GET /api/appointments`, tela `Agendar` | Validar slots validos, conflitos, servico/profissional inativo e persistencia |

## Pre-condicoes

- Branch base atualizada a partir de `develop`.
- Stack local em execucao com `docker compose up --build`.
- Usuario `admin` autenticado para operacoes administrativas.
- Usuario `client` autenticado para fluxo de agendamento.
- Pelo menos um usuario com role `barber` disponivel para vincular a profissional.

## Matriz de casos

| ID | Area | Cenario | Passos resumidos | Resultado esperado | Tipo | Status inicial | Evidencia sugerida |
|---|---|---|---|---|---|---|---|
| S2-QA-001 | Servicos | Listar servicos | Chamar `GET /api/services` | Retorna `200` e lista JSON, mesmo vazia | API | Planejado | Curl/Postman |
| S2-QA-002 | Servicos | Criar servico como admin | Login admin, `POST /api/services` com nome, duracao, preco e ativo | Retorna `201`; item aparece no GET e na UI | API/UI | Planejado | Print UI + resposta API |
| S2-QA-003 | Servicos | Bloquear criacao sem token | `POST /api/services` sem `Authorization` | Retorna `401` | API | Planejado | Curl/Postman |
| S2-QA-004 | Servicos | Bloquear criacao como cliente | Login client, `POST /api/services` | Retorna `403` | API | Planejado | Curl/Postman |
| S2-QA-005 | Servicos | Rejeitar payload invalido | `POST /api/services` com `price=-1` ou `duration=0` | Retorna `422` ou erro de validacao claro | API | Planejado | Curl/Postman |
| S2-QA-006 | Servicos | Editar servico existente | Admin altera nome, preco ou status via `PATCH /api/services/{id}` | Retorna `200` com campos atualizados | API/UI | Planejado | Print antes/depois |
| S2-QA-007 | Servicos | Editar servico inexistente | Admin chama `PATCH /api/services/999999` | Retorna `404` | API | Planejado | Curl/Postman |
| S2-QA-008 | Servicos | Servico inativo fora do agendamento | Marcar servico `active=false` e abrir tela Agendar | Servico inativo nao deve ser selecionavel para novo agendamento ou API deve bloquear | E2E | Planejado | Print UI + resposta API |
| S2-QA-009 | Profissionais | Listar profissionais autenticado | Login, chamar `GET /api/professionals` | Retorna `200` com nome, email, especialidade e status | API | Coberto parcialmente | `docs/RF03_PROFESSIONALS_MATRIX.md` |
| S2-QA-010 | Profissionais | Bloquear listagem sem token | Chamar `GET /api/professionals` sem token | Retorna `401` | API | Planejado | Curl/Postman |
| S2-QA-011 | Profissionais | Criar profissional com usuario barber | Admin cria profissional para `user_id` de role `barber` | Retorna `201` e profissional aparece na listagem | API/UI | Coberto parcialmente | `tests/integration/test_professionals_rf03.py` |
| S2-QA-012 | Profissionais | Rejeitar usuario client/admin | Criar profissional para usuario sem role `barber` | Retorna `400` com mensagem de role invalida | API | Coberto parcialmente | `tests/integration/test_professionals_rf03.py` |
| S2-QA-013 | Profissionais | Rejeitar profissional duplicado | Repetir `POST /api/professionals` para mesmo `user_id` | Retorna `409` | API | Coberto parcialmente | `tests/integration/test_professionals_rf03.py` |
| S2-QA-014 | Profissionais | Editar especialidade | Admin altera `specialty` via `PATCH /api/professionals/{id}` | Retorna `200`; UI mostra nova especialidade | API/UI | Coberto parcialmente | `tests/frontend/test_professionals.py` |
| S2-QA-015 | Profissionais | Inativar profissional | Admin envia `active=false` | Profissional fica inativo e nao aparece com `active_only=true` | API/UI | Coberto parcialmente | `docs/RF03_PROFESSIONALS_MATRIX.md` |
| S2-QA-016 | Profissionais | Buscar profissional inexistente | `GET /api/professionals/999999` | Retorna `404` | API | Planejado | Curl/Postman |
| S2-QA-017 | Disponibilidade | Criar faixa valida | Admin cria disponibilidade com `day_of_week`, `start_time`, `end_time` | Retorna `201`; faixa aparece na listagem | API/UI | Planejado | Print UI + resposta API |
| S2-QA-018 | Disponibilidade | Rejeitar fim antes do inicio | Criar faixa com `end_time <= start_time` | Retorna `400` ou `422` | API | Planejado | Curl/Postman |
| S2-QA-019 | Disponibilidade | Rejeitar dia invalido | Criar faixa com `day_of_week < 0` ou `> 6` | Retorna erro de validacao/constraint | API | Planejado | Curl/Postman |
| S2-QA-020 | Disponibilidade | Rejeitar sobreposicao | Criar duas faixas no mesmo dia com horarios sobrepostos | Segunda chamada retorna `409` | API/UI | Planejado | Curl/Postman |
| S2-QA-021 | Disponibilidade | Remover faixa | Admin executa `DELETE /api/availability/{id}` | Retorna `204`; faixa some da listagem | API/UI | Planejado | Print antes/depois |
| S2-QA-022 | Disponibilidade | Bloquear remocao como cliente | Client executa `DELETE /api/availability/{id}` | Retorna `403` | API | Planejado | Curl/Postman |
| S2-QA-023 | Agendamento | Criar agendamento em slot valido | Cliente escolhe servico, profissional, data e horario dentro da disponibilidade | Retorna `201`; aparece em Meus agendamentos | E2E | Coberto parcialmente | `tests/integration/test_appointment_flow.py` |
| S2-QA-024 | Agendamento | Bloquear agendamento fora da grade | Cliente tenta horario sem disponibilidade | Retorna `400` com mensagem de indisponibilidade | API/E2E | Coberto parcialmente | `tests/integration/test_appointment_flow.py` |
| S2-QA-025 | Agendamento | Bloquear conflito de horario | Criar dois agendamentos sobrepostos para mesmo profissional | Segundo retorna `409` | API/E2E | Coberto parcialmente | `tests/integration/test_appointment_flow.py` |
| S2-QA-026 | Agendamento | Bloquear data passada | Cliente tenta agendar no passado | Retorna `400` ou erro de validacao claro | API/UI | Planejado | Curl/Postman |
| S2-QA-027 | Agendamento | Bloquear profissional inativo | Inativar profissional e tentar agendamento | Retorna erro de profissional indisponivel ou nao lista na UI | E2E | Planejado | Print UI + resposta API |
| S2-QA-028 | Agendamento | Confirmar persistencia | Criar agendamento e consultar `GET /api/appointments?mine=true` | Agendamento criado aparece para o cliente dono | API/E2E | Coberto parcialmente | `tests/integration/test_appointment_flow.py` |

## Criterio de execucao da Sprint 2

- Total documentado: 28 casos.
- Meta minima do card: executar pelo menos 80% dos casos, ou seja, 23 de 28.
- Bugs P0/P1 encontrados devem virar issue no GitHub, com link para o card Trello.
- Ao fim da Sprint 2, atualizar a coluna `Status inicial` para `Passou`, `Falhou`, `Bloqueado` ou `Nao aplicavel`.

## Evidencias esperadas

- Prints das telas administrativas e do fluxo de agendamento.
- Respostas `curl`, Postman ou Insomnia com URL, status HTTP e trecho do body.
- Logs curtos de testes automatizados quando existirem.
- Links de issues para bugs encontrados.
