from datetime import datetime

from pydantic import BaseModel, Field

from app.models.appointment import AppointmentStatus


class AppointmentCreate(BaseModel):
    professional_id: int
    service_id: int
    scheduled_at: datetime
    notes: str | None = None


class AppointmentOut(BaseModel):
    id: int
    client_id: int
    client_name: str | None = None
    professional_id: int
    professional_name: str | None = None
    service_id: int
    service_name: str | None = None
    scheduled_at: datetime
    status: AppointmentStatus
    notes: str | None = None
