# TECHNOVINHO

Sistema de gestao de barbearias para a APS E3 (GTIADS 2026.1 / UNIPE).

## Repositorio

- Web: `https://github.com/dv-dev1/technovinho-projeto`
- Clone HTTPS: `https://github.com/dv-dev1/technovinho-projeto.git`
- Clone SSH: `git@github.com:dv-dev1/technovinho-projeto.git`
- Trello: `https://trello.com/b/VPTx8KsB/technovinho`
- Figma: `a definir pelo time`

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.11, FastAPI, SQLAlchemy, Alembic |
| Frontend | Streamlit |
| Banco | PostgreSQL 15 |
| Infra | Docker Compose |
| Auth | JWT (`python-jose`) + bcrypt (`passlib`) |

## Como clonar

```bash
git clone https://github.com/dv-dev1/technovinho-projeto.git
cd technovinho-projeto
```

Opcionalmente, voce pode trocar o `origin` para SSH depois que sua chave estiver configurada:

```bash
git remote set-url origin git@github.com:dv-dev1/technovinho-projeto.git
```

## Fluxo de branches

- `main`: versao de entrega / demo APS
- `develop`: integracao continua do time
- `feature/*`: implementacao de um card ou entrega fechavel

Exemplos de nomes:

- `feature/rf01-auth`
- `feature/docker-compose`
- `feature/historico-atendimentos`

O fluxo combinado do time esta em [CONTRIBUTING.md](CONTRIBUTING.md).

## Prototipo

- **Link Figma view-only:** https://www.figma.com/design/O79fatjH5z0BStcQDUdwIv/Sem-t%C3%ADtulo?node-id=0-1&t=pxWPDhk6RPPRs3Ym-1
- **Wireframes principais (Figma-ready):** [docs/PROTOTIPO_FIGMA_WIREFRAMES.md](docs/PROTOTIPO_FIGMA_WIREFRAMES.md)
- **Arquivo visual importavel no Figma:** [docs/prototipo-figma-wireframes.svg](docs/prototipo-figma-wireframes.svg)

## Subir com Docker

```bash
cp .env.example .env
# Edite JWT_SECRET no .env antes de subir

docker compose up --build
```

Servicos esperados:

- API: `http://localhost:8000`
- OpenAPI: `http://localhost:8000/docs`
- Frontend: `http://localhost:8501`

## Migrations

Com Docker em execucao:

```bash
docker compose exec api alembic upgrade head
```

Sem Docker:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set DATABASE_URL=postgresql+psycopg2://technovinho:technovinho@localhost:5432/technovinho
set JWT_SECRET=dev-secret
alembic upgrade head
uvicorn app.main:app --reload
```

## Testes automaticos de interface

Os testes de interface Streamlit usam `pytest` com `streamlit.testing.v1.AppTest`.

```bash
pip install -r frontend/requirements.txt -r requirements-dev.txt
pytest tests/ui
```

## Estrutura rapida

```text
backend/   API FastAPI, models, routers, services e Alembic
frontend/  app Streamlit e paginas
docs/      documentacao tecnica e paridade de API
```

## Auth (curl)

## Auth de exemplo

```bash
curl -X POST http://localhost:8000/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Admin\",\"email\":\"admin@test.com\",\"password\":\"senha12345\",\"role\":\"admin\"}"

curl -X POST http://localhost:8000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@test.com\",\"password\":\"senha12345\"}"
```

## Referencias

- Paridade do backend legado: [docs/API_PARITY.md](docs/API_PARITY.md)
- Fluxo de contribuicao: [CONTRIBUTING.md](CONTRIBUTING.md)
- Wiki tecnica: [docs/notion/README.md](docs/notion/README.md)
- Importacao para Notion: [docs/notion-import/Home.md](docs/notion-import/Home.md)
