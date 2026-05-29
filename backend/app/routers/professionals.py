from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.availability import AvailabilityCreate, AvailabilityOut
from app.schemas.professional import ProfessionalCreate, ProfessionalOut, ProfessionalUpdate
from app.services import availability_service, professional_service

router = APIRouter(prefix="/api/professionals", tags=["professionals"])


@router.get("/", response_model=list[ProfessionalOut])
def list_professionals(
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    active_only: bool = Query(default=False),
):
    return professional_service.list_professionals(db, active_only=active_only)


@router.get("/{professional_id}", response_model=ProfessionalOut)
def get_professional(
    professional_id: int,
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return professional_service.get_professional(db, professional_id)
    except professional_service.ProfessionalNotFoundError:
        raise HTTPException(status_code=404, detail="Profissional nao encontrado") from None


@router.post("/", response_model=ProfessionalOut, status_code=status.HTTP_201_CREATED)
def create_professional(
    data: ProfessionalCreate,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return professional_service.create_professional(db, data)
    except professional_service.ProfessionalAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Email ja cadastrado") from None


@router.patch("/{professional_id}", response_model=ProfessionalOut)
def update_professional(
    professional_id: int,
    data: ProfessionalUpdate,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return professional_service.update_professional(db, professional_id, data)
    except professional_service.ProfessionalNotFoundError:
        raise HTTPException(status_code=404, detail="Profissional nao encontrado") from None


@router.get("/{professional_id}/availability", response_model=list[AvailabilityOut])
def list_professional_availability(
    professional_id: int,
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return availability_service.list_for_professional(db, professional_id)
    except availability_service.ProfessionalNotFoundError:
        raise HTTPException(status_code=404, detail="Profissional nao encontrado") from None


@router.post(
    "/{professional_id}/availability",
    response_model=AvailabilityOut,
    status_code=status.HTTP_201_CREATED,
)
def create_professional_availability(
    professional_id: int,
    data: AvailabilityCreate,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return availability_service.create_slot(db, professional_id, data)
    except availability_service.ProfessionalNotFoundError:
        raise HTTPException(status_code=404, detail="Profissional nao encontrado") from None
    except availability_service.InvalidTimeRangeError:
        raise HTTPException(status_code=400, detail="end_time deve ser maior que start_time") from None
    except availability_service.AvailabilityOverlapError:
        raise HTTPException(status_code=409, detail="Faixa sobrepoe outra no mesmo dia") from None
