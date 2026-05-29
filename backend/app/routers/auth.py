from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginIn, RegisterIn, TokenOut, UserOut
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: RegisterIn, db: Annotated[Session, Depends(get_db)]):
    try:
        user = auth_service.register_user(db, data)
    except auth_service.EmailAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email ja cadastrado") from None
    except auth_service.SelfRegistrationRoleNotAllowedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cadastro publico disponivel apenas para clientes",
        ) from None
    return user


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Annotated[Session, Depends(get_db)]):
    try:
        _, token = auth_service.authenticate_user(db, data)
    except auth_service.InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha invalidos",
        ) from None
    return TokenOut(access_token=token)


@router.get("/me", response_model=UserOut)
def me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
