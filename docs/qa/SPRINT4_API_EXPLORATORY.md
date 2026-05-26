# Sprint 4 - 5 testes exploratorios de API

Card Trello: **[Pedro] 5 testes exploratorios de API**

Esta matriz registra os 5 testes exploratorios exigidos na Sprint 4, com status esperado, evidencia automatizada e comandos equivalentes em `curl` para reproducao manual.

## Criterios de aceite revisados

| Criterio | Status | Evidencia |
|---|---|---|
| 5 casos exploratorios documentados | Passou | Esta matriz |
| Evidencia por caso com URL, status e trecho do body | Passou | `docs/evidence/sprint4-api-exploratory/README.md` |
| Testes executaveis no repositorio | Passou | `tests/integration/test_sprint4_api_exploratory.py` |
| Caso 1: `POST /api/auth/register` body valido | Passou | `test_01_register_valid_user_returns_201_without_password` |
| Caso 2: `POST /api/auth/login` | Passou | `test_02_login_valid_credentials_returns_bearer_token` |
| Caso 3: `GET /api/services` sem authorization | Passou | `test_03_get_services_without_authorization_returns_200_list` |
| Caso 4: `POST /api/appointments` com Bearer valido | Passou | `test_04_post_appointment_with_valid_bearer_returns_201` |
| Caso 5: `POST /api/appointments` com Bearer invalido | Passou | `test_05_post_appointment_with_invalid_bearer_returns_401` |

## Matriz dos 5 testes

| ID | Request | Pre-condicao | Esperado | Status | Evidencia |
|---|---|---|---|---|---|
| S4-API-001 | `POST /api/auth/register` | Body valido com nome, email, senha e role | `201`; body sem password | Passou | Teste automatizado + README evidencia |
| S4-API-002 | `POST /api/auth/login` | Usuario client seedado no teste | `200`; `access_token` e `token_type=bearer` | Passou | Teste automatizado + README evidencia |
| S4-API-003 | `GET /api/services` sem Authorization | Servico ativo seedado no teste | `200`; lista JSON | Passou | Teste automatizado + README evidencia |
| S4-API-004 | `POST /api/appointments` com Bearer valido | Client, service, professional e availability validos | `201`; status `pending` | Passou | Teste automatizado + README evidencia |
| S4-API-005 | `POST /api/appointments` com Bearer invalido | Payload valido, token invalido | `401`; erro menciona token | Passou | Teste automatizado + README evidencia |

## Validacao automatizada

Comando:

```bash
venv\Scripts\python.exe -m pytest tests\integration\test_sprint4_api_exploratory.py
```

Validacao completa de integracao:

```bash
venv\Scripts\python.exe -m pytest tests\integration
```
