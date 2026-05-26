---
date: 2026-05-25
tags:
  - spec
  - technovinho
  - streamlit
---

# RF01 - Cadastro e autenticacao JWT

## Escopo

Implementar o fluxo Streamlit do card `[Caue] RF01 - Cadastro e autenticacao (JWT)` consumindo a API FastAPI ja existente em `develop`.

## Comportamento

- Registro em pagina multipage com nome, email, senha, confirmacao de senha e role.
- Role `client` deve ser o padrao.
- Validacao client-side: email em formato valido, senha com pelo menos 8 caracteres e senhas iguais.
- Login deve chamar `/api/auth/login`, buscar `/api/auth/me` e salvar em `st.session_state`: `token`, `user_role`, `user_id`, `user_name`.
- Manter `st.session_state.user` por compatibilidade com telas existentes.
- Logout deve limpar dados de autenticacao da sessao.
- `require_auth(roles=None)` deve bloquear usuario sem token e bloquear role fora da lista informada.
- Paginas admin-only devem usar `require_auth(["admin"])`; pagina de agendamento deve aceitar cliente.

## Tratamento de erros

- API offline: mensagem clara, sem stack trace.
- `401`: "Email ou senha invalidos".
- `409`: "Email ja cadastrado".
- `422`: mensagem amigavel de dados invalidos.
- Nao exibir JWT completo na UI e nao armazenar senha em `session_state`.

## Nao escopo

- Alterar backend de autenticacao, exceto se a inspecao revelar incompatibilidade real.
- Implementar painel admin RF07.
- Persistir tokens/API keys em arquivos, notas, `.env` ou codigo.

## Aceite

- Cliente registra, loga e acessa pagina protegida.
- Logout invalida sessao local.
- Requests autenticadas seguintes enviam header `Authorization: Bearer <token>`.
