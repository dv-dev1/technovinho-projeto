# Evidencia - RF03 CRUD de profissionais

Card Trello: rastreio `[Lucio] RF03 — CRUD de profissionais`

Arquivos e comprovacoes:

- `docs/RF03_PROFESSIONALS_MATRIX.md`: matriz funcional do requisito.
- `tests/integration/test_professionals_rf03.py`: cobre criacao valida, duplicidade, rejeicao de usuario sem role `barber` e filtro `active_only`.
- `tests/frontend/test_professionals.py`: cobre o `PATCH` da UI admin para especialidade/status.
- `frontend/pages/1_Profissionais.py`: evidencia a listagem e manutencao via Streamlit.

Ambiente esperado para validacao:

- API FastAPI local com banco temporario nos testes automatizados.
- Autenticacao admin via JWT para criacao/edicao de profissionais.
- Tela de agendamento consumindo apenas profissionais ativos.

Resultado esperado da matriz:

- listar profissionais
- criar com `user_id` de barbeiro valido
- bloquear duplicidade de `user_id`
- impedir uso de usuario que nao seja `barber`
- ocultar profissional inativo do fluxo de agendamento
