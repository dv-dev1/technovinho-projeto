import streamlit as st

from lib import api, dashboard, ui

ui.sidebar_nav()
ui.page_header(
    "Dashboard",
    "Visao geral do dia.",
    eyebrow="Admin",
)

token = ui.require_auth(["admin"])

with st.spinner("Carregando dashboard..."):
    try:
        appointments = api.list_appointments(token)
        services = api.list_services(token)
        professionals = api.list_professionals(token)
    except api.ApiError as err:
        ui.show_api_error(err)
        st.stop()

today_rows = dashboard.today_appointments(appointments)
revenue = dashboard.estimated_revenue(today_rows, services)
active_professionals = dashboard.active_professionals_count(professionals)

metric_cols = st.columns(3)
metric_cols[0].metric("Cortes Hoje", len(today_rows))
metric_cols[1].metric("Faturamento do Dia", dashboard.format_money(revenue))
metric_cols[2].metric("Barbeiros na Ativa", active_professionals)

with st.container(border=True):
    ui.section_intro("Agenda do dia")
    table_rows = dashboard.dashboard_rows(today_rows)
    if table_rows:
        st.dataframe(table_rows, hide_index=True)
    else:
        st.info("Nenhum corte agendado para hoje.")
