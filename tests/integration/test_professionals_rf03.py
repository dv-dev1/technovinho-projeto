import unittest

from fastapi.testclient import TestClient  # noqa: E402

from app.core.security import hash_password  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.main import app  # noqa: E402
from app.models.professional import Professional  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402
from tests.integration.conftest import clean_integration_db  # noqa: E402


class ProfessionalsRf03IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        with SessionLocal() as db:
            clean_integration_db(db)

            admin = User(
                name="Admin APS",
                email="admin.rf03@test.com",
                password=hash_password("senha12345"),
                role=UserRole.admin,
            )
            client = User(
                name="Cliente APS",
                email="client.rf03@test.com",
                password=hash_password("senha12345"),
                role=UserRole.client,
            )
            db.add_all([admin, client])
            db.commit()

            db.refresh(admin)
            db.refresh(client)

            self.admin_user_id = admin.id
            self.client_user_id = client.id

    def _admin_token(self):
        response = self.client.post(
            "/api/auth/login",
            json={"email": "admin.rf03@test.com", "password": "senha12345"},
        )
        self.assertEqual(200, response.status_code)
        return response.json()["access_token"]

    def _client_token(self):
        response = self.client.post(
            "/api/auth/login",
            json={"email": "client.rf03@test.com", "password": "senha12345"},
        )
        self.assertEqual(200, response.status_code)
        return response.json()["access_token"]

    def test_admin_can_create_professional_with_barber_credentials(self):
        response = self.client.post(
            "/api/professionals",
            headers={"Authorization": f"Bearer {self._admin_token()}"},
            json={
                "name": "Barbeiro APS",
                "email": "barber.rf03@test.com",
                "password": "senha12345",
                "specialty": "Degrade",
                "active": True,
            },
        )

        self.assertEqual(201, response.status_code)
        body = response.json()
        self.assertEqual("Barbeiro APS", body["name"])
        self.assertEqual("barber.rf03@test.com", body["email"])
        self.assertEqual("Degrade", body["specialty"])
        self.assertTrue(body["active"])

        with SessionLocal() as db:
            barber_user = db.query(User).filter(User.email == "barber.rf03@test.com").one()
            professional = db.query(Professional).filter(Professional.user_id == barber_user.id).one()

        self.assertEqual(UserRole.barber, barber_user.role)
        self.assertEqual("Degrade", professional.specialty)

        login = self.client.post(
            "/api/auth/login",
            json={"email": "barber.rf03@test.com", "password": "senha12345"},
        )
        self.assertEqual(200, login.status_code)
        me = self.client.get("/api/auth/me", headers={"Authorization": f"Bearer {login.json()['access_token']}"})
        self.assertEqual("barber", me.json()["role"])

    def test_duplicate_email_returns_conflict(self):
        headers = {"Authorization": f"Bearer {self._admin_token()}"}
        first = self.client.post(
            "/api/professionals",
            headers=headers,
            json={
                "name": "Barbeiro APS",
                "email": "barber.rf03@test.com",
                "password": "senha12345",
                "specialty": "Corte",
                "active": True,
            },
        )
        second = self.client.post(
            "/api/professionals",
            headers=headers,
            json={
                "name": "Outro Nome",
                "email": "barber.rf03@test.com",
                "password": "senha12345",
                "specialty": "Barba",
                "active": True,
            },
        )

        self.assertEqual(201, first.status_code)
        self.assertEqual(409, second.status_code)
        self.assertIn("email", second.json()["detail"].lower())

    def test_invalid_payload_returns_422(self):
        response = self.client.post(
            "/api/professionals",
            headers={"Authorization": f"Bearer {self._admin_token()}"},
            json={
                "name": "A",
                "email": "email-invalido",
                "password": "123",
                "specialty": "Nao deve criar",
                "active": True,
            },
        )

        self.assertEqual(422, response.status_code)

    def test_client_role_cannot_create_professional(self):
        response = self.client.post(
            "/api/professionals",
            headers={"Authorization": f"Bearer {self._client_token()}"},
            json={
                "name": "Barbeiro Bloqueado",
                "email": "barber.bloqueado.rf03@test.com",
                "password": "senha12345",
                "specialty": "Corte",
                "active": True,
            },
        )

        self.assertEqual(403, response.status_code)

    def test_inactive_professional_is_hidden_from_active_only_listing(self):
        headers = {"Authorization": f"Bearer {self._admin_token()}"}
        created_active = self.client.post(
            "/api/professionals",
            headers=headers,
            json={
                "name": "Barbeiro Ativo",
                "email": "barber.ativo.rf03@test.com",
                "password": "senha12345",
                "specialty": "Corte",
                "active": True,
            },
        )
        created_inactive = self.client.post(
            "/api/professionals",
            headers=headers,
            json={
                "name": "Barbeiro Inativo",
                "email": "barber.inativo.rf03@test.com",
                "password": "senha12345",
                "specialty": "Barba",
                "active": False,
            },
        )
        self.assertEqual(201, created_active.status_code)
        self.assertEqual(201, created_inactive.status_code)

        response = self.client.get(
            "/api/professionals?active_only=true",
            headers={"Authorization": f"Bearer {self._admin_token()}"},
        )

        self.assertEqual(200, response.status_code)
        rows = response.json()
        self.assertEqual(1, len(rows))
        self.assertEqual("barber.ativo.rf03@test.com", rows[0]["email"])
        self.assertTrue(rows[0]["active"])


if __name__ == "__main__":
    unittest.main()
