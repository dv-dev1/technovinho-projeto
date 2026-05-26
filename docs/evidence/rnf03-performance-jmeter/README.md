# Evidencia - RNF03 Desempenho + JMeter

Card Trello: **[Pedro] RNF03 - Desempenho + JMeter**

## O que foi validado

- Plano JMeter versionado em `tests/jmeter/technovinho.jmx`.
- Cenario 1: `GET /api/appointments`, 50 threads, ramp-up 10s, loop 5.
- Cenario 2: `POST /api/appointments`, 20 threads, ramp-up 5s, loop 3.
- Massa CSV para variar `scheduled_at` no POST: `tests/jmeter/appointments.csv`.
- Documentacao de preparo/execucao: `tests/jmeter/README.md`.

## Validacao automatizada estrutural

Comando:

```bash
venv\Scripts\python.exe -m pytest tests\integration\test_jmeter_rnf03_plan.py
```

Resultado:

```text
3 passed in 0.03s
```

## Regressao

Comando:

```bash
venv\Scripts\python.exe -m pytest tests\integration
```

Resultado:

```text
28 passed in 27.30s
```

## Medicao real com JMeter

Foi instalada uma copia local do Apache JMeter 5.6.3 em:

```text
C:\Users\pedro\Documents\Codex\tools\apache-jmeter-5.6.3
```

Comando executado:

```bash
jmeter -n -t tests/jmeter/technovinho.jmx -JJWT_TOKEN=TOKEN_VALIDO -l results-rnf03.jtl -e -o report
```

Resumo do JMeter:

```text
summary = 310 in 00:00:10 = 31.5/s Avg: 1 Min: 0 Max: 98 Err: 0 (0.00%)
```

Aggregate summary:

| Endpoint | Samples | Avg | Min | Max | Errors | Error % |
|---|---:|---:|---:|---:|---:|---:|
| `GET /api/appointments` | 250 | 1.77ms | 0ms | 98ms | 0 | 0.00% |
| `POST /api/appointments` | 60 | 2.83ms | 0ms | 80ms | 0 | 0.00% |

Conclusao: meta RNF03 de media abaixo de 500ms atingida no ambiente local Docker.

## Arquivos gerados localmente

Os arquivos brutos foram gerados fora do repositório para evitar versionar o relatorio HTML completo:

```text
C:\Users\pedro\Documents\Codex\2026-05-26\tenho-um-projeto-integrado-no-github\jmeter-rnf03-run\results-rnf03.jtl
C:\Users\pedro\Documents\Codex\2026-05-26\tenho-um-projeto-integrado-no-github\jmeter-rnf03-run\report
```
