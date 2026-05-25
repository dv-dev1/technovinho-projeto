import streamlit as st

from lib import api, auth

st.title("Profissionais")

auth.require_auth(["admin"])

token = st.session_state.token

try:
    professionals = api.list_professionals(token)
except api.ApiError as err:
    st.error(err.detail)
    st.stop()

if professionals:
    st.dataframe(
        [
            {
                "ID": p["id"],
                "Nome": p["name"],
                "Email": p["email"],
                "Especialidade": p.get("specialty") or "-",
                "Ativo": "Sim" if p["active"] else "Nao",
            }
            for p in professionals
        ],
        use_container_width=True,
    )
else:
    st.info("Nenhum profissional cadastrado.")

st.divider()
st.subheader("Novo profissional")

with st.form("create_professional"):
    user_id = st.number_input("user_id (usuario com role barber)", min_value=1, step=1)
    specialty = st.text_input("Especialidade")
    active = st.checkbox("Ativo", value=True)
    if st.form_submit_button("Criar"):
        try:
            api.create_professional(
                token,
                {"user_id": int(user_id), "specialty": specialty or None, "active": active},
            )
            st.success("Profissional criado.")
            st.rerun()
        except api.ApiError as err:
            st.error(err.detail)
