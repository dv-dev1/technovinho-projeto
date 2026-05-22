# Testes JMeter — TECHNOVINHO

Pré-requisitos: API no ar (`docker compose up`), usuário admin com token.

## Gerar token

```bash
curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"senha12345"}' | jq -r .access_token
```

## Executar

```bash
export JWT_TOKEN="cole_o_token_aqui"
jmeter -n -t tests/jmeter/technovinho.jmx -l tests/jmeter/results.jtl -e -o tests/jmeter/report
```

## Cenários (APS)

| # | Threads | Ramp-up | Request |
|---|---------|---------|---------|
| 1 | 50 | 10s | GET `/api/appointments` |
| 2 | 20 | 5s | POST `/api/appointments` |

Meta documentada: tempo médio GET < 500ms (registrar valor real no relatório HTML em `tests/jmeter/report`).

## Variáveis no `.jmx`

- `API_HOST` (default `localhost`)
- `API_PORT` (default `8000`)
- `JWT_TOKEN` (obrigatório)
