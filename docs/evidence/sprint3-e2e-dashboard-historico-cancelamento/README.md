# Evidencia - Sprint 3 E2E

Card Trello: **[Pedro] Sprint 3 - Testes E2E: dashboard, historico e cancelamento**

## Escopo validado

- RF07: Dashboard admin com agendamentos do dia, faturamento estimado e profissionais ativos.
- RF06: Cancelamento dentro do prazo e bloqueio fora do prazo.
- RF08: Historico filtrando atendimentos concluidos.

## Evidencia automatizada

Arquivo principal:

```text
tests/integration/test_sprint3_e2e.py
```

Cenarios:

1. Admin abre dashboard e ve agendamentos do dia.
2. Cliente agenda e o registro aparece na fonte de dados do dashboard.
3. Cliente cancela dentro do prazo.
4. Cancelamento fora do prazo e bloqueado.
5. Historico lista atendimentos concluidos com filtro.

## Comando de validacao

```bash
venv\Scripts\python.exe -m pytest tests\integration
```

## Resultado

Ultima execucao local:

```text
venv\Scripts\python.exe -m pytest tests\integration
25 passed in 26.73s

venv\Scripts\python.exe -m pytest tests\frontend\test_dashboard.py
4 passed in 0.03s
```

## Smoke manual com Docker

Executado em ambiente Docker local com:

```bash
docker compose up --build -d
```

Servicos confirmados:

```text
api       0.0.0.0:8000->8000/tcp
db        0.0.0.0:5432->5432/tcp (healthy)
frontend  0.0.0.0:8501->8501/tcp
```

Health checks:

```text
GET http://localhost:8000/api/health -> ok
GET http://localhost:8501 -> 200 OK
```

Dados criados no smoke:

```text
admin: admin.s3.1779809943@test.com
client: client.s3.1779809943@test.com
barber: barber.s3.1779809943@test.com
service_id: 1
professional_id: 1
today_appointment_id: 1
future_appointment_id: 2
past_appointment_id: 3
```

Cenarios validados:

| Cenario | Resultado |
|---|---|
| Admin ve fonte de dados do dashboard com agendamento do dia | `dashboardContainsToday=true` |
| Cliente agenda e registro aparece para admin | `todayAppointmentId=1` presente em `GET /api/appointments/` |
| Cliente cancela dentro do prazo | `futureAppointmentId=2`, status `cancelled` |
| Cancelamento fora do prazo e bloqueado | `deadlineStatus=400` |
| Historico lista atendimento concluido | `pastAppointmentId=3`, status `done`, `historyContainsPast=true` |

Observacao: para validar historico em Docker, o atendimento passado foi inserido diretamente no Postgres com `docker compose exec -T db psql ...`, pois a API bloqueia corretamente a criacao de agendamentos no passado. Depois disso, o fluxo voltou para a API: admin marcou o atendimento como concluido e o cliente consultou `GET /api/appointments/?status=done&mine=true`.
