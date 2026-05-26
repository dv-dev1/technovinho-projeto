import re
from typing import Any

import streamlit as st

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
AUTH_SESSION_KEYS = (
    "token",
    "user_role",
    "user_id",
    "user_name",
    "user",
    "appointment_confirmation",
    "last_booking",
)


def ensure_session_defaults(st_module=st) -> None:
    st_module.session_state.setdefault("token", None)
    st_module.session_state.setdefault("user_role", None)
    st_module.session_state.setdefault("user_id", None)
    st_module.session_state.setdefault("user_name", None)
    st_module.session_state.setdefault("user", None)


def validate_register_form(
    *,
    name: str,
    email: str,
    password: str,
    confirm_password: str,
) -> list[str]:
    errors = []
    if len(name.strip()) < 2:
        errors.append("Informe um nome com pelo menos 2 caracteres.")
    if not EMAIL_RE.match(email.strip()):
        errors.append("Informe um email valido.")
    if len(password) < 8:
        errors.append("A senha deve ter pelo menos 8 caracteres.")
    if password != confirm_password:
        errors.append("As senhas devem ser iguais.")
    return errors


def set_authenticated_session(token: str, user: dict[str, Any], *, st_module=st) -> None:
    st_module.session_state["token"] = token
    st_module.session_state["user_role"] = user.get("role")
    st_module.session_state["user_id"] = user.get("id")
    st_module.session_state["user_name"] = user.get("name")
    st_module.session_state["user"] = user


def logout(*, st_module=st) -> None:
    for key in AUTH_SESSION_KEYS:
        st_module.session_state.pop(key, None)


def current_role(st_module=st) -> str | None:
    role = st_module.session_state.get("user_role")
    if role:
        return role
    user = st_module.session_state.get("user") or {}
    return user.get("role")
