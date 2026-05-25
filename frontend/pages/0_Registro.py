import streamlit as st

from lib import api, auth, ui

ROLE_OPTIONS = {
    "Cliente": "client",
    "Barbeiro": "barber",
    "Admin": "admin",
}

st.title("Cadastro")
st.caption("Crie uma conta para acessar o TECHNOVINHO.")

auth.ensure_session_defaults()
ui.sidebar_nav()

with st.form("register"):
    name = st.text_input("Nome")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    confirm_password = st.text_input("Confirmacao da senha", type="password")
    role_label = st.selectbox("Perfil", list(ROLE_OPTIONS.keys()), index=0)

    if st.form_submit_button("Cadastrar", type="primary"):
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
                api.register(
                    {
                        "name": name.strip(),
                        "email": email.strip(),
                        "password": password,
                        "role": ROLE_OPTIONS[role_label],
                    }
                )
                st.success("Cadastro criado. Volte para a pagina inicial para fazer login.")
                st.page_link("app.py", label="Ir para login")
            except api.ApiError as err:
                ui.show_api_error(err)
