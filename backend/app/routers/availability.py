from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.availability import AvailabilityOut
from app.services import availability_service

router = APIRouter(prefix="/api/availability", tags=["availability"])


@router.get("/", response_model=list[AvailabilityOut])
def list_all_availability(
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return availability_service.list_all(db)


@router.delete("/{availability_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_availability(
    availability_id: int,
    _: Annotated[User, Depends(require_roles(UserRole.admin))],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        availability_service.delete_slot(db, availability_id)
    except availability_service.AvailabilityNotFoundError:
        raise HTTPException(status_code=404, detail="Disponibilidade não encontrada") from None
