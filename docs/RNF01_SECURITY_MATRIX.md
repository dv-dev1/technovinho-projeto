# RNF01 - Matriz de seguranca JWT + bcrypt

Esta matriz registra o estado de seguranca exigido pelo card `[Caue] RNF01 - Seguranca (JWT + bcrypt)`.

## Rotas publicas

| Metodo | Rota | Justificativa |
|---|---|---|
| `POST` | `/api/auth/register` | Cadastro inicial de usuario. |
| `POST` | `/api/auth/login` | Emissao de JWT. |
| `GET` | `/` | Health simples da API. |
| `GET` | `/api/health` | Health check operacional. |
| `GET` | `/docs` | Documentacao FastAPI. |
| `GET` | `/openapi.json` | Schema OpenAPI. |

## Rotas protegidas por JWT

| Metodo | Rota | Dependencia |
|---|---|---|
| `GET` | `/api/auth/me` | `Depends(get_current_user)` |
| `GET` | `/api/services` | `Depends(get_current_user)` |
| `GET` | `/api/professionals` | `Depends(get_current_user)` |
| `GET` | `/api/professionals/{professional_id}` | `Depends(get_current_user)` |
| `GET` | `/api/professionals/{professional_id}/availability` | `Depends(get_current_user)` |
| `GET` | `/api/appointments` | `Depends(get_current_user)` |
| `POST` | `/api/appointments` | `Depends(get_current_user)` |
| `PATCH` | `/api/appointments/{appointment_id}/cancel` | `Depends(get_current_user)` |
| `GET` | `/api/availability` | `Depends(get_current_user)` |

## Rotas admin-only

| Metodo | Rota | Dependencia |
|---|---|---|
| `POST` | `/api/services` | `Depends(require_roles(UserRole.admin))` |
| `POST` | `/api/professionals` | `Depends(require_roles(UserRole.admin))` |
| `PATCH` | `/api/professionals/{professional_id}` | `Depends(require_roles(UserRole.admin))` |
| `POST` | `/api/professionals/{professional_id}/availability` | `Depends(require_roles(UserRole.admin))` |
| `DELETE` | `/api/availability/{availability_id}` | `Depends(require_roles(UserRole.admin))` |

## Senhas

- Cadastro usa `bcrypt.hashpw(password, bcrypt.gensalt())`.
- Login usa `bcrypt.checkpw(plain, hashed)`.
- A senha nunca deve ser salva em texto puro, retornada por `UserOut` ou armazenada em `st.session_state`.

## Testes de regressao

- `POST /api/appointments` sem header retorna `401` com `{"detail": "Not authenticated"}`.
- `POST /api/appointments` com `Authorization: Bearer xxx` retorna `401`.
- `POST /api/auth/register` salva a coluna `password` com prefixo bcrypt `$2b$`.
