import streamlit as st

from lib import api, ui

st.set_page_config(page_title="TECHNOVINHO", page_icon="✂️", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

ui.sidebar_nav()

st.title("TECHNOVINHO")
st.caption("Gestão de barbearias — APS")

with st.sidebar:
    if st.session_state.token:
        st.write(f"**{st.session_state.user['name']}**")
        st.caption(f"Perfil: {st.session_state.user['role']}")
        if st.button("Sair"):
            st.session_state.token = None
            st.session_state.user = None
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
                        st.session_state.user = api.me(data["access_token"])
                    st.session_state.token = data["access_token"]
                    st.rerun()
                except api.ApiError as err:
                    ui.show_api_error(err)

if st.session_state.token:
    if st.session_state.user.get("role") == "admin":
        st.success("Admin: use **👥 Profissionais** e **🗓️ Disponibilidade**.")
    elif st.session_state.user.get("role") == "client":
        st.success("Cliente: use **📅 Agendar** e **📋 Meus agendamentos**.")
    else:
        st.info("Use o menu conforme seu perfil.")
else:
    st.info("Entre para acessar as funcionalidades do TECHNOVINHO.")
