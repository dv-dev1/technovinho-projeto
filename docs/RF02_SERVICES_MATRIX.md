# RF02 - Matriz de CRUD de servicos

Card Trello: **[Pedro] RF02 - CRUD de servicos**

Esta matriz registra a validacao do requisito funcional **RF02**, responsavel pelo cadastro, listagem e manutencao dos servicos da barbearia.

## Escopo rastreado

| Caso | Fluxo | Esperado | Status | Evidencia |
|---|---|---|---|---|
| C1 | `GET /api/services` | Retorna `200` e lista de servicos | Passou | `tests/integration/test_services_rf02.py` |
| C2 | `POST /api/services` como admin | Retorna `201` e servico criado | Passou | `tests/integration/test_services_rf02.py` |
| C3 | `POST /api/services` sem auth | Retorna `401` | Passou | `tests/integration/test_services_rf02.py` |
| C4 | `POST /api/services` com role client | Retorna `403` | Passou | `tests/integration/test_services_rf02.py` |
| C5 | `POST /api/services` com `price=-1` | Retorna `422` | Passou | `tests/integration/test_services_rf02.py` |
| C6 | `PATCH /api/services/{id}` como admin | Retorna `200` e atualiza nome, duracao, preco e status | Passou | `tests/integration/test_services_rf02.py` |
| C7 | `PATCH /api/services/999999` | Retorna `404` | Passou | `tests/integration/test_services_rf02.py` |

## Evidencia de implementacao

| Camada | Arquivo |
|---|---|
| API | `backend/app/routers/services.py` |
| Schemas | `backend/app/schemas/service.py` |
| Regra de negocio | `backend/app/services/service_service.py` |
| UI admin | `frontend/pages/6_Servicos.py` |
| Testes de API | `tests/integration/test_services_rf02.py` |
| Testes frontend/API client | `tests/frontend/test_services.py` |

## Criterios de aceite

- [x] Servicos podem ser listados.
- [x] Admin pode criar servico.
- [x] Criacao sem token e bloqueada.
- [x] Cliente nao consegue criar servico.
- [x] Payload invalido e rejeitado.
- [x] Admin pode editar dados e status do servico.
- [x] Servico inexistente retorna erro claro.

## Validacao

Comando dedicado:

```bash
venv\Scripts\python.exe -m pytest tests\integration\test_services_rf02.py
```

Resultado:

```text
7 passed in 5.69s
```

Comando de regressao:

```bash
venv\Scripts\python.exe -m pytest tests\integration
```

Resultado:

```text
32 passed in 30.65s
```
