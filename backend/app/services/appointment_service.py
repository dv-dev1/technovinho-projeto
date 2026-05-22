from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.config import settings
from app.models.appointment import Appointment, AppointmentStatus
from app.models.professional import Professional
from app.models.service import Service
from app.models.user import User, UserRole
from app.schemas.appointment import AppointmentCreate
from app.services import availability_service


class AppointmentNotFoundError(Exception):
    pass


class AppointmentForbiddenError(Exception):
    pass


class CancelDeadlineError(Exception):
    pass


class InvalidAppointmentStateError(Exception):
    pass


class SlotUnavailableError(Exception):
    pass


class ServiceNotFoundError(Exception):
    pass


def _to_out(row: Appointment) -> dict:
    prof_user = row.professional.user if row.professional else None
    return {
        "id": row.id,
        "client_id": row.client_id,
        "client_name": row.client.name if row.client else None,
        "professional_id": row.professional_id,
        "professional_name": prof_user.name if prof_user else None,
        "service_id": row.service_id,
        "service_name": row.service.name if row.service else None,
        "scheduled_at": row.scheduled_at,
        "status": row.status,
        "notes": row.notes,
    }


def _base_query():
    return (
        select(Appointment)
        .options(
            joinedload(Appointment.client),
            joinedload(Appointment.service),
            joinedload(Appointment.professional).joinedload(Professional.user),
        )
    )


def list_appointments(
    db: Session,
    *,
    current_user: User,
    status: AppointmentStatus | None = None,
    mine: bool = False,
) -> list[dict]:
    stmt = _base_query().order_by(Appointment.scheduled_at.desc())

    if current_user.role != UserRole.admin or mine:
        stmt = stmt.where(Appointment.client_id == current_user.id)
    if status is not None:
        stmt = stmt.where(Appointment.status == status)

    rows = db.scalars(stmt).unique().all()
    return [_to_out(r) for r in rows]


def create_appointment(db: Session, *, current_user: User, data: AppointmentCreate) -> dict:
    if current_user.role != UserRole.client:
        raise AppointmentForbiddenError()

    service = db.get(Service, data.service_id)
    if service is None:
        raise ServiceNotFoundError()

    scheduled = data.scheduled_at
    if scheduled.tzinfo is None:
        scheduled = scheduled.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    if scheduled <= now:
        raise InvalidAppointmentStateError("Agendamento deve ser no futuro")

    if not availability_service.is_slot_available(db, data.professional_id, scheduled):
        raise SlotUnavailableError()

    appointment = Appointment(
        client_id=current_user.id,
        professional_id=data.professional_id,
        service_id=data.service_id,
        scheduled_at=scheduled,
        status=AppointmentStatus.pending,
        notes=data.notes,
    )
    db.add(appointment)
    db.commit()

    row = db.scalar(_base_query().where(Appointment.id == appointment.id))
    return _to_out(row)


def cancel_appointment(db: Session, *, appointment_id: int, current_user: User) -> dict:
    row = db.scalar(_base_query().where(Appointment.id == appointment_id))
    if row is None:
        raise AppointmentNotFoundError()

    if current_user.role != UserRole.admin and row.client_id != current_user.id:
        raise AppointmentForbiddenError()

    if row.status == AppointmentStatus.cancelled:
        raise InvalidAppointmentStateError("Agendamento já cancelado")
    if row.status == AppointmentStatus.done:
        raise InvalidAppointmentStateError("Agendamento já concluído")

    scheduled = row.scheduled_at
    if scheduled.tzinfo is None:
        scheduled = scheduled.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    min_delta = timedelta(hours=settings.cancel_min_hours)
    if scheduled - now < min_delta:
        raise CancelDeadlineError(
            f"Cancelamento permitido até {settings.cancel_min_hours}h antes do horário"
        )

    row.status = AppointmentStatus.cancelled
    db.commit()
    db.refresh(row)
    row = db.scalar(_base_query().where(Appointment.id == appointment_id))
    return _to_out(row)
