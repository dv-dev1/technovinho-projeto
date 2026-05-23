from datetime import date, datetime

import streamlit as st

from lib import api, scheduling

STATUS_LABELS = {
    "pending": "Pendente",
    "confirmed": "Confirmado",
    "cancelled": "Cancelado",
    "done": "Concluido",
}


def fmt_money(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_br(iso_value: str) -> str:
    try:
        return datetime.fromisoformat(iso_value.replace("Z", "+00:00")).strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return iso_value


def service_label(service: dict) -> str:
    price = fmt_money(float(service["price"]))
    return f"{service['name']} - {service['duration']} min - {price}"


def professional_label(professional: dict) -> str:
    specialty = professional.get("specialty") or "Profissional"
    return f"{professional['name']} - {specialty}"


st.title("Agendar horario")

if not st.session_state.get("token"):
    st.warning("Faca login na pagina inicial para agendar.")
    st.stop()

if st.session_state.get("user", {}).get("role") != "client":
    st.warning("Agendamentos devem ser criados por usuarios cliente.")
    st.stop()

token = st.session_state.token

confirmation = st.session_state.get("appointment_confirmation")
if confirmation:
    with st.container(border=True):
        st.success("Agendamento solicitado.")
        st.write(f"**Codigo:** #{confirmation['id']}")
        st.write(f"**Status:** {STATUS_LABELS.get(confirmation['status'], confirmation['status'])}")
        st.write(f"**Servico:** {confirmation.get('service_name') or 'Servico'}")
        st.write(f"**Profissional:** {confirmation.get('professional_name') or 'Profissional'}")
        st.write(f"**Quando:** {fmt_br(confirmation['scheduled_at'])}")
        if confirmation.get("notes"):
            st.write(f"**Observacoes:** {confirmation['notes']}")
        st.page_link("pages/3_Meus_Agendamentos.py", label="Abrir Meus agendamentos")
        if st.button("Novo agendamento"):
            st.session_state.appointment_confirmation = None
            st.rerun()
    st.stop()

try:
    services = [service for service in api.list_services(token) if service.get("active")]
    professionals = api.list_active_professionals(token)
except api.ApiError as err:
    st.error(err.detail)
    st.stop()

if not services:
    st.info("Nenhum servico ativo disponivel para agendamento.")
    st.stop()

if not professionals:
    st.info("Nenhum profissional ativo disponivel para agendamento.")
    st.stop()

st.subheader("1. Servico")
service_options = {service_label(service): service for service in services}
selected_service_label = st.selectbox("Escolha o servico", list(service_options.keys()))
selected_service = service_options[selected_service_label]

st.subheader("2. Profissional")
professional_options = {
    professional_label(professional): professional for professional in professionals
}
selected_professional_label = st.selectbox(
    "Escolha o profissional",
    list(professional_options.keys()),
)
selected_professional = professional_options[selected_professional_label]

st.subheader("3. Data")
selected_date = st.date_input("Escolha a data", min_value=date.today(), value=date.today())
if scheduling.is_past_date(selected_date):
    st.error("Escolha uma data de hoje em diante.")
    st.stop()

try:
    availability = api.list_availability(token, selected_professional["id"])
except api.ApiError as err:
    st.error(err.detail)
    st.stop()

day_availability = scheduling.availability_for_date(availability, selected_date)
slot_options = scheduling.build_slot_options(day_availability)

st.subheader("4. Horario")
if not slot_options:
    st.info("Nao ha horarios cadastrados para este profissional nesta data.")
    st.stop()

slot_labels = [slot["label"] for slot in slot_options]
selected_slot_label = st.selectbox("Escolha o horario", slot_labels)
selected_slot = slot_options[slot_labels.index(selected_slot_label)]

st.subheader("5. Observacoes")
notes = st.text_area("Notes opcional", placeholder="Preferencias ou observacoes para o atendimento")

scheduled_at = scheduling.combine_date_time(selected_date, selected_slot["time"])

with st.container(border=True):
    st.subheader("Resumo")
    st.write(f"**Servico:** {selected_service['name']}")
    st.write(f"**Profissional:** {selected_professional['name']}")
    st.write(f"**Data e hora:** {fmt_br(scheduled_at)}")
    st.write(f"**Valor:** {fmt_money(float(selected_service['price']))}")

    if st.button("Confirmar agendamento", type="primary"):
        payload = {
            "professional_id": selected_professional["id"],
            "service_id": selected_service["id"],
            "scheduled_at": scheduled_at,
            "notes": notes.strip() or None,
        }
        try:
            appointment = api.create_appointment(token, payload)
            st.session_state.appointment_confirmation = appointment
            st.rerun()
        except api.ApiError as err:
            st.error(err.detail)
