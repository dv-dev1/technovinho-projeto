import streamlit as st

from lib import api, auth, ui

st.set_page_config(page_title="Technovinho", layout="wide")

auth.ensure_session_defaults()
ui.sidebar_nav()

role = ui.current_role()
summary = ui.role_summary(role)

if role == "guest":
    col1, col2, col3 = st.columns([1, 1.2, 1], gap="large")
    with col2:
        st.write("")
        ui.page_header(
            "Technovinho",
            "Acesse sua conta para continuar.",
            eyebrow="BARBEARIA"
        )
        with st.form("login", enter_to_submit=False):
            email = st.text_input("E-mail", placeholder="seu@email.com")
            password = st.text_input("Senha", type="password", placeholder="Sua senha")
            submitted = st.form_submit_button("Entrar", type="primary")
            
        if submitted:
            try:
                with st.spinner("Autenticando..."):
                    data = api.login(email, password)
                    user = api.me(data["access_token"])
                auth.set_authenticated_session(data["access_token"], user)
                st.rerun()
            except api.ApiError as err:
                ui.show_api_error(err)
else:
    ui.page_header(
        "Technovinho",
        summary["summary"] or "Painel de gestao da barbearia.",
        eyebrow="PAINEL",
    )

    main_col, side_col = st.columns([1.6, 1], gap="large")

    with main_col:
        quick_actions = ui.nav_items_for_role(role)[1:]
        if quick_actions:
            action_cols = st.columns(min(3, len(quick_actions)))
            for index, item in enumerate(quick_actions):
                with action_cols[index % len(action_cols)]:
                    ui.safe_page_link(item["path"], label=item["label"], icon=item["icon"])

    with side_col:
        with st.container(border=True):
            st.caption(f"{st.session_state.user_name or 'Usuario'} · {ui.role_label(role)}")
            if st.button("Sair"):
                auth.logout()
                st.rerun()

