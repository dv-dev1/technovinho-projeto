from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.professional import Professional
from app.models.user import User

router = APIRouter(prefix="/api/professionals", tags=["professionals"])


@router.get("/")
def list_professionals(
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    rows = db.scalars(select(Professional)).all()
    return [
        {
            "id": p.id,
            "user_id": p.user_id,
            "specialty": p.specialty,
            "active": p.active,
        }
        for p in rows
    ]
