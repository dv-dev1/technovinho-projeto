import streamlit as st

from lib import api, auth, ui

auth.ensure_session_defaults()
ui.sidebar_nav()
ui.page_header(
    "Profissionais",
    "Equipe da barbearia.",
    eyebrow="Equipe",
)

token = ui.require_auth(roles=["admin"])

try:
    with st.spinner("Carregando..."):
        professionals = api.list_professionals(token)
except api.ApiError as err:
    ui.show_api_error(err)
    st.stop()

summary_left, summary_right = st.columns([1.35, 0.65], gap="large")

with summary_left:
    with st.container(border=True):
        if professionals:
            st.dataframe(
                [
                    {
                        "Nome": p["name"],
                        "Email": p["email"],
                        "Especialidade": p.get("specialty") or "-",
                        "Status": "Ativo" if p["active"] else "Inativo",
                    }
                    for p in professionals
                ],
                hide_index=True,
            )
        else:
            st.caption("Nenhum barbeiro cadastrado.")

with summary_right:
    with st.container(border=True):
        active_total = sum(1 for p in professionals if p["active"])
        st.metric("Ativos", active_total)
        st.metric("Total", len(professionals))

content_left, content_right = st.columns([1.05, 0.95], gap="large")

with content_left:
    with st.container(border=True):
        ui.section_intro("Novo barbeiro")
        with st.form("create_professional", clear_on_submit=True, enter_to_submit=False):
            barber_name = st.text_input("Nome")
            barber_email = st.text_input("E-mail")
            barber_password = st.text_input("Senha inicial", type="password")
            barber_specialty = st.text_input("Especialidade")
            barber_active = st.checkbox("Ativo", value=True)
            submitted = st.form_submit_button("Criar", type="primary")

        if submitted:
            errors = auth.validate_register_form(
                name=barber_name,
                email=barber_email,
                password=barber_password,
                confirm_password=barber_password,
            )
            if errors:
                for error in errors:
                    st.error(error)
            else:
                try:
                    with st.spinner("Criando..."):
                        api.create_professional(
                            token,
                            {
                                "name": barber_name.strip(),
                                "email": barber_email.strip(),
                                "password": barber_password,
                                "specialty": barber_specialty.strip() or None,
                                "active": barber_active,
                            },
                        )
                    st.success("Barbeiro criado.")
                    st.rerun()
                except api.ApiError as err:
                    ui.show_api_error(err)

with content_right:
    with st.container(border=True):
        ui.section_intro("Editar")
        if not professionals:
            st.caption("Cadastre um barbeiro primeiro.")
        else:
            professional_options = {f"{p['name']} (#{p['id']})": p for p in professionals}
            selected_label = st.selectbox("Profissional", list(professional_options.keys()))
            selected_professional = professional_options[selected_label]

            st.caption(f"{selected_professional['email']} · {'Ativo' if selected_professional['active'] else 'Inativo'}")

            with st.form(f"update_professional_{selected_professional['id']}", enter_to_submit=False):
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
                save_submitted = st.form_submit_button("Salvar", type="primary")

            if save_submitted:
                try:
                    with st.spinner("Salvando..."):
                        api.update_professional(
                            token,
                            selected_professional["id"],
                            {
                                "specialty": updated_specialty.strip() or None,
                                "active": updated_active,
                            },
                        )
                    st.success("Atualizado.")
                    st.rerun()
                except api.ApiError as err:
                    ui.show_api_error(err)

