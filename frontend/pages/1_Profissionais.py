import streamlit as st

from lib import api, ui

ui.sidebar_nav()

st.title("Profissionais")

token = ui.require_auth(roles=["admin"])

try:
    with st.spinner("Carregando profissionais..."):
        professionals = api.list_professionals(token)
except api.ApiError as err:
    ui.show_api_error(err)
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

if professionals:
    st.divider()
    st.subheader("Editar profissional")

    professional_options = {
        f"{p['name']} (#{p['id']})": p
        for p in professionals
    }
    selected_label = st.selectbox("Selecione o profissional", list(professional_options.keys()))
    selected_professional = professional_options[selected_label]

    with st.form(f"update_professional_{selected_professional['id']}"):
        updated_specialty = st.text_input(
            "Especialidade",
            value=selected_professional.get("specialty") or "",
            key=f"specialty_{selected_professional['id']}",
        )
        updated_active = st.checkbox(
            "Ativo",
            value=selected_professional["active"],
            key=f"active_{selected_professional['id']}",
        )
        if st.form_submit_button("Salvar alteracoes"):
            try:
                with st.spinner("Atualizando profissional..."):
                    api.update_professional(
                        token,
                        selected_professional["id"],
                        {
                            "specialty": updated_specialty.strip() or None,
                            "active": updated_active,
                        },
                    )
                st.success("Profissional atualizado.")
                st.rerun()
            except api.ApiError as err:
                ui.show_api_error(err)

st.divider()
st.subheader("Novo profissional")

with st.form("create_professional"):
    user_id = st.number_input("user_id (usuario com role barber)", min_value=1, step=1)
    specialty = st.text_input("Especialidade")
    active = st.checkbox("Ativo", value=True)
    if st.form_submit_button("Criar"):
        try:
            with st.spinner("Criando profissional..."):
                api.create_professional(
                    token,
                    {"user_id": int(user_id), "specialty": specialty or None, "active": active},
                )
            st.success("Profissional criado.")
            st.rerun()
        except api.ApiError as err:
            ui.show_api_error(err)
