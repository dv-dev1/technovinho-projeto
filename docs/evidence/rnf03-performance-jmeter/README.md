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
3 passed in 0.05s
```

## Regressao

Comando:

```bash
venv\Scripts\python.exe -m pytest tests\integration
```

Resultado:

```text
28 passed in 27.16s
```

## Pendente para medicao real

O binario `jmeter` nao esta instalado nesta maquina:

```text
jmeter: comando nao reconhecido
```

Por isso, ainda falta executar a medicao real de carga e anexar o relatorio HTML ou Aggregate Report com tempos medios e percentual de erro.

Quando o JMeter estiver disponivel, executar:

```bash
jmeter -n -t tests/jmeter/technovinho.jmx -JJWT_TOKEN=TOKEN_VALIDO -l tests/jmeter/results.jtl -e -o tests/jmeter/report
```
