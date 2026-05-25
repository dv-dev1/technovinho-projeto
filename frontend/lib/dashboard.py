from datetime import date, datetime


STATUS_LABELS = {
    "pending": "Pendente",
    "confirmed": "Confirmado",
    "cancelled": "Cancelado",
    "done": "Concluido",
}


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def today_appointments(rows: list[dict], *, today: date | None = None) -> list[dict]:
    reference = today or date.today()
    result = []
    for row in rows:
        try:
            scheduled_date = _parse_datetime(row["scheduled_at"]).date()
        except (KeyError, ValueError):
            continue
        if scheduled_date == reference:
            result.append(row)
    return result


def estimated_revenue(appointments: list[dict], services: list[dict]) -> float:
    prices = {service["id"]: float(service["price"]) for service in services}
    total = 0.0
    for appointment in appointments:
        if appointment.get("status") == "cancelled":
            continue
        total += prices.get(appointment.get("service_id"), 0.0)
    return total


def active_professionals_count(professionals: list[dict]) -> int:
    return sum(1 for professional in professionals if professional.get("active") is True)


def dashboard_rows(appointments: list[dict]) -> list[dict]:
    rows = []
    for appointment in appointments:
        try:
            scheduled = _parse_datetime(appointment["scheduled_at"])
            hour = scheduled.strftime("%H:%M")
        except (KeyError, ValueError):
            hour = "-"
        status = appointment.get("status", "-")
        rows.append(
            {
                "ID": appointment.get("id"),
                "Horario": hour,
                "Cliente": appointment.get("client_name") or "-",
                "Servico": appointment.get("service_name") or "-",
                "Profissional": appointment.get("professional_name") or "-",
                "Status": STATUS_LABELS.get(status, status),
            }
        )
    return rows


def format_money(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
