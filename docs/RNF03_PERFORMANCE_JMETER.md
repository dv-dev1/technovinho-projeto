# RNF03 - Desempenho + JMeter

Card Trello: **[Pedro] RNF03 - Desempenho + JMeter**

Esta matriz registra o rastreio do requisito nao funcional de desempenho da API. A meta APS documentada e manter operacoes principais com tempo medio abaixo de **500ms**, registrando gargalo e proposta de melhoria caso a meta nao seja atingida.

## Escopo RNF03

| Cenario | Ferramenta | Carga | Endpoint | Status | Evidencia |
|---|---|---|---|---|---|
| Cenario 1 | JMeter | 50 threads, ramp-up 10s, loop 5 | `GET /api/appointments` | Plano pronto | `tests/jmeter/technovinho.jmx` |
| Cenario 2 | JMeter | 20 threads, ramp-up 5s, loop 3 | `POST /api/appointments` | Plano pronto | `tests/jmeter/technovinho.jmx` + `tests/jmeter/appointments.csv` |

## Artefatos

| Arquivo | Funcao |
|---|---|
| `tests/jmeter/technovinho.jmx` | Plano JMeter com os 2 cenarios de desempenho |
| `tests/jmeter/appointments.csv` | Massa com horarios unicos para evitar conflito no POST |
| `tests/jmeter/README.md` | Como preparar token, seed e executar o JMeter |
| `tests/integration/test_jmeter_rnf03_plan.py` | Teste estrutural do plano JMeter e da massa CSV |

## Criterios de aceite

- [x] Plano JMeter versionado.
- [x] Cenario GET `/api/appointments` com 50 threads e ramp-up 10s.
- [x] Cenario POST `/api/appointments` com 20 threads.
- [x] Massa do POST varia `scheduled_at`.
- [x] Teste automatizado valida estrutura do `.jmx`.
- [x] Executar JMeter real e anexar relatorio/aggregate summary.
- [x] Registrar tempo medio real e comparar com meta de 500ms.

## Validacao local realizada

Foi feita validacao estrutural automatizada dos artefatos versionados e execucao real com Apache JMeter 5.6.3 instalado localmente em `C:\Users\pedro\Documents\Codex\tools`.

Comando:

```bash
venv\Scripts\python.exe -m pytest tests\integration\test_jmeter_rnf03_plan.py
```

Resultado:

```text
3 passed in 0.03s
```

Regressao de integracao:

```bash
venv\Scripts\python.exe -m pytest tests\integration
```

Resultado:

```text
28 passed in 27.30s
```

## Resultado JMeter real

Comando executado:

```bash
jmeter -n -t tests/jmeter/technovinho.jmx -JJWT_TOKEN=TOKEN_VALIDO -l results-rnf03.jtl -e -o report
```

Resumo geral:

```text
310 amostras em 10s, throughput 31.5/s, media geral 1ms, erro 0.00%
```

Resumo por endpoint:

| Endpoint | Amostras | Media | Min | Max | Erros |
|---|---:|---:|---:|---:|---:|
| `GET /api/appointments` | 250 | 1.77ms | 0ms | 98ms | 0 |
| `POST /api/appointments` | 60 | 2.83ms | 0ms | 80ms | 0 |

Conclusao: a meta documentada de tempo medio abaixo de **500ms** foi atingida no ambiente local Docker.

## Como executar a medicao real

1. Subir a stack:

```bash
docker compose up --build -d
```

2. Criar dados base:

- usuario admin/client;
- servico `id=1`;
- profissional `id=1`;
- disponibilidade ampla para as datas de `tests/jmeter/appointments.csv`.

3. Gerar token JWT e executar:

```bash
jmeter -n -t tests/jmeter/technovinho.jmx ^
  -JJWT_TOKEN=TOKEN_VALIDO ^
  -l tests/jmeter/results.jtl ^
  -e -o tests/jmeter/report
```

4. Registrar no PR:

- tempo medio do GET `/api/appointments`;
- tempo medio do POST `/api/appointments`;
- percentual de erro;
- observacao se a meta `<500ms` foi atingida.
