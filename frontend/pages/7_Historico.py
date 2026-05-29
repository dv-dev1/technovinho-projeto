from datetime import datetime

import streamlit as st

from lib import api, auth, ui

ui.sidebar_nav()


def fmt_br(value: str) -> str:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d/%m/%Y %H:%M")


def fmt_money(value: object) -> str:
    return f"R$ {float(value or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


role = auth.current_role()
ui.page_header(
    "Historico",
    "Atendimentos concluidos.",
    eyebrow="Historico",
)

token = ui.require_auth()

try:
    with st.spinner("Carregando historico..."):
        rows = api.list_appointments(
            token,
            status="done",
            mine=(role == "client"),
        )
except api.ApiError as err:
    ui.show_api_error(err)
    st.stop()

if not rows:
    st.caption("Nenhum atendimento concluido.")
    st.stop()

metric_cols = st.columns(3)
metric_cols[0].metric("Atendimentos", len(rows))
metric_cols[1].metric(
    "Ultimo",
    fmt_br(rows[0]["scheduled_at"]).split(" ")[0],
)
metric_cols[2].metric(
    "Faturamento",
    fmt_money(sum(float(row.get("service_price") or 0) for row in rows)),
)

ui.section_intro("Registros")
st.dataframe(
    [
        {
            "Data": fmt_br(row["scheduled_at"]),
            "Cliente": row.get("client_name") or "-",
            "Servico": row.get("service_name") or "-",
            "Profissional": row.get("professional_name") or "-",
            "Valor": fmt_money(row.get("service_price")),
        }
        for row in rows
    ],
    hide_index=True,
)
