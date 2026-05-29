from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.security import hash_password
from app.models.professional import Professional
from app.models.user import User, UserRole
from app.schemas.professional import ProfessionalCreate, ProfessionalUpdate


class ProfessionalAlreadyExistsError(Exception):
    pass


class ProfessionalNotFoundError(Exception):
    pass


def _to_out(professional: Professional) -> dict:
    user = professional.user
    return {
        "id": professional.id,
        "user_id": professional.user_id,
        "name": user.name,
        "email": user.email,
        "specialty": professional.specialty,
        "active": professional.active,
    }


def list_professionals(db: Session, *, active_only: bool = False) -> list[dict]:
    stmt = select(Professional).options(joinedload(Professional.user))
    if active_only:
        stmt = stmt.where(Professional.active.is_(True))
    rows = db.scalars(stmt).unique().all()
    return [_to_out(p) for p in rows]


def get_professional(db: Session, professional_id: int) -> dict:
    professional = db.scalar(
        select(Professional)
        .options(joinedload(Professional.user))
        .where(Professional.id == professional_id)
    )
    if professional is None:
        raise ProfessionalNotFoundError()
    return _to_out(professional)


def create_professional(db: Session, data: ProfessionalCreate) -> dict:
    existing = db.scalar(select(User).where(User.email == data.email))
    if existing is not None:
        raise ProfessionalAlreadyExistsError()

    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=UserRole.barber,
    )
    db.add(user)
    db.flush()

    professional = Professional(
        user_id=user.id,
        specialty=data.specialty,
        active=data.active,
    )
    db.add(professional)
    db.commit()
    db.refresh(professional)
    professional = db.scalar(
        select(Professional).options(joinedload(Professional.user)).where(Professional.id == professional.id)
    )
    return _to_out(professional)


def update_professional(db: Session, professional_id: int, data: ProfessionalUpdate) -> dict:
    professional = db.scalar(
        select(Professional).options(joinedload(Professional.user)).where(Professional.id == professional_id)
    )
    if professional is None:
        raise ProfessionalNotFoundError()

    if data.specialty is not None:
        professional.specialty = data.specialty
    if data.active is not None:
        professional.active = data.active

    db.commit()
    db.refresh(professional)
    return _to_out(professional)
