import os

import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class ApiError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def _headers(token: str | None) -> dict:
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def _request(method: str, path: str, *, token: str | None = None, **kwargs):
    url = f"{API_BASE_URL.rstrip('/')}{path}"
    try:
        response = requests.request(method, url, headers=_headers(token), timeout=15, **kwargs)
    except requests.exceptions.ConnectionError as exc:
        raise ApiError(0, f"API offline em {API_BASE_URL}") from exc

    if response.status_code >= 400:
        detail = response.text
        try:
            detail = response.json().get("detail", detail)
        except Exception:
            pass
        if isinstance(detail, list):
            detail = str(detail)
        raise ApiError(response.status_code, str(detail))
    if response.status_code == 204:
        return None
    if not response.content:
        return None
    return response.json()


def login(email: str, password: str) -> dict:
    return _request("POST", "/api/auth/login", json={"email": email, "password": password})


def me(token: str) -> dict:
    return _request("GET", "/api/auth/me", token=token)


def list_professionals(token: str) -> list:
    return _request("GET", "/api/professionals", token=token) or []


def create_professional(token: str, payload: dict) -> dict:
    return _request("POST", "/api/professionals", token=token, json=payload)


def list_availability(token: str, professional_id: int) -> list:
    return _request("GET", f"/api/professionals/{professional_id}/availability", token=token) or []


def create_availability(token: str, professional_id: int, payload: dict) -> dict:
    return _request("POST", f"/api/professionals/{professional_id}/availability", token=token, json=payload)


def delete_availability(token: str, availability_id: int) -> None:
    _request("DELETE", f"/api/availability/{availability_id}", token=token)
