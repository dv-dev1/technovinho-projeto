from datetime import time

import streamlit as st

from lib import api, ui

DAY_LABELS = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]

ui.sidebar_nav()
ui.page_header(
    "Disponibilidade",
    "Grade semanal dos barbeiros.",
    eyebrow="Horarios",
)

token = ui.require_auth(roles=["admin"])

try:
    with st.spinner("Carregando profissionais..."):
        professionals = api.list_professionals(token)
except api.ApiError as err:
    ui.show_api_error(err)
    st.stop()

if not professionals:
    st.caption("Cadastre um profissional antes.")
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

main_col, action_col = st.columns([1.15, 0.95], gap="large")

with main_col:
    with st.container(border=True):
        ui.section_intro("Grade semanal")
        if slots:
            st.dataframe(
                [
                    {
                        "ID": s["id"],
                        "Dia": DAY_LABELS[s["day_of_week"]],
                        "Inicio": s["start_time"][:5],
                        "Fim": s["end_time"][:5],
                    }
                    for s in slots
                ],
                hide_index=True,
            )
        else:
            st.caption("Nenhuma faixa cadastrada.")

with action_col:
    with st.container(border=True):
        ui.section_intro("Remover faixa")
        if slots:
            to_delete = st.selectbox(
                "Faixa cadastrada",
                [
                    None,
                    *[
                        f"#{s['id']} - {DAY_LABELS[s['day_of_week']]} {s['start_time'][:5]}-{s['end_time'][:5]}"
                        for s in slots
                    ],
                ],
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
            st.caption("Nenhuma faixa para remover.")

    with st.container(border=True):
        ui.section_intro("Nova faixa")
        with st.form("add_slot", enter_to_submit=False):
            day = st.selectbox("Dia", range(7), format_func=lambda i: DAY_LABELS[i])
            works = st.checkbox("Trabalha neste dia", value=True)
            start = st.time_input("Inicio", value=time(9, 0))
            end = st.time_input("Fim", value=time(18, 0))
            submitted = st.form_submit_button("Salvar", type="primary")

        if submitted:
            if not works:
                st.warning("Marque o dia ou selecione outra data.")
            elif end <= start:
                st.error("Fim deve ser depois do inicio.")
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
