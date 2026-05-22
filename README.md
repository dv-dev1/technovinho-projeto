# TECHNOVINHO — API

Sistema de gestão de barbearias (APS E3 · GTIADS 2026.1).

| Camada | Stack |
|--------|--------|
| API | Python 3.11 · FastAPI · SQLAlchemy · Alembic |
| DB | PostgreSQL 15 |
| Auth | JWT (python-jose) · bcrypt (passlib) |

- **Trello:** https://trello.com/b/VPTx8KsB/technovinho
- **Legado (referência):** [api-agendamento-backend](https://github.com/dv-dev1/api-agendamento-backend)

## Prototipo

- **Link Figma view-only:** https://www.figma.com/design/O79fatjH5z0BStcQDUdwIv/Sem-t%C3%ADtulo?node-id=0-1&t=pxWPDhk6RPPRs3Ym-1
- **Wireframes principais (Figma-ready):** [docs/PROTOTIPO_FIGMA_WIREFRAMES.md](docs/PROTOTIPO_FIGMA_WIREFRAMES.md)
- **Arquivo visual importavel no Figma:** [docs/prototipo-figma-wireframes.svg](docs/prototipo-figma-wireframes.svg)

## Subir com Docker

```bash
cp .env.example .env
# Edite JWT_SECRET no .env

docker compose up --build
```

- API: http://localhost:8000
- OpenAPI: http://localhost:8000/docs

## Desenvolvimento local (sem Docker)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+psycopg2://technovinho:technovinho@localhost:5432/technovinho
export JWT_SECRET=dev-secret
alembic upgrade head
uvicorn app.main:app --reload
```

## Auth (curl)

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Admin","email":"admin@test.com","password":"senha12345","role":"admin"}'

curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"senha12345"}'

# Troque TOKEN
curl http://localhost:8000/api/auth/me -H "Authorization: Bearer TOKEN"
```

## Branches

- `main` — entrega APS
- `develop` — integração
- `feature/*` — uma task do Trello

## Paridade com backend Node

Ver [docs/API_PARITY.md](docs/API_PARITY.md).
