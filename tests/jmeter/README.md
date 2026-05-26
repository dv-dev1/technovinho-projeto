# Testes JMeter - TECHNOVINHO

Pre-requisitos: API no ar (`docker compose up`), usuario cliente com token e massa base no banco.

## Gerar token

```bash
curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"cliente@test.com","password":"senha12345"}' | jq -r .access_token
```

## Preparar massa do POST

O cenario `POST /api/appointments` usa `tests/jmeter/appointments.csv` para variar `scheduled_at` e evitar que todas as threads tentem reservar o mesmo horario.

Antes da execucao real, garanta no banco:

- usuario cliente autenticado pelo `JWT_TOKEN`;
- `service_id=1` ativo;
- `professional_id=1` ativo;
- disponibilidade ampla para as datas existentes em `appointments.csv`.

## Executar

```bash
jmeter -n -t tests/jmeter/technovinho.jmx -JJWT_TOKEN="cole_o_token_aqui" -l tests/jmeter/results.jtl -e -o tests/jmeter/report
```

No PowerShell:

```powershell
jmeter -n -t tests/jmeter/technovinho.jmx -JJWT_TOKEN="cole_o_token_aqui" -l tests/jmeter/results.jtl -e -o tests/jmeter/report
```

## Cenarios APS

| # | Threads | Ramp-up | Loop | Request |
|---|---:|---:|---:|---|
| 1 | 50 | 10s | 5 | GET `/api/appointments` |
| 2 | 20 | 5s | 3 | POST `/api/appointments` |

Meta documentada: tempo medio GET < 500ms. Registrar valor real no relatorio HTML em `tests/jmeter/report`.

## Variaveis no `.jmx`

- `API_HOST` (default `localhost`)
- `API_PORT` (default `8000`)
- `JWT_TOKEN` (obrigatorio)

## Validacao estrutural sem JMeter

Se o binario `jmeter` nao estiver instalado na maquina, valide ao menos a estrutura do plano:

```bash
venv\Scripts\python.exe -m pytest tests\integration\test_jmeter_rnf03_plan.py
```
