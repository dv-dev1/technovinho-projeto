from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.service import ServiceCreate, ServiceOut, ServiceUpdate
from app.services import service_service

router = APIRouter(prefix="/api/services", tags=["services"])


@router.get("/", response_model=list[ServiceOut])
def list_services(
    db: Annotated[Session, Depends(get_db)],
):
    return service_service.list_services(db)


@router.post("/", response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
def create_service(
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
    db: Annotated[Session, Depends(get_db)],
    data: ServiceCreate,
):
    return service_service.create_service(db, data)


@router.patch("/{service_id}", response_model=ServiceOut)
def update_service(
    service_id: int,
    data: ServiceUpdate,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return service_service.update_service(db, service_id, data)
    except service_service.ServiceNotFoundError:
        raise HTTPException(status_code=404, detail="Servico nao encontrado") from None
