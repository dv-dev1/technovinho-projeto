from collections.abc import Iterable

import streamlit as st

try:
    from lib import api
except ModuleNotFoundError:  # pragma: no cover - used by local unittest imports.
    from frontend.lib import api


def friendly_error(err: api.ApiError) -> str:
    detail = (err.detail or "").strip()
    if err.status_code == 0:
        return "API offline. Verifique se o backend esta rodando e tente novamente."
    if err.status_code == 400:
        return f"Revise os dados informados. {detail}".strip()
    if err.status_code == 401:
        return "Sessao expirada ou login invalido. Entre novamente."
    if err.status_code == 403:
        return "Acesso restrito para este perfil."
    if err.status_code == 404:
        return "Registro nao encontrado. Atualize a pagina e tente novamente."
    if err.status_code == 409:
        return f"Conflito com um registro existente. {detail}".strip()
    if err.status_code >= 500:
        return "Erro interno na API. Tente novamente em alguns instantes."
    return detail or "Nao foi possivel concluir a operacao."


def show_api_error(err: api.ApiError) -> None:
    st.error(friendly_error(err))


def sidebar_nav() -> None:
    with st.sidebar:
        st.page_link("app.py", label="Inicio", icon="🏠")
        st.page_link("pages/4_Agendar.py", label="Agendar", icon="📅")
        st.page_link("pages/3_Meus_Agendamentos.py", label="Meus agendamentos", icon="📋")
        st.page_link("pages/1_Profissionais.py", label="Profissionais", icon="👥")
        st.page_link("pages/2_Disponibilidade.py", label="Disponibilidade", icon="🗓️")


def require_auth(*, roles: Iterable[str] | None = None) -> str:
    if not st.session_state.get("token"):
        st.warning("Faca login na pagina inicial para continuar.")
        st.stop()

    user = st.session_state.get("user") or {}
    role = user.get("role")
    allowed_roles = set(roles or [])
    if allowed_roles and role not in allowed_roles:
        st.warning("Acesso restrito para este perfil.")
        st.stop()

    return st.session_state.token
