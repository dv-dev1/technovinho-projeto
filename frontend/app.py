import streamlit as st

from lib import api

st.set_page_config(page_title="TECHNOVINHO", page_icon="✂️", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

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
                    data = api.login(email, password)
                    st.session_state.token = data["access_token"]
                    st.session_state.user = api.me(st.session_state.token)
                    st.rerun()
                except api.ApiError as err:
                    st.error(err.detail)

if st.session_state.token:
    if st.session_state.user.get("role") == "admin":
        st.success("Logado como admin. Abra **Profissionais** ou **Disponibilidade** no menu.")
    else:
        st.warning("Perfil sem acesso admin às telas de gestão.")
else:
    st.info("Entre com usuário admin para gerenciar profissionais e disponibilidade.")
