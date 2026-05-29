from datetime import datetime

import streamlit as st

from lib import api, auth, ui

STATUS_LABELS = {
    "pending": "Pendente",
    "confirmed": "Confirmado",
    "cancelled": "Cancelado",
    "done": "Concluido",
}

STATUS_TONES = {
    "pending": "warning",
    "confirmed": "success",
    "cancelled": "danger",
    "done": "neutral",
}

ui.sidebar_nav()


def fmt_br(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return iso


token = ui.require_auth()
role = auth.current_role()

page_title = "Minha agenda" if role == "barber" else "Agendamentos"
page_caption = (
    "Seus atendimentos do dia."
    if role == "barber"
    else "Seus horarios marcados."
)
ui.page_header(page_title, page_caption, eyebrow="Agenda" if role == "barber" else "Agendamentos")

filter_col, _ = st.columns([1.2, 1], gap="large")
with filter_col:
    status_filter = st.selectbox(
        "Status",
        [None, "pending", "confirmed", "cancelled", "done"],
        format_func=lambda s: "Todos" if s is None else STATUS_LABELS.get(s, s),
    )

try:
    with st.spinner("Carregando agendamentos..."):
        rows = api.list_appointments(
            token,
            status=status_filter,
            mine=(role == "client"),
        )
except api.ApiError as err:
    ui.show_api_error(err)
    st.stop()

if not rows:
    st.caption("Nenhum agendamento encontrado.")
    st.stop()

ui.section_intro("Atendimentos")

for row in rows:
    with st.container(border=True):
        top_col, side_col = st.columns([1.7, 1], gap="large")
        with top_col:
            st.markdown(
                f"**{row.get('service_name', 'Servico')}**  \n{row.get('professional_name', 'Profissional')}"
            )
            st.caption(fmt_br(row['scheduled_at']))
            if row.get("client_name") and role != "client":
                st.write(f"Cliente: **{row['client_name']}**")
            if row.get("notes"):
                st.write(f"Observacoes: {row['notes']}")
        with side_col:
            ui.status_badge(
                STATUS_LABELS.get(row["status"], row["status"]),
                STATUS_TONES.get(row["status"], "neutral"),
            )

        if row["status"] not in ("cancelled", "done"):
            action_cols = st.columns(2)
            with action_cols[0]:
                confirm = st.checkbox("Confirmar cancelamento", key=f"confirm_{row['id']}")
                if st.button("Cancelar", key=f"cancel_{row['id']}", disabled=not confirm):
                    try:
                        with st.spinner("Cancelando agendamento..."):
                            api.cancel_appointment(token, row["id"])
                        st.success("Agendamento cancelado.")
                        st.rerun()
                    except api.ApiError as err:
                        ui.show_api_error(err)
            with action_cols[1]:
                if role == "admin":
                    if st.button("Concluir", key=f"complete_{row['id']}", type="primary"):
                        try:
                            with st.spinner("Concluindo atendimento..."):
                                api.complete_appointment(token, row["id"])
                            st.success("Atendimento concluido.")
                            st.rerun()
                        except api.ApiError as err:
                            ui.show_api_error(err)
