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
