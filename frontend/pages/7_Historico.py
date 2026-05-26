from datetime import datetime

import streamlit as st

from lib import api, auth, ui

ui.sidebar_nav()

st.title("Historico de atendimentos")
st.caption("Atendimentos concluidos")

token = ui.require_auth()

try:
    with st.spinner("Carregando historico..."):
        rows = api.list_appointments(
            token,
            status="done",
            mine=(auth.current_role() == "client"),
        )
except api.ApiError as err:
    ui.show_api_error(err)
    st.stop()

if not rows:
    st.info("Nenhum atendimento concluido.")
    st.stop()


def fmt_br(value: str) -> str:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d/%m/%Y %H:%M")


def fmt_money(value: object) -> str:
    return f"R$ {float(value or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


st.dataframe(
    [
        {
            "Data": fmt_br(row["scheduled_at"]),
            "Servico": row.get("service_name") or "-",
            "Profissional": row.get("professional_name") or "-",
            "Valor": fmt_money(row.get("service_price")),
        }
        for row in rows
    ],
    use_container_width=True,
    hide_index=True,
)
