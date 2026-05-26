import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

DB_FILE = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
DB_FILE.close()
os.environ["DATABASE_URL"] = f"sqlite:///{DB_FILE.name}"
os.environ["JWT_SECRET"] = "test-secret"

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import delete  # noqa: E402

from app.core.security import hash_password  # noqa: E402
from app.db.base import Base  # noqa: E402
from app.db.session import SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models.appointment import Appointment  # noqa: E402
from app.models.availability import Availability  # noqa: E402
from app.models.professional import Professional  # noqa: E402
from app.models.service import Service  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402


class ServicesRF02IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)
        try:
            os.unlink(DB_FILE.name)
        except OSError:
            pass

    def setUp(self):
        self.client = TestClient(app)
        with SessionLocal() as db:
            for model in (Appointment, Availability, Professional, Service, User):
                db.execute(delete(model))
            db.commit()

            admin = User(
                name="Admin RF02",
                email="admin.rf02@test.com",
                password=hash_password("senha12345"),
                role=UserRole.admin,
            )
            client = User(
                name="Cliente RF02",
                email="client.rf02@test.com",
                password=hash_password("senha12345"),
                role=UserRole.client,
            )
            service = Service(
                name="Corte RF02",
                description="Servico inicial RF02",
                duration=30,
                price=45,
                active=True,
            )
            db.add_all([admin, client, service])
            db.commit()

    def _token(self, email: str) -> str:
        response = self.client.post(
            "/api/auth/login",
            json={"email": email, "password": "senha12345"},
        )
        self.assertEqual(200, response.status_code)
        return response.json()["access_token"]

    def _admin_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token('admin.rf02@test.com')}"}

    def _client_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token('client.rf02@test.com')}"}

    def test_c1_get_services_returns_200_list(self):
        response = self.client.get("/api/services")

        self.assertEqual(200, response.status_code)
        body = response.json()
        self.assertEqual(1, len(body))
        self.assertEqual("Corte RF02", body[0]["name"])

    def test_c2_admin_can_create_service(self):
        response = self.client.post(
            "/api/services",
            headers=self._admin_headers(),
            json={
                "name": "Barba RF02",
                "description": "Barba completa",
                "duration": 25,
                "price": "35.00",
                "active": True,
            },
        )

        self.assertEqual(201, response.status_code)
        body = response.json()
        self.assertEqual("Barba RF02", body["name"])
        self.assertEqual(25, body["duration"])
        self.assertEqual("35.00", body["price"])
        self.assertTrue(body["active"])

    def test_c3_create_service_without_auth_returns_401(self):
        response = self.client.post(
            "/api/services",
            json={"name": "Sem auth", "duration": 30, "price": "20.00"},
        )

        self.assertEqual(401, response.status_code)
        self.assertEqual({"detail": "Not authenticated"}, response.json())

    def test_c4_client_role_cannot_create_service(self):
        response = self.client.post(
            "/api/services",
            headers=self._client_headers(),
            json={"name": "Cliente criando", "duration": 30, "price": "20.00"},
        )

        self.assertEqual(403, response.status_code)
        self.assertIn("restrito", response.json()["detail"].lower())

    def test_c5_invalid_service_payload_returns_422(self):
        response = self.client.post(
            "/api/services",
            headers=self._admin_headers(),
            json={"name": "Preco invalido", "duration": 30, "price": "-1.00"},
        )

        self.assertEqual(422, response.status_code)

    def test_admin_can_update_service_and_toggle_active_status(self):
        listed = self.client.get("/api/services").json()
        service_id = listed[0]["id"]

        response = self.client.patch(
            f"/api/services/{service_id}",
            headers=self._admin_headers(),
            json={
                "name": "Corte RF02 Atualizado",
                "description": "Atualizado pela matriz RF02",
                "duration": 40,
                "price": "55.00",
                "active": False,
            },
        )

        self.assertEqual(200, response.status_code)
        body = response.json()
        self.assertEqual("Corte RF02 Atualizado", body["name"])
        self.assertEqual(40, body["duration"])
        self.assertEqual("55.00", body["price"])
        self.assertFalse(body["active"])

    def test_update_missing_service_returns_404(self):
        response = self.client.patch(
            "/api/services/999999",
            headers=self._admin_headers(),
            json={"name": "Nao existe"},
        )

        self.assertEqual(404, response.status_code)
        self.assertIn("nao encontrado", response.json()["detail"].lower())


if __name__ == "__main__":
    unittest.main()
