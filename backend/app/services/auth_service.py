from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.schemas.auth import LoginIn, RegisterIn


class EmailAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class SelfRegistrationRoleNotAllowedError(Exception):
    pass


def register_user(db: Session, data: RegisterIn) -> User:
    existing = db.scalar(select(User).where(User.email == data.email))
    if existing:
        raise EmailAlreadyExistsError()
    if data.role != UserRole.client:
        raise SelfRegistrationRoleNotAllowedError()

    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, data: LoginIn) -> tuple[User, str]:
    user = db.scalar(select(User).where(User.email == data.email))
    if user is None or not verify_password(data.password, user.password):
        raise InvalidCredentialsError()

    token = create_access_token(user_id=user.id, role=user.role.value)
    return user, token
