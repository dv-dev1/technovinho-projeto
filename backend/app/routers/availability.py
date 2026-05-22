from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.availability import Availability
from app.models.user import User

router = APIRouter(prefix="/api/availability", tags=["availability"])


@router.get("/")
def list_availability(
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    rows = db.scalars(select(Availability)).all()
    return [
        {
            "id": r.id,
            "professional_id": r.professional_id,
            "day_of_week": r.day_of_week,
            "start_time": r.start_time.isoformat(),
            "end_time": r.end_time.isoformat(),
        }
        for r in rows
    ]
