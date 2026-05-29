from __future__ import annotations

from collections.abc import Iterable
from html import escape

import streamlit as st

try:
    from lib import api
except ModuleNotFoundError:  # pragma: no cover - used by local unittest imports.
    from frontend.lib import api


NAV_ITEMS = {
    "guest": [
        {"path": "app.py", "label": "Inicio", "icon": ":material/home:"},
    ],
    "client": [
        {"path": "app.py", "label": "Inicio", "icon": ":material/home:"},
        {"path": "pages/4_Agendar.py", "label": "Agendar", "icon": ":material/calendar_month:"},
        {"path": "pages/3_Meus_Agendamentos.py", "label": "Meus agendamentos", "icon": ":material/event_note:"},
        {"path": "pages/7_Historico.py", "label": "Historico", "icon": ":material/history:"},
    ],
    "barber": [
        {"path": "app.py", "label": "Inicio", "icon": ":material/home:"},
        {"path": "pages/3_Meus_Agendamentos.py", "label": "Minha agenda", "icon": ":material/content_cut:"},
        {"path": "pages/7_Historico.py", "label": "Historico", "icon": ":material/history:"},
    ],
    "admin": [
        {"path": "app.py", "label": "Inicio", "icon": ":material/home:"},
        {"path": "pages/5_Admin_Dashboard.py", "label": "Dashboard admin", "icon": ":material/dashboard:"},
        {"path": "pages/0_Registro.py", "label": "Novo Cadastro", "icon": ":material/person_add:"},
        {"path": "pages/6_Servicos.py", "label": "Servicos", "icon": ":material/storefront:"},
        {"path": "pages/1_Profissionais.py", "label": "Profissionais", "icon": ":material/groups:"},
        {"path": "pages/2_Disponibilidade.py", "label": "Disponibilidade", "icon": ":material/schedule:"},
        {"path": "pages/3_Meus_Agendamentos.py", "label": "Operacao", "icon": ":material/event_note:"},
        {"path": "pages/7_Historico.py", "label": "Historico", "icon": ":material/history:"},
    ],
}

ROLE_COPY = {
    "guest": {
        "label": "Acesso",
        "eyebrow": "Technovinho",
        "summary": "",
        "highlights": [],
    },
    "client": {
        "label": "Cliente",
        "eyebrow": "Cliente",
        "summary": "Seus agendamentos e historico.",
        "highlights": [
            "Agendar",
            "Historico",
        ],
    },
    "barber": {
        "label": "Barbeiro",
        "eyebrow": "Barbeiro",
        "summary": "Sua agenda e atendimentos.",
        "highlights": [
            "Agenda",
            "Historico",
        ],
    },
    "admin": {
        "label": "Admin",
        "eyebrow": "Gestao",
        "summary": "Equipe, servicos e operacao.",
        "highlights": [
            "Operacao",
            "Equipe",
        ],
    },
}


def friendly_error(err: api.ApiError) -> str:
    detail = (err.detail or "").strip()
    if err.status_code == 0:
        return "API offline. Verifique se o backend esta rodando e tente novamente."
    if err.status_code == 400:
        return f"Revise os dados informados. {detail}".strip()
    if err.status_code == 401:
        if "Email ou senha invalidos" in detail:
            return detail
        return "Sessao expirada ou login invalido. Entre novamente."
    if err.status_code == 403:
        return "Acesso restrito para este perfil."
    if err.status_code == 404:
        return "Registro nao encontrado. Atualize a pagina e tente novamente."
    if err.status_code == 409:
        if "Email ja cadastrado" in detail:
            return detail
        return f"Conflito com um registro existente. {detail}".strip()
    if err.status_code >= 500:
        return "Erro interno na API. Tente novamente em alguns instantes."
    return detail or "Nao foi possivel concluir a operacao."


def show_api_error(err: api.ApiError) -> None:
    st.error(friendly_error(err))


def current_role() -> str:
    token = st.session_state.get("token")
    if not token:
        return "guest"
    role = st.session_state.get("user_role") or (st.session_state.get("user") or {}).get("role")
    return role or "guest"


def role_label(role: str | None = None) -> str:
    key = role or current_role()
    return ROLE_COPY.get(key, ROLE_COPY["guest"])["label"]


def nav_items_for_role(role: str | None = None) -> list[dict]:
    key = role or current_role()
    return list(NAV_ITEMS.get(key, NAV_ITEMS["guest"]))


def role_summary(role: str | None = None) -> dict:
    key = role or current_role()
    return ROLE_COPY.get(key, ROLE_COPY["guest"])


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Fraunces:wght@500;600&display=swap');

        :root {
          --tv-bg: #0a0a0a;
          --tv-bg-elevated: #0a0a0a;
          --tv-surface: #0a0a0a;
          --tv-surface-strong: #141414;
          --tv-line: #1e1e1e;
          --tv-line-strong: #2a2a2a;
          --tv-text: #e4e4e7;
          --tv-text-soft: #71717a;
          --tv-heading: #fafafa;
          --tv-accent: #c5a059;
          --tv-accent-strong: #b38b46;
          --tv-danger: #ef4444;
          --tv-shadow: none;
          --tv-radius: 0.5rem;
          --tv-radius-sm: 0.35rem;
        }

        .stApp {
          background: var(--tv-bg);
          color: var(--tv-text);
          font-family: 'Inter', -apple-system, sans-serif;
        }

        .stApp [data-testid="stAppViewContainer"] > .main {
          padding-top: 1.5rem;
        }

        .stApp [data-testid="block-container"] {
          max-width: 1000px;
          padding-top: 1rem;
          padding-bottom: 3rem;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
          background: var(--tv-bg);
          border-right: 1px solid var(--tv-line);
          font-family: 'Inter', sans-serif;
          padding-top: 0.5rem;
        }

        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] .tv-shell,
        [data-testid="stSidebar"] .tv-kicker,
        [data-testid="stSidebar"] .tv-muted,
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stCaption {
          color: var(--tv-text-soft);
        }

        [data-testid="stSidebar"] .stPageLink a {
          text-decoration: none;
          color: var(--tv-text) !important;
          opacity: 0.85;
          border-radius: var(--tv-radius-sm);
          padding: 0.35rem 0.5rem;
          margin-bottom: 0.15rem;
          transition: all 150ms ease;
          font-size: 0.88rem;
          font-weight: 500;
          letter-spacing: 0.01em;
        }

        [data-testid="stSidebar"] .stPageLink a *,
        [data-testid="stSidebar"] .stButton > button,
        [data-testid="stSidebar"] .stButton > button * {
          color: var(--tv-text-soft);
        }

        [data-testid="stSidebar"] .stPageLink a:hover {
          opacity: 1;
          background: var(--tv-line);
          color: var(--tv-heading) !important;
        }

        [data-testid="stSidebar"] .stPageLink a:visited {
          color: var(--tv-text) !important;
        }

        [data-testid="stSidebar"] .stButton > button,
        [data-testid="stSidebar"] .stPageLink a {
          border-radius: var(--tv-radius-sm);
        }

        /* ── Animations ── */
        .tv-shell {
          animation: tv-fade-up 280ms ease-out;
        }

        /* ── Page Header ── */
        .tv-page-header {
          padding: 0 0 1.25rem 0;
          margin-bottom: 1.5rem;
          border-bottom: 1px solid var(--tv-line);
        }

        .tv-eyebrow {
          text-transform: uppercase;
          letter-spacing: 0.1em;
          font-size: 0.7rem;
          font-weight: 600;
          color: var(--tv-accent);
          margin-bottom: 0.4rem;
        }

        .tv-page-header h1 {
          font-family: 'Fraunces', serif;
          font-size: clamp(1.75rem, 3.5vw, 2.25rem);
          font-weight: 500;
          line-height: 1.15;
          color: var(--tv-heading);
          margin: 0;
        }

        .tv-page-header p {
          margin: 0.4rem 0 0;
          color: var(--tv-text-soft);
          font-size: 0.88rem;
          max-width: 48ch;
        }

        /* ── Section Header ── */
        .tv-section {
          margin: 0.15rem 0 0.6rem;
        }

        .tv-section h2 {
          font-family: 'Inter', sans-serif;
          font-size: 0.95rem;
          color: var(--tv-heading);
          margin: 0;
          font-weight: 600;
          letter-spacing: 0.01em;
        }

        .tv-section p {
          margin: 0.15rem 0 0;
          color: var(--tv-text-soft);
          font-size: 0.82rem;
        }

        /* ── Kicker / Muted ── */
        .tv-kicker {
          display: inline-flex;
          align-items: center;
          gap: 0.4rem;
          padding: 0.25rem 0.65rem;
          border: 1px solid var(--tv-line);
          border-radius: var(--tv-radius-sm);
          background: transparent;
          color: var(--tv-text-soft);
          font-size: 0.72rem;
          font-weight: 600;
          letter-spacing: 0.06em;
          text-transform: uppercase;
          margin-bottom: 0.8rem;
        }

        .tv-muted {
          color: var(--tv-text-soft);
          font-size: 0.8rem;
        }

        .tv-inline-note {
          padding: 0.7rem 0.9rem;
          border: 1px solid var(--tv-line);
          border-radius: var(--tv-radius);
          background: var(--tv-surface-strong);
          color: var(--tv-text-soft);
          font-size: 0.82rem;
          margin: 0.3rem 0 0.8rem;
        }

        /* ── Containers / Cards ── */
        div[data-testid="stVerticalBlockBorderWrapper"] {
          border-radius: var(--tv-radius) !important;
          border: 1px solid var(--tv-line) !important;
          box-shadow: none !important;
          background: var(--tv-surface) !important;
          transition: border-color 200ms ease;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
          border-color: var(--tv-line-strong) !important;
        }

        /* ── Metrics ── */
        div[data-testid="stMetric"] {
          background: var(--tv-surface);
          border: 1px solid var(--tv-line);
          border-radius: var(--tv-radius);
          padding: 1rem 1.2rem;
          box-shadow: none;
        }

        div[data-testid="stMetric"] label {
          color: var(--tv-text-soft);
          font-weight: 500;
          font-size: 0.78rem;
          text-transform: uppercase;
          letter-spacing: 0.04em;
        }

        div[data-testid="stMetricValue"] {
          color: var(--tv-heading);
          font-family: 'Fraunces', serif;
        }

        /* ── Buttons ── */
        .stButton > button,
        .stDownloadButton > button,
        div[data-testid="stFormSubmitButton"] button {
          min-height: 2.4rem;
          border-radius: var(--tv-radius);
          border: 1px solid var(--tv-line);
          background: var(--tv-surface-strong);
          color: var(--tv-heading);
          font-weight: 500;
          font-size: 0.85rem;
          padding: 0.45rem 1rem;
          transition: all 150ms ease;
          box-shadow: none;
          margin-top: 0.15rem;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        div[data-testid="stFormSubmitButton"] button:hover {
          background: var(--tv-line);
          border-color: var(--tv-line-strong);
        }

        .stButton > button[kind="primary"],
        div[data-testid="stFormSubmitButton"] button[kind="primary"] {
          background: var(--tv-accent);
          color: #000000;
          border: 1px solid var(--tv-accent-strong);
          font-weight: 600;
        }

        .stButton > button[kind="primary"]:hover,
        div[data-testid="stFormSubmitButton"] button[kind="primary"]:hover {
          background: var(--tv-accent-strong);
          border-color: var(--tv-accent-strong);
        }

        /* ── Page Links (shortcuts) ── */
        .main .stPageLink a {
          border: 1px solid var(--tv-line) !important;
          border-radius: var(--tv-radius) !important;
          padding: 0.6rem 0.8rem !important;
          background: var(--tv-surface) !important;
          transition: all 150ms ease !important;
          font-weight: 500 !important;
          font-size: 0.85rem !important;
          color: var(--tv-text) !important;
        }

        .main .stPageLink a:hover {
          border-color: var(--tv-line-strong) !important;
          background: var(--tv-surface-strong) !important;
          color: var(--tv-heading) !important;
        }

        /* ── Inputs ── */
        .stSelectbox label,
        .stTextInput label,
        .stTextArea label,
        .stTimeInput label,
        .stDateInput label,
        .stNumberInput label,
        .stCheckbox label {
          font-weight: 500;
          color: var(--tv-text);
          font-size: 0.85rem;
        }

        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stDateInput input,
        .stTimeInput input {
          border-radius: var(--tv-radius) !important;
          border: 1px solid var(--tv-line) !important;
          background: transparent !important;
          color: var(--tv-heading) !important;
          -webkit-text-fill-color: var(--tv-heading) !important;
          caret-color: var(--tv-heading) !important;
          font-size: 0.88rem !important;
        }

        div[data-baseweb="select"] > div {
          border-radius: var(--tv-radius) !important;
          border: 1px solid var(--tv-line) !important;
          background: transparent !important;
          color: var(--tv-heading) !important;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder,
        .stNumberInput input::placeholder,
        .stDateInput input::placeholder,
        .stTimeInput input::placeholder {
          color: var(--tv-text-soft) !important;
          -webkit-text-fill-color: var(--tv-text-soft) !important;
        }

        div[data-baseweb="input"] input,
        div[data-baseweb="base-input"] input,
        div[data-baseweb="select"] input,
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div {
          color: var(--tv-heading) !important;
          -webkit-text-fill-color: var(--tv-heading) !important;
        }

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {
          gap: 0;
          border-bottom: 1px solid var(--tv-line);
        }

        .stTabs [data-baseweb="tab"] {
          color: var(--tv-text-soft);
          font-weight: 500;
          font-size: 0.85rem;
          padding: 0.6rem 1.2rem;
          border-bottom: 2px solid transparent;
          transition: all 150ms ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
          color: var(--tv-heading);
        }

        .stTabs [aria-selected="true"] {
          color: var(--tv-heading) !important;
          border-bottom-color: var(--tv-accent) !important;
        }

        /* ── Data Tables ── */
        [data-testid="stDataFrame"] {
          border: 1px solid var(--tv-line);
          border-radius: var(--tv-radius);
          overflow: hidden;
          background: transparent;
        }

        /* ── Alerts ── */
        [data-testid="stAlert"] {
          border-radius: var(--tv-radius);
          border: 1px solid var(--tv-line);
          background: var(--tv-surface-strong);
          color: var(--tv-text);
          font-size: 0.85rem;
        }

        [data-testid="stAlert"] p {
          color: var(--tv-text) !important;
        }

        /* ── Spacing ── */
        div[data-testid="stVerticalBlock"] > div:has(> div.stButton),
        div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stForm"]) {
          margin-bottom: 0.35rem;
        }

        .element-container {
          animation: tv-fade-up 200ms ease-out;
        }

        @keyframes tv-fade-up {
          from {
            opacity: 0;
            transform: translateY(6px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_nav() -> None:
    apply_theme()
    role = current_role()
    summary = role_summary(role)
    with st.sidebar:
        st.markdown(
            f"""
            <div class="tv-shell">
              <div class="tv-kicker">TECHNOVINHO</div>
              <div class="tv-muted">{escape(summary["eyebrow"])} · {escape(role_label(role))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for item in nav_items_for_role(role):
            safe_page_link(item["path"], label=item["label"], icon=item["icon"])


def page_header(title: str, caption: str, *, eyebrow: str | None = None) -> None:
    apply_theme()
    eyebrow_text = eyebrow or role_summary().get("eyebrow") or "TECHNOVINHO"
    st.markdown(
        f"""
        <div class="tv-shell tv-page-header">
          <div class="tv-eyebrow">{escape(eyebrow_text)}</div>
          <h1>{escape(title)}</h1>
          <p>{escape(caption)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def safe_page_link(path: str, *, label: str, icon: str | None = None) -> None:
    try:
        st.page_link(path, label=label, icon=icon)
    except Exception:  # pragma: no cover - Streamlit testing runner may not expose page metadata.
        st.caption(label)


def section_intro(title: str, caption: str | None = None) -> None:
    caption_html = f"<p>{escape(caption)}</p>" if caption else ""
    st.markdown(
        f"""
        <div class="tv-shell tv-section">
          <h2>{escape(title)}</h2>
          {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def inline_note(message: str) -> None:
    st.markdown(
        f'<div class="tv-shell tv-inline-note">{escape(message)}</div>',
        unsafe_allow_html=True,
    )


def status_badge(label: str, tone: str = "neutral") -> None:
    safe_tone = tone if tone in {"neutral", "success", "warning", "danger"} else "neutral"
    st.markdown(
        f'<div class="tv-badge tv-badge--{safe_tone}">{escape(label)}</div>',
        unsafe_allow_html=True,
    )


def require_auth(roles: Iterable[str] | None = None, *, st_module=st) -> str:
    if not st_module.session_state.get("token"):
        st_module.warning("Faca login na pagina inicial para continuar.")
        st_module.stop()

    user = st_module.session_state.get("user") or {}
    role = st_module.session_state.get("user_role") or user.get("role")
    allowed_roles = set(roles or [])
    if allowed_roles and role not in allowed_roles:
        st_module.warning("Acesso restrito para este perfil.")
        st_module.stop()

    return st_module.session_state.token
