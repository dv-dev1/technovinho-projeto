import streamlit as st

from lib import api, ui

SERVICE_PRESETS = {
    "corte_social": {
        "name": "Corte social",
        "description": "Corte classico, alinhado e versatil.",
        "duration": 35,
        "price": 35.0,
    },
    "corte_navalhado": {
        "name": "Corte navalhado",
        "description": "Acabamento com textura e laterais bem definidas.",
        "duration": 45,
        "price": 45.0,
    },
    "corte_degrade": {
        "name": "Corte degrade",
        "description": "Fade com transicao suave e acabamento preciso.",
        "duration": 50,
        "price": 50.0,
    },
}


def preset_options() -> dict[str, dict]:
    return {
        f"{preset['name']} - R$ {preset['price']:.2f} - {preset['duration']} min": preset
        for preset in SERVICE_PRESETS.values()
    }


ui.sidebar_nav()
ui.page_header(
    "Servicos",
    "Catalogo da barbearia.",
    eyebrow="Servicos",
)

token = ui.require_auth(["admin"])

try:
    with st.spinner("Carregando servicos..."):
        services = api.list_services(token)
except api.ApiError as err:
    ui.show_api_error(err)
    st.stop()

existing_names = {service["name"].strip().casefold() for service in services}
service_templates = preset_options()

tab_catalog, tab_new, tab_edit = st.tabs(["Catalogo", "Novo Servico", "Editar/Status"])

with tab_catalog:
    ui.section_intro("Catalogo")
    if not services:
        st.info("Nenhum servico cadastrado.")
    else:
        st.dataframe(
            [
                {
                    "Nome": service["name"],
                    "Duracao": f"{service['duration']} min",
                    "Preco": f"R$ {float(service['price']):.2f}",
                    "Ativo": "Sim" if service["active"] else "Nao",
                }
                for service in services
            ],
            hide_index=True,
        )

with tab_new:
    with st.container(border=True):
        ui.section_intro("Novo servico")
        selected_template_label = st.selectbox(
            "Selecione um corte padrao",
            list(service_templates.keys()),
            key="service_template",
        )
        selected_template = service_templates[selected_template_label]
        already_exists = selected_template["name"].casefold() in existing_names

        summary_left, summary_right = st.columns(2)
        with summary_left:
            st.metric("Duracao Base", f"{selected_template['duration']} min")
        with summary_right:
            st.metric("Preco Sugerido", f"R$ {selected_template['price']:.2f}")

        st.caption(selected_template["description"])
        with st.form("new_service", clear_on_submit=True, enter_to_submit=False):
            active = st.checkbox("Ativo", value=True)
            submitted = st.form_submit_button(
                "Adicionar Servico",
                type="primary",
                disabled=already_exists,
            )

        if submitted:
            try:
                with st.spinner("Salvando servico..."):
                    api.create_service(
                        token,
                        {
                            "name": selected_template["name"],
                            "description": selected_template["description"],
                            "duration": int(selected_template["duration"]),
                            "price": float(selected_template["price"]),
                            "active": active,
                        },
                    )
                st.success("Servico adicionado ao catalogo.")
                st.rerun()
            except api.ApiError as err:
                ui.show_api_error(err)

        if already_exists:
            st.info("Esse servico ja existe no seu catalogo.")

with tab_edit:
    if not services:
        st.warning("Adicione um servico primeiro.")
    else:
        edit_left, status_right = st.columns([1.1, 0.9], gap="large")

        with edit_left:
            with st.container(border=True):
                ui.section_intro("Editar Servico")
                service_options = {
                    f"{service['name']} (#{service['id']})": service
                    for service in services
                }
                selected_label = st.selectbox("Selecione o servico para modificar", list(service_options.keys()))
                selected_service = service_options[selected_label]

                with st.form(f"edit_service_{selected_service['id']}", enter_to_submit=False):
                    edit_name = st.text_input("Nome", value=selected_service["name"])
                    edit_description = st.text_area("Descricao", value=selected_service.get("description") or "")
                    
                    col_dur, col_price = st.columns(2)
                    with col_dur:
                        edit_duration = st.number_input(
                            "Duracao (min)",
                            min_value=15,
                            step=5,
                            value=int(selected_service["duration"]),
                        )
                    with col_price:
                        edit_price = st.number_input(
                            "Preco (R$)",
                            min_value=0.0,
                            step=1.0,
                            format="%.2f",
                            value=float(selected_service["price"]),
                        )
                    
                    edit_active = st.checkbox("Ativo", value=selected_service["active"])
                    edit_submitted = st.form_submit_button("Salvar alteracoes", type="primary")

                if edit_submitted:
                    if not edit_name.strip():
                        st.error("Informe o nome do servico.")
                    else:
                        try:
                            with st.spinner("Atualizando..."):
                                api.update_service(
                                    token,
                                    selected_service["id"],
                                    {
                                        "name": edit_name.strip(),
                                        "description": edit_description.strip() or None,
                                        "duration": int(edit_duration),
                                        "price": float(edit_price),
                                        "active": edit_active,
                                    },
                                )
                            st.success("Servico atualizado com sucesso!")
                            st.rerun()
                        except api.ApiError as err:
                            ui.show_api_error(err)

        with status_right:
            with st.container(border=True):
                ui.section_intro("Status")
                for service in services:
                    row_left, row_right = st.columns([1.4, 0.8])
                    with row_left:
                        st.write(f"**{service['name']}**")
                        st.caption(f"{service['duration']} min · R$ {float(service['price']):.2f}")
                    with row_right:
                        label = "Desativar" if service["active"] else "Ativar"
                        if st.button(label, key=f"status_{service['id']}"):
                            try:
                                with st.spinner("Atualizando..."):
                                    api.update_service(token, service["id"], {"active": not service["active"]})
                                st.success("Status modificado!")
                                st.rerun()
                            except api.ApiError as err:
                                ui.show_api_error(err)
