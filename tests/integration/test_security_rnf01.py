import unittest

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import select  # noqa: E402

from app.db.session import SessionLocal  # noqa: E402
from app.main import app  # noqa: E402
from app.models.user import User  # noqa: E402
from tests.integration.conftest import clean_integration_db  # noqa: E402


class SecurityRNF01Tests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        with SessionLocal() as db:
            clean_integration_db(db)

    def test_post_appointments_without_token_returns_standard_401(self):
        response = self.client.post(
            "/api/appointments",
            json={
                "professional_id": 1,
                "service_id": 1,
                "scheduled_at": "2026-06-01T14:00:00",
            },
        )

        self.assertEqual(401, response.status_code)
        self.assertEqual({"detail": "Not authenticated"}, response.json())

    def test_post_appointments_with_malformed_bearer_token_returns_401(self):
        response = self.client.post(
            "/api/appointments",
            headers={"Authorization": "Bearer xxx"},
            json={
                "professional_id": 1,
                "service_id": 1,
                "scheduled_at": "2026-06-01T14:00:00",
            },
        )

        self.assertEqual(401, response.status_code)
        self.assertIn("token", response.json()["detail"].lower())

    def test_register_stores_bcrypt_hash_instead_of_plain_password(self):
        response = self.client.post(
            "/api/auth/register",
            json={
                "name": "Cliente Seguro",
                "email": "seguro@test.com",
                "password": "senha12345",
                "role": "client",
            },
        )

        self.assertEqual(201, response.status_code)
        with SessionLocal() as db:
            user = db.scalar(select(User).where(User.email == "seguro@test.com"))

        self.assertIsNotNone(user)
        self.assertNotEqual("senha12345", user.password)
        self.assertTrue(user.password.startswith("$2b$"))

    def test_register_rejects_non_client_role(self):
        response = self.client.post(
            "/api/auth/register",
            json={
                "name": "Barbeiro Publico",
                "email": "barbeiro.publico@test.com",
                "password": "senha12345",
                "role": "barber",
            },
        )

        self.assertEqual(403, response.status_code)
        self.assertIn("clientes", response.json()["detail"].lower())


if __name__ == "__main__":
    unittest.main()
