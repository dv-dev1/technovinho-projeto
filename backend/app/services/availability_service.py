from datetime import datetime, time

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.models.availability import Availability
from app.schemas.availability import AvailabilityCreate


class ProfessionalNotFoundError(Exception):
    pass


class AvailabilityNotFoundError(Exception):
    pass


class AvailabilityOverlapError(Exception):
    pass


class InvalidTimeRangeError(Exception):
    pass


def _times_overlap(start_a: time, end_a: time, start_b: time, end_b: time) -> bool:
    return start_a < end_b and start_b < end_a


def list_for_professional(db: Session, professional_id: int) -> list[Availability]:
    from app.models.professional import Professional

    if db.get(Professional, professional_id) is None:
        raise ProfessionalNotFoundError()
    return list(
        db.scalars(
            select(Availability)
            .where(Availability.professional_id == professional_id)
            .order_by(Availability.day_of_week, Availability.start_time)
        ).all()
    )


def list_all(db: Session) -> list[Availability]:
    return list(db.scalars(select(Availability).order_by(Availability.professional_id)).all())


def create_slot(db: Session, professional_id: int, data: AvailabilityCreate) -> Availability:
    from app.models.professional import Professional

    if db.get(Professional, professional_id) is None:
        raise ProfessionalNotFoundError()

    if data.end_time <= data.start_time:
        raise InvalidTimeRangeError()

    existing = list_for_professional(db, professional_id)
    for row in existing:
        if row.day_of_week == data.day_of_week and _times_overlap(
            row.start_time, row.end_time, data.start_time, data.end_time
        ):
            raise AvailabilityOverlapError()

    slot = Availability(
        professional_id=professional_id,
        day_of_week=data.day_of_week,
        start_time=data.start_time,
        end_time=data.end_time,
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot


def delete_slot(db: Session, availability_id: int) -> None:
    slot = db.get(Availability, availability_id)
    if slot is None:
        raise AvailabilityNotFoundError()
    db.delete(slot)
    db.commit()


def is_slot_available(db: Session, professional_id: int, scheduled_at: datetime) -> bool:
    if scheduled_at.tzinfo is not None:
        scheduled_at = scheduled_at.replace(tzinfo=None)

    day = scheduled_at.weekday()  # 0=Segunda (Python)
    slot_time = scheduled_at.time()

    rows = db.scalars(
        select(Availability).where(
            and_(
                Availability.professional_id == professional_id,
                Availability.day_of_week == day,
                Availability.start_time <= slot_time,
                Availability.end_time > slot_time,
            )
        )
    ).all()
    return len(rows) > 0
