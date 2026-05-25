import streamlit as st

from lib import api, auth

st.set_page_config(page_title="TECHNOVINHO", page_icon=":scissors:", layout="wide")

auth.ensure_session_defaults()

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
                    data = api.login(email, password)
                    user = api.me(data["access_token"])
                    auth.set_authenticated_session(data["access_token"], user)
                    st.success("Login realizado.")
                    st.rerun()
                except api.ApiError as err:
                    st.error(err.detail)
        st.page_link("pages/0_Registro.py", label="Criar conta")

if st.session_state.token:
    if st.session_state.user_role == "admin":
        st.success("Admin: abra Profissionais ou Disponibilidade.")
    elif st.session_state.user_role == "client":
        st.success("Cliente: abra Meus agendamentos ou Agendar horario.")
    else:
        st.info("Use o menu conforme seu perfil.")
else:
    st.info("Entre com sua conta ou crie um cadastro para acessar as paginas protegidas.")
