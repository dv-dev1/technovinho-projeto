import streamlit as st

from lib import api, auth, ui

auth.ensure_session_defaults()
ui.require_auth(["admin"])
ui.sidebar_nav()
ui.page_header(
    "Novo Cadastro",
    "Crie contas de acesso ao sistema.",
    eyebrow="Admin",
)

form_col, info_col = st.columns([1.2, 0.8], gap="large")

with form_col:
    with st.container(border=True):
        with st.form("register", enter_to_submit=False):
            name = st.text_input("Nome")
            email = st.text_input("E-mail")
            
            roles = {"Cliente": "client", "Barbeiro": "barber", "Admin": "admin"}
            role_selected = st.selectbox("Perfil", list(roles.keys()))
            
            password = st.text_input("Senha", type="password")
            confirm_password = st.text_input("Confirmar senha", type="password")
            submitted = st.form_submit_button("Cadastrar", type="primary")

        if submitted:
            errors = auth.validate_register_form(
                name=name,
                email=email,
                password=password,
                confirm_password=confirm_password,
            )
            if errors:
                for error in errors:
                    st.error(error)
            else:
                try:
                    role_val = roles[role_selected]
                    api.register(
                        {
                            "name": name.strip(),
                            "email": email.strip(),
                            "password": password,
                            "role": role_val,
                        }
                    )
                    st.success("Cadastro criado.")
                except api.ApiError as err:
                    ui.show_api_error(err)

with info_col:
    with st.container(border=True):
        ui.section_intro("Perfis")
        st.caption("Cliente — agenda horarios.")
        st.caption("Barbeiro — visualiza sua agenda.")
        st.caption("Admin — acesso completo.")

