from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.service import Service
from app.models.user import User, UserRole

router = APIRouter(prefix="/api/services", tags=["services"])


@router.get("/")
def list_services(
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    services = db.scalars(select(Service)).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "description": s.description,
            "duration": s.duration,
            "price": float(s.price),
            "active": s.active,
        }
        for s in services
    ]


@router.post("/", status_code=201)
def create_service(
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
    db: Annotated[Session, Depends(get_db)],
    body: dict,
):
    service = Service(
        name=body["name"],
        description=body.get("description"),
        duration=body["duration"],
        price=body["price"],
        active=body.get("active", True),
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return {
        "id": service.id,
        "name": service.name,
        "description": service.description,
        "duration": service.duration,
        "price": float(service.price),
        "active": service.active,
    }
