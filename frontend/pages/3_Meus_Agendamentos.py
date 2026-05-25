from datetime import datetime

import streamlit as st

from lib import api, auth

STATUS_LABELS = {
    "pending": "Pendente",
    "confirmed": "Confirmado",
    "cancelled": "Cancelado",
    "done": "Concluido",
}


def fmt_br(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return iso


st.title("Meus agendamentos")

auth.require_auth()

token = st.session_state.token
role = auth.current_role()

status_filter = st.selectbox(
    "Status",
    [None, "pending", "confirmed", "cancelled", "done"],
    format_func=lambda s: "Todos" if s is None else STATUS_LABELS.get(s, s),
)

try:
    rows = api.list_appointments(
        token,
        status=status_filter,
        mine=(role == "client"),
    )
except api.ApiError as err:
    st.error(err.detail)
    st.stop()

if not rows:
    st.info("Nenhum agendamento encontrado.")
    st.stop()

for row in rows:
    with st.container(border=True):
        st.markdown(
            f"**{row.get('service_name', 'Servico')}** - {row.get('professional_name', 'Profissional')}"
        )
        st.caption(f"Quando: {fmt_br(row['scheduled_at'])}")
        st.write(f"Status: **{STATUS_LABELS.get(row['status'], row['status'])}**")
        if row.get("notes"):
            st.write(f"Obs: {row['notes']}")

        if row["status"] not in ("cancelled", "done"):
            confirm = st.checkbox("Confirmo cancelamento", key=f"confirm_{row['id']}")
            if st.button("Cancelar agendamento", key=f"cancel_{row['id']}", disabled=not confirm):
                try:
                    api.cancel_appointment(token, row["id"])
                    st.success("Agendamento cancelado.")
                    st.rerun()
                except api.ApiError as err:
                    st.error(err.detail)
