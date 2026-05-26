from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate


class ServiceNotFoundError(Exception):
    pass


def list_services(db: Session) -> list[Service]:
    return list(db.scalars(select(Service).order_by(Service.name)).all())


def create_service(db: Session, data: ServiceCreate) -> Service:
    service = Service(**data.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def update_service(db: Session, service_id: int, data: ServiceUpdate) -> Service:
    service = db.get(Service, service_id)
    if service is None:
        raise ServiceNotFoundError()

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(service, field, value)
    db.commit()
    db.refresh(service)
    return service
