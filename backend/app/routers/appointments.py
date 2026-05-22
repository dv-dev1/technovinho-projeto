from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.appointment import Appointment
from app.models.user import User

router = APIRouter(prefix="/api/appointments", tags=["appointments"])


@router.get("/")
def list_appointments(
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    rows = db.scalars(select(Appointment)).all()
    return [
        {
            "id": a.id,
            "client_id": a.client_id,
            "professional_id": a.professional_id,
            "service_id": a.service_id,
            "scheduled_at": a.scheduled_at.isoformat(),
            "status": a.status.value if hasattr(a.status, "value") else a.status,
            "notes": a.notes,
        }
        for a in rows
    ]
