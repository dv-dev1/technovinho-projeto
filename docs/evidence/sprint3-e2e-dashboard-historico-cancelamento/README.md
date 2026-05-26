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
