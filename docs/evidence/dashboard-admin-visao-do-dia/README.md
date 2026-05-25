# Evidencia - Dashboard admin visao do dia

Card Trello: https://trello.com/c/26BffEOZ/23-cau%C3%AA-dashboard-admin-vis%C3%A3o-do-dia

Arquivos:

- `01-dashboard-admin.png`: screenshot do dashboard admin com metricas e tabela.
- `02-dashboard-metrics.txt`: resumo das metricas esperadas no smoke test.

Ambiente usado na evidencia:

- API FastAPI local com banco SQLite temporario seedado para smoke test.
- Usuario admin ficticio: `admin.aps@gmail.com`.
- Dados seedados: 2 agendamentos hoje, sendo 1 cancelado; 1 profissional ativo.

Observacao: a regra de faturamento estimado ignora agendamentos cancelados, conforme RF07.
