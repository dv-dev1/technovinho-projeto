from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.appointment import AppointmentStatus
from app.models.user import User
from app.schemas.appointment import AppointmentCreate, AppointmentOut
from app.services import appointment_service

router = APIRouter(prefix="/api/appointments", tags=["appointments"])


@router.get("/", response_model=list[AppointmentOut])
def list_appointments(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    status: AppointmentStatus | None = Query(default=None),
    mine: bool = Query(default=False),
):
    return appointment_service.list_appointments(
        db, current_user=current_user, status=status, mine=mine
    )


@router.post("/", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(
    data: AppointmentCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return appointment_service.create_appointment(db, current_user=current_user, data=data)
    except appointment_service.ServiceNotFoundError:
        raise HTTPException(status_code=404, detail="Serviço não encontrado") from None
    except appointment_service.ServiceUnavailableError:
        raise HTTPException(status_code=400, detail="Servico inativo para agendamento") from None
    except appointment_service.ProfessionalUnavailableError:
        raise HTTPException(status_code=400, detail="Profissional indisponivel para agendamento") from None
    except appointment_service.SlotUnavailableError:
        raise HTTPException(status_code=400, detail="Horário indisponível para o profissional") from None
    except appointment_service.AppointmentConflictError:
        raise HTTPException(status_code=409, detail="Horario ja reservado para o profissional") from None
    except appointment_service.InvalidAppointmentStateError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from None
    except appointment_service.AppointmentForbiddenError:
        raise HTTPException(status_code=403, detail="Sem permissão para criar agendamento") from None


@router.patch("/{appointment_id}/cancel", response_model=AppointmentOut)
def cancel_appointment(
    appointment_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return appointment_service.cancel_appointment(
            db, appointment_id=appointment_id, current_user=current_user
        )
    except appointment_service.AppointmentNotFoundError:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado") from None
    except appointment_service.AppointmentForbiddenError:
        raise HTTPException(status_code=403, detail="Sem permissão para cancelar") from None
    except appointment_service.CancelDeadlineError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from None
    except appointment_service.InvalidAppointmentStateError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from None
