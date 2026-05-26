import streamlit as st

from lib import api, ui

ui.sidebar_nav()

st.title("Servicos")
st.caption("Cadastro e manutencao do catalogo")

token = ui.require_auth(["admin"])

with st.form("new_service", clear_on_submit=True):
    st.subheader("Novo servico")
    name = st.text_input("Nome")
    description = st.text_area("Descricao")
    duration = st.number_input("Duracao (minutos)", min_value=15, value=30, step=5)
    price = st.number_input("Preco (R$)", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    active = st.checkbox("Ativo", value=True)
    submitted = st.form_submit_button("Cadastrar servico", type="primary")

if submitted:
    if not name.strip():
        st.error("Informe o nome do servico.")
    else:
        try:
            with st.spinner("Salvando servico..."):
                api.create_service(
                    token,
                    {
                        "name": name.strip(),
                        "description": description.strip() or None,
                        "duration": int(duration),
                        "price": float(price),
                        "active": active,
                    },
                )
            st.success("Servico cadastrado.")
            st.rerun()
        except api.ApiError as err:
            ui.show_api_error(err)

try:
    with st.spinner("Carregando servicos..."):
        services = api.list_services(token)
except api.ApiError as err:
    ui.show_api_error(err)
    st.stop()

st.subheader("Catalogo")
if not services:
    st.info("Nenhum servico cadastrado.")
    st.stop()

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
    use_container_width=True,
    hide_index=True,
)

st.divider()
st.subheader("Editar servico")

service_options = {
    f"{service['name']} (#{service['id']})": service
    for service in services
}
selected_label = st.selectbox("Selecione o servico", list(service_options.keys()))
selected_service = service_options[selected_label]

with st.form(f"edit_service_{selected_service['id']}"):
    edit_name = st.text_input("Nome do servico", value=selected_service["name"])
    edit_description = st.text_area("Descricao", value=selected_service.get("description") or "")
    edit_duration = st.number_input(
        "Duracao (minutos)",
        min_value=15,
        step=5,
        value=int(selected_service["duration"]),
    )
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
            with st.spinner("Atualizando servico..."):
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
            st.success("Servico atualizado.")
            st.rerun()
        except api.ApiError as err:
            ui.show_api_error(err)

for service in services:
    label = "Desativar" if service["active"] else "Ativar"
    if st.button(f"{label} {service['name']}", key=f"status_{service['id']}"):
        try:
            with st.spinner("Atualizando servico..."):
                api.update_service(token, service["id"], {"active": not service["active"]})
            st.success("Servico atualizado.")
            st.rerun()
        except api.ApiError as err:
            ui.show_api_error(err)
