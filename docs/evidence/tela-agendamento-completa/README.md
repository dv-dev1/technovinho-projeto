# Evidencia - Tela de agendamento completa

Card Trello: https://trello.com/c/gG6G2AoN/22-cau%C3%AA-tela-de-agendamento-completa

Arquivos:

- `01-formulario-agendamento.png`: cliente logado preenchendo o fluxo de agendamento.
- `02-confirmacao-agendamento.png`: tela de confirmacao com codigo, status e resumo.
- `03-meus-agendamentos.png`: agendamento visivel na pagina Meus agendamentos.
- `04-db-appointments.txt`: consulta da tabela `appointments` no smoke test local.

Ambiente usado na evidencia:

- API FastAPI local com banco SQLite temporario seedado para smoke test.
- Usuario cliente ficticio: `cliente.aps@gmail.com`.
- Status inicial validado: `pending`.

Observacao: a validacao automatizada de API cria seu proprio banco temporario e confirma
login, `POST /api/appointments` e persistencia da linha em `appointments`.
