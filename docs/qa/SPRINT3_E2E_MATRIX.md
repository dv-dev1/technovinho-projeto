# Sprint 3 - Testes E2E: dashboard, historico e cancelamento

Card Trello: **[Pedro] Sprint 3 - Testes E2E: dashboard, historico e cancelamento**

Esta matriz registra a validacao integrada das features avancadas da Sprint 3: **RF06 Cancelamento**, **RF07 Painel admin** e **RF08 Historico de atendimentos**.

## Criterios de aceite revisados

| Criterio do card | Status | Evidencia |
|---|---|---|
| Ambiente com dados de admin e client | Passou | Fixture automatizada em `tests/integration/test_sprint3_e2e.py` |
| Minimo 5 cenarios E2E executados | Passou | 5 testes em `tests/integration/test_sprint3_e2e.py` |
| Dashboard admin mostra agendamentos do dia | Passou | `test_admin_dashboard_shows_today_metrics` |
| Cliente agenda e aparece na fonte do dashboard admin | Passou | `test_client_booking_appears_in_admin_dashboard_source_data` |
| Cliente cancela dentro do prazo | Passou | `test_client_cancels_own_appointment_before_deadline` |
| Cancelamento fora do prazo e bloqueado | Passou | `test_cancellation_after_deadline_is_rejected` |
| Historico lista atendimentos concluidos com filtro | Passou | `test_history_lists_only_done_appointments_for_client` |
| Evidencia anexada | Passou | Esta matriz + teste automatizado + `docs/evidence/sprint3-e2e-dashboard-historico-cancelamento/README.md` |

## Matriz de cenarios

| ID | RF | Cenario | Passos resumidos | Resultado esperado | Status | Evidencia |
|---|---|---|---|---|---|---|
| S3-E2E-001 | RF07 | Admin abre dashboard e ve agendamentos do dia | Criar agendamento do dia, listar dados como admin e calcular metricas do dashboard | Dashboard considera o agendamento, receita estimada e profissional ativo | Passou | `test_admin_dashboard_shows_today_metrics` |
| S3-E2E-002 | RF07/RF04 | Cliente agenda e aparece no dashboard | Cliente cria agendamento; admin lista agendamentos usados pelo dashboard | Agendamento criado aparece na lista filtrada do dia | Passou | `test_client_booking_appears_in_admin_dashboard_source_data` |
| S3-E2E-003 | RF06 | Cliente cancela dentro do prazo | Criar agendamento futuro e chamar `/cancel` como dono | Status muda para `cancelled` | Passou | `test_client_cancels_own_appointment_before_deadline` |
| S3-E2E-004 | RF06 | Cancelamento fora do prazo | Criar agendamento com menos de 24h e chamar `/cancel` | API retorna `400` com regra de 24h | Passou | `test_cancellation_after_deadline_is_rejected` |
| S3-E2E-005 | RF08 | Historico mostra concluidos | Admin conclui atendimento passado; cliente consulta `status=done&mine=true` | Historico retorna somente atendimento concluido do cliente | Passou | `test_history_lists_only_done_appointments_for_client` |

## Execucao

Comando:

```bash
venv\Scripts\python.exe -m pytest tests\integration
```

Resultado esperado para aceite:

```text
Todos os testes de integracao passando, incluindo os 5 cenarios da Sprint 3.
```

## Observacoes

- A evidencia foi versionada no repositorio porque a automacao nao tem acesso direto ao Notion.
- Nenhum bug P0/P1 foi identificado na execucao automatizada.
- O criterio de video curto fica substituido por evidencia automatizada reprodutivel no repo; caso o time precise do video para a APS, usar esta matriz como roteiro de gravacao.
