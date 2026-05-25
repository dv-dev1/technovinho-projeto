import streamlit as st

from lib import api, auth, ui

st.set_page_config(page_title="TECHNOVINHO", page_icon=":scissors:", layout="wide")

auth.ensure_session_defaults()
ui.sidebar_nav()

st.title("TECHNOVINHO")
st.caption("Gestao de barbearias - APS")

with st.sidebar:
    if st.session_state.token:
        st.write(f"**{st.session_state.user_name or 'Usuario'}**")
        st.caption(f"Perfil: {st.session_state.user_role or 'sem perfil'}")
        if st.button("Sair"):
            auth.logout()
            st.rerun()
    else:
        st.subheader("Login")
        with st.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar"):
                try:
                    with st.spinner("Entrando..."):
                        data = api.login(email, password)
                        user = api.me(data["access_token"])
                    auth.set_authenticated_session(data["access_token"], user)
                    st.rerun()
                except api.ApiError as err:
                    ui.show_api_error(err)
        st.page_link("pages/0_Registro.py", label="Criar conta")

if st.session_state.token:
    if st.session_state.user_role == "admin":
        st.success("Admin: use Profissionais e Disponibilidade.")
    elif st.session_state.user_role == "client":
        st.success("Cliente: use Agendar e Meus agendamentos.")
    else:
        st.info("Use o menu conforme seu perfil.")
else:
    st.info("Entre ou crie uma conta para acessar as funcionalidades do TECHNOVINHO.")
