import streamlit as st

from lib import api, dashboard

st.title("Dashboard admin")
st.caption("Visao do dia")

if not st.session_state.get("token"):
    st.warning("Faca login na pagina inicial.")
    st.stop()

if st.session_state.get("user", {}).get("role") != "admin":
    st.warning("Acesso restrito para administradores.")
    st.stop()

token = st.session_state.token

with st.spinner("Carregando dashboard..."):
    try:
        appointments = api.list_appointments(token)
        services = api.list_services(token)
        professionals = api.list_professionals(token)
    except api.ApiError as err:
        st.error(err.detail)
        st.stop()

today_rows = dashboard.today_appointments(appointments)
revenue = dashboard.estimated_revenue(today_rows, services)
active_professionals = dashboard.active_professionals_count(professionals)

metric_cols = st.columns(3)
metric_cols[0].metric("Agendamentos hoje", len(today_rows))
metric_cols[1].metric("Faturamento estimado", dashboard.format_money(revenue))
metric_cols[2].metric("Profissionais ativos", active_professionals)

st.divider()
st.subheader("Agendamentos de hoje")

table_rows = dashboard.dashboard_rows(today_rows)
if table_rows:
    st.dataframe(table_rows, use_container_width=True, hide_index=True)
else:
    st.info("Nenhum agendamento para hoje.")
