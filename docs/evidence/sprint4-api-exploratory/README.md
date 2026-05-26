# Evidencia - Sprint 4: 5 testes exploratorios de API

Card Trello: **[Pedro] 5 testes exploratorios de API**

## Escopo

Os 5 casos abaixo validam endpoints essenciais da API em formato exploratorio e reprodutivel:

1. Cadastro de usuario.
2. Login e emissao de JWT.
3. Listagem publica de servicos.
4. Criacao de agendamento com Bearer valido.
5. Bloqueio de agendamento com Bearer invalido.

## Evidencia automatizada

Arquivo:

```text
tests/integration/test_sprint4_api_exploratory.py
```

## Casos e trechos de resposta esperados

| Caso | URL | Status | Trecho validado |
|---|---|---|---|
| 1 | `POST /api/auth/register` | `201` | `name`, `email`; sem campo `password` |
| 2 | `POST /api/auth/login` | `200` | `access_token`, `token_type=bearer` |
| 3 | `GET /api/services` | `200` | lista JSON com `Corte Exploratorio` |
| 4 | `POST /api/appointments` | `201` | `status=pending`, `service_name`, `professional_name` |
| 5 | `POST /api/appointments` com token invalido | `401` | `detail` menciona token |

## Curl equivalente

> Substituir `TOKEN_VALIDO`, `professional_id`, `service_id` e `scheduled_at` conforme dados do ambiente.

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Usuario Exploratorio","email":"usuario.exploratorio@test.com","password":"senha12345","role":"client"}'

curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"cliente.exploratorio@test.com","password":"senha12345"}'

curl http://localhost:8000/api/services

curl -X POST http://localhost:8000/api/appointments \
  -H "Authorization: Bearer TOKEN_VALIDO" \
  -H "Content-Type: application/json" \
  -d '{"professional_id":1,"service_id":1,"scheduled_at":"2026-12-01T10:00:00","notes":"Teste exploratorio Sprint 4"}'

curl -X POST http://localhost:8000/api/appointments \
  -H "Authorization: Bearer token_invalido" \
  -H "Content-Type: application/json" \
  -d '{"professional_id":1,"service_id":1,"scheduled_at":"2026-12-01T10:00:00","notes":"Teste exploratorio Sprint 4"}'
```

## Resultado

Ultima execucao local:

```text
venv\Scripts\python.exe -m pytest tests\integration\test_sprint4_api_exploratory.py
5 passed in 3.69s

venv\Scripts\python.exe -m pytest tests\integration
30 passed in 29.32s
```
