from datetime import time

import streamlit as st

from lib import api, ui

DAY_LABELS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

ui.sidebar_nav()

st.title("🗓️ Grade semanal — disponibilidade")

token = ui.require_auth(roles=["admin"])

try:
    with st.spinner("Carregando profissionais..."):
        professionals = api.list_professionals(token)
except api.ApiError as err:
    ui.show_api_error(err)
    st.stop()

if not professionals:
    st.info("Cadastre um profissional antes.")
    st.stop()

options = {f"{p['name']} (#{p['id']})": p["id"] for p in professionals}
choice = st.selectbox("Profissional", list(options.keys()))
professional_id = options[choice]

try:
    with st.spinner("Carregando disponibilidade..."):
        slots = api.list_availability(token, professional_id)
except api.ApiError as err:
    ui.show_api_error(err)
    st.stop()

if slots:
    st.dataframe(
        [
            {
                "ID": s["id"],
                "Dia": DAY_LABELS[s["day_of_week"]],
                "Início": s["start_time"][:5],
                "Fim": s["end_time"][:5],
            }
            for s in slots
        ],
        use_container_width=True,
    )
    to_delete = st.selectbox(
        "Remover faixa",
        [None] + [f"#{s['id']} — {DAY_LABELS[s['day_of_week']]} {s['start_time'][:5]}-{s['end_time'][:5]}" for s in slots],
    )
    if to_delete and st.button("Excluir selecionada"):
        slot_id = int(to_delete.split("#")[1].split(" ")[0])
        try:
            with st.spinner("Excluindo faixa..."):
                api.delete_availability(token, slot_id)
            st.success("Faixa removida.")
            st.rerun()
        except api.ApiError as err:
            ui.show_api_error(err)
else:
    st.caption("Nenhuma faixa cadastrada.")

st.divider()
st.subheader("Adicionar faixa")

with st.form("add_slot"):
    day = st.selectbox("Dia", range(7), format_func=lambda i: DAY_LABELS[i])
    works = st.checkbox("Trabalha neste dia?", value=True)
    start = st.time_input("Início", value=time(9, 0))
    end = st.time_input("Fim", value=time(18, 0))
    if st.form_submit_button("Salvar"):
        if not works:
            st.warning("Marque o dia ou use outro dia.")
        elif end <= start:
            st.error("Fim deve ser depois do início.")
        else:
            try:
                with st.spinner("Salvando disponibilidade..."):
                    api.create_availability(
                        token,
                        professional_id,
                        {
                            "day_of_week": day,
                            "start_time": start.strftime("%H:%M:%S"),
                            "end_time": end.strftime("%H:%M:%S"),
                        },
                    )
                st.success("Disponibilidade salva.")
                st.rerun()
            except api.ApiError as err:
                ui.show_api_error(err)
