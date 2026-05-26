# Paridade API — Node → FastAPI

Referência: `api-agendamento-backend` (Express + MongoDB).

| Legado | FastAPI | Auth | Status |
|--------|---------|------|--------|
| `POST /api/auth/register` | `POST /api/auth/register` | não | ✅ |
| `POST /api/auth/login` | `POST /api/auth/login` | não | ✅ (`access_token` + `token_type`) |
| `GET /api/auth/me` | `GET /api/auth/me` | JWT | ✅ |
| `GET /api/services` | `GET /api/services` | JWT | ✅ (lista vazia até S2) |
| `POST /api/services` | `POST /api/services` | admin | ✅ básico |
| `GET /api/professionals` | `GET /api/professionals` | JWT | ✅ join user |
| `POST /api/professionals` | `POST /api/professionals` | admin | ✅ |
| `GET /api/professionals/:id` | `GET /api/professionals/{id}` | JWT | ✅ |
| `GET /api/appointments` | `GET /api/appointments` | JWT | ✅ filtros `status`, `mine` |
| `POST /api/appointments` | `POST /api/appointments` | client | ✅ |
| cancel | `PATCH /api/appointments/{id}/cancel` | client/admin | ✅ prazo `CANCEL_MIN_HOURS` |
| `GET /api/availability/:professionalId` | `GET /api/professionals/{id}/availability` | JWT | ✅ |
| `POST availability` | `POST /api/professionals/{id}/availability` | admin | ✅ |
| `DELETE availability` | `DELETE /api/availability/{id}` | admin | ✅ |

## Cancelamento RF06

`PATCH /api/appointments/{id}/cancel` permite cancelamento pelo cliente dono
do agendamento ou por um administrador. A antecedencia minima e configurada
por `CANCEL_MIN_HOURS` (padrao: `24`); fora do prazo a API responde HTTP 400.

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
