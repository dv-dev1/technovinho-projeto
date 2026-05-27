import unittest

from fastapi.testclient import TestClient  # noqa: E402

from app.core.security import hash_password  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.main import app  # noqa: E402
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
            barber = User(
                name="Barbeiro APS",
                email="barber.rf03@test.com",
                password=hash_password("senha12345"),
                role=UserRole.barber,
            )
            barber_two = User(
                name="Barbeiro Inativo",
                email="barber2.rf03@test.com",
                password=hash_password("senha12345"),
                role=UserRole.barber,
            )
            client = User(
                name="Cliente APS",
                email="client.rf03@test.com",
                password=hash_password("senha12345"),
                role=UserRole.client,
            )
            db.add_all([admin, barber, barber_two, client])
            db.commit()

            db.refresh(admin)
            db.refresh(barber)
            db.refresh(barber_two)
            db.refresh(client)

            self.admin_user_id = admin.id
            self.barber_user_id = barber.id
            self.barber_two_user_id = barber_two.id
            self.client_user_id = client.id

    def _admin_token(self):
        response = self.client.post(
            "/api/auth/login",
            json={"email": "admin.rf03@test.com", "password": "senha12345"},
        )
        self.assertEqual(200, response.status_code)
        return response.json()["access_token"]

    def test_admin_can_create_professional_with_barber_user(self):
        response = self.client.post(
            "/api/professionals",
            headers={"Authorization": f"Bearer {self._admin_token()}"},
            json={"user_id": self.barber_user_id, "specialty": "Degrade", "active": True},
        )

        self.assertEqual(201, response.status_code)
        body = response.json()
        self.assertEqual(self.barber_user_id, body["user_id"])
        self.assertEqual("Barbeiro APS", body["name"])
        self.assertEqual("Degrade", body["specialty"])
        self.assertTrue(body["active"])

    def test_duplicate_user_id_returns_conflict(self):
        headers = {"Authorization": f"Bearer {self._admin_token()}"}
        first = self.client.post(
            "/api/professionals",
            headers=headers,
            json={"user_id": self.barber_user_id, "specialty": "Corte", "active": True},
        )
        second = self.client.post(
            "/api/professionals",
            headers=headers,
            json={"user_id": self.barber_user_id, "specialty": "Barba", "active": True},
        )

        self.assertEqual(201, first.status_code)
        self.assertEqual(409, second.status_code)
        self.assertIn("existe", second.json()["detail"].lower())

    def test_non_barber_user_is_rejected(self):
        response = self.client.post(
            "/api/professionals",
            headers={"Authorization": f"Bearer {self._admin_token()}"},
            json={"user_id": self.client_user_id, "specialty": "Nao deve criar", "active": True},
        )

        self.assertEqual(400, response.status_code)
        self.assertIn("barber", response.json()["detail"].lower())

    def test_inactive_professional_is_hidden_from_active_only_listing(self):
        headers = {"Authorization": f"Bearer {self._admin_token()}"}
        created_active = self.client.post(
            "/api/professionals",
            headers=headers,
            json={"user_id": self.barber_user_id, "specialty": "Corte", "active": True},
        )
        created_inactive = self.client.post(
            "/api/professionals",
            headers=headers,
            json={"user_id": self.barber_two_user_id, "specialty": "Barba", "active": False},
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
        self.assertEqual(self.barber_user_id, rows[0]["user_id"])
        self.assertTrue(rows[0]["active"])


if __name__ == "__main__":
    unittest.main()
