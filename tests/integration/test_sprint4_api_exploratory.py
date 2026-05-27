import unittest
from datetime import datetime, time, timedelta, timezone

from fastapi.testclient import TestClient  # noqa: E402

from app.core.security import hash_password  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.main import app  # noqa: E402
from app.models.availability import Availability  # noqa: E402
from app.models.professional import Professional  # noqa: E402
from app.models.service import Service  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402
from tests.integration.conftest import clean_integration_db  # noqa: E402


class Sprint4ApiExploratoryTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.target_day = (datetime.now(timezone.utc) + timedelta(days=10)).date()
        with SessionLocal() as db:
            clean_integration_db(db)

            client_user = User(
                name="Cliente Exploratorio",
                email="cliente.exploratorio@test.com",
                password=hash_password("senha12345"),
                role=UserRole.client,
            )
            barber_user = User(
                name="Barbeiro Exploratorio",
                email="barbeiro.exploratorio@test.com",
                password=hash_password("senha12345"),
                role=UserRole.barber,
            )
            service = Service(
                name="Corte Exploratorio",
                description="Servico usado nos 5 testes exploratorios de API",
                duration=30,
                price=45,
                active=True,
            )
            db.add_all([client_user, barber_user, service])
            db.commit()
            db.refresh(barber_user)
            db.refresh(service)

            professional = Professional(
                user_id=barber_user.id,
                specialty="Corte",
                active=True,
            )
            db.add(professional)
            db.commit()
            db.refresh(professional)

            db.add(
                Availability(
                    professional_id=professional.id,
                    day_of_week=self.target_day.weekday(),
                    start_time=time(9, 0),
                    end_time=time(18, 0),
                )
            )
            db.commit()

            self.service_id = service.id
            self.professional_id = professional.id

    def _client_token(self) -> str:
        response = self.client.post(
            "/api/auth/login",
            json={"email": "cliente.exploratorio@test.com", "password": "senha12345"},
        )
        self.assertEqual(200, response.status_code)
        return response.json()["access_token"]

    def _appointment_payload(self):
        return {
            "professional_id": self.professional_id,
            "service_id": self.service_id,
            "scheduled_at": datetime.combine(self.target_day, time(10, 0)).isoformat(),
            "notes": "Teste exploratorio Sprint 4",
        }

    def test_01_register_valid_user_returns_201_without_password(self):
        response = self.client.post(
            "/api/auth/register",
            json={
                "name": "Usuario Exploratorio",
                "email": "usuario.exploratorio@test.com",
                "password": "senha12345",
                "role": "client",
            },
        )

        self.assertEqual(201, response.status_code)
        body = response.json()
        self.assertEqual("Usuario Exploratorio", body["name"])
        self.assertEqual("usuario.exploratorio@test.com", body["email"])
        self.assertNotIn("password", body)

    def test_02_login_valid_credentials_returns_bearer_token(self):
        response = self.client.post(
            "/api/auth/login",
            json={"email": "cliente.exploratorio@test.com", "password": "senha12345"},
        )

        self.assertEqual(200, response.status_code)
        body = response.json()
        self.assertEqual("bearer", body["token_type"])
        self.assertTrue(body["access_token"])

    def test_03_get_services_without_authorization_returns_200_list(self):
        response = self.client.get("/api/services")

        self.assertEqual(200, response.status_code)
        services = response.json()
        self.assertGreaterEqual(len(services), 1)
        self.assertEqual("Corte Exploratorio", services[0]["name"])

    def test_04_post_appointment_with_valid_bearer_returns_201(self):
        response = self.client.post(
            "/api/appointments",
            headers={"Authorization": f"Bearer {self._client_token()}"},
            json=self._appointment_payload(),
        )

        self.assertEqual(201, response.status_code)
        body = response.json()
        self.assertEqual("pending", body["status"])
        self.assertEqual("Corte Exploratorio", body["service_name"])
        self.assertEqual("Barbeiro Exploratorio", body["professional_name"])

    def test_05_post_appointment_with_invalid_bearer_returns_401(self):
        response = self.client.post(
            "/api/appointments",
            headers={"Authorization": "Bearer token_invalido"},
            json=self._appointment_payload(),
        )

        self.assertEqual(401, response.status_code)
        self.assertIn("token", response.json()["detail"].lower())


if __name__ == "__main__":
    unittest.main()
