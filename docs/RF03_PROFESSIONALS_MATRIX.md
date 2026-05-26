# RF03 - Matriz de CRUD de profissionais

Esta matriz registra a cobertura funcional do card `[Lucio] RF03 — CRUD de profissionais`.

## Escopo rastreado

| Caso | Resultado esperado | Evidencia no projeto |
|---|---|---|
| Listar profissionais | `GET /api/professionals` retorna nome, email, especialidade e status | `backend/app/routers/professionals.py`, `frontend/pages/1_Profissionais.py` |
| Criar com `user_id` de barber valido | Admin cria profissional com `201` | `backend/app/services/professional_service.py`, `tests/integration/test_professionals_rf03.py` |
| Duplicar `user_id` | Segunda criacao retorna `409` | `backend/app/services/professional_service.py`, `tests/integration/test_professionals_rf03.py` |
| Rejeitar usuario sem role `barber` | API retorna `400` | `backend/app/routers/professionals.py`, `tests/integration/test_professionals_rf03.py` |
| Inativar profissional | Admin pode atualizar `active=false` | `backend/app/services/professional_service.py`, `frontend/pages/1_Profissionais.py`, `tests/frontend/test_professionals.py` |
| Profissional inativo nao aparece no agendamento | Filtro `active_only=true` remove inativos da listagem usada na tela de agendamento | `backend/app/services/professional_service.py`, `frontend/lib/api.py`, `frontend/pages/4_Agendar.py`, `tests/integration/test_professionals_rf03.py` |

## Observacoes

- A tela administrativa cobre listagem, criacao e edicao de especialidade/status.
- O filtro de agendamento usa apenas profissionais ativos via `list_active_professionals(...)`.
- Esta matriz complementa o card principal de CRUD e serve como evidencia de rastreio para a APS.
