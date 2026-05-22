# Paridade API — Node → FastAPI

Referência: `api-agendamento-backend` (Express + MongoDB).

| Legado | FastAPI | Auth | Status |
|--------|---------|------|--------|
| `POST /api/auth/register` | `POST /api/auth/register` | não | ✅ |
| `POST /api/auth/login` | `POST /api/auth/login` | não | ✅ (`access_token` + `token_type`) |
| `GET /api/auth/me` | `GET /api/auth/me` | JWT | ✅ |
| `GET /api/services` | `GET /api/services` | JWT | ✅ (lista vazia até S2) |
| `POST /api/services` | `POST /api/services` | admin | ✅ básico |
| `GET /api/professionals` | `GET /api/professionals` | JWT | ✅ stub |
| `GET /api/appointments` | `GET /api/appointments` | JWT | ✅ stub |
| `GET /api/availability` | `GET /api/availability` | JWT | ✅ stub |

## Diferenças intencionais (APS)

| Item | Legado | TECHNOVINHO |
|------|--------|---------------|
| DB | MongoDB ObjectId | PostgreSQL SERIAL |
| Role barbeiro | `professional` | `barber` |
| Login response | `{ "token" }` | `{ "access_token", "token_type": "bearer" }` |
| Email duplicado | HTTP 400 | HTTP 409 |
| CORS | `:5173` (React) | `:8501` (Streamlit) + `:5173` |

## Próximos cards (S2+)

- CRUD completo serviços/profissionais
- POST appointments, availability
- Validação Pydantic em todos os bodies
