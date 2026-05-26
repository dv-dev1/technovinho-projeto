import os
import sys
import tempfile
import unittest
from datetime import datetime, time, timedelta, timezone
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


class Sprint2QaMatrixIntegrationTests(unittest.TestCase):
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
        self.target_day = (datetime.now(timezone.utc) + timedelta(days=8)).date()
        with SessionLocal() as db:
            for model in (Appointment, Availability, Professional, Service, User):
                db.execute(delete(model))
            db.commit()

            admin = User(
                name="Admin Sprint 2",
                email="admin.sprint2@test.com",
                password=hash_password("senha12345"),
                role=UserRole.admin,
            )
            client = User(
                name="Cliente Sprint 2",
                email="client.sprint2@test.com",
                password=hash_password("senha12345"),
                role=UserRole.client,
            )
            barber = User(
                name="Barbeiro Sprint 2",
                email="barber.sprint2@test.com",
                password=hash_password("senha12345"),
                role=UserRole.barber,
            )
            service = Service(
                name="Corte QA",
                description="Servico base QA",
                duration=45,
                price=40,
                active=True,
            )
            inactive_service = Service(
                name="Servico inativo QA",
                description=None,
                duration=30,
                price=20,
                active=False,
            )
            db.add_all([admin, client, barber, service, inactive_service])
            db.commit()
            db.refresh(barber)
            db.refresh(service)
            db.refresh(inactive_service)

            professional = Professional(user_id=barber.id, specialty="Cortes QA", active=True)
            inactive_professional = Professional(user_id=barber.id, specialty="Inativo QA", active=False)
            db.add(professional)
            db.flush()
            inactive_professional.user_id = barber.id + 999
            inactive_barber = User(
                id=inactive_professional.user_id,
                name="Barbeiro Inativo QA",
                email="barber-inativo.sprint2@test.com",
                password=hash_password("senha12345"),
                role=UserRole.barber,
            )
            db.add(inactive_barber)
            db.add(inactive_professional)
            db.commit()
            db.refresh(professional)
            db.refresh(inactive_professional)

            self.service_id = service.id
            self.inactive_service_id = inactive_service.id
            self.professional_id = professional.id
            self.inactive_professional_id = inactive_professional.id

    def _token(self, email: str) -> str:
        response = self.client.post(
            "/api/auth/login",
            json={"email": email, "password": "senha12345"},
        )
        self.assertEqual(200, response.status_code)
        return response.json()["access_token"]

    def _admin_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token('admin.sprint2@test.com')}"}

    def _client_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token('client.sprint2@test.com')}"}

    def _appointment_payload(self, *, professional_id: int | None = None, service_id: int | None = None):
        return {
            "professional_id": professional_id or self.professional_id,
            "service_id": service_id or self.service_id,
            "scheduled_at": datetime.combine(self.target_day, time(10, 0)).isoformat(),
            "notes": "Teste Sprint 2",
        }

    def _create_availability(self, start="09:00:00", end="18:00:00"):
        return self.client.post(
            f"/api/professionals/{self.professional_id}/availability",
            headers=self._admin_headers(),
            json={
                "day_of_week": self.target_day.weekday(),
                "start_time": start,
                "end_time": end,
            },
        )

    def test_services_crud_and_permissions(self):
        listed = self.client.get("/api/services")
        created = self.client.post(
            "/api/services",
            headers=self._admin_headers(),
            json={
                "name": "Barba QA",
                "description": "Barba completa",
                "duration": 30,
                "price": "25.00",
                "active": True,
            },
        )
        unauthenticated = self.client.post(
            "/api/services",
            json={"name": "Sem token", "duration": 30, "price": "10.00"},
        )
        forbidden = self.client.post(
            "/api/services",
            headers=self._client_headers(),
            json={"name": "Cliente tentando criar", "duration": 30, "price": "10.00"},
        )
        invalid = self.client.post(
            "/api/services",
            headers=self._admin_headers(),
            json={"name": "Preco invalido", "duration": 30, "price": "-1.00"},
        )
        updated = self.client.patch(
            f"/api/services/{created.json()['id']}",
            headers=self._admin_headers(),
            json={"price": "35.00", "active": False},
        )
        missing = self.client.patch(
            "/api/services/999999",
            headers=self._admin_headers(),
            json={"name": "Nao existe"},
        )

        self.assertEqual(200, listed.status_code)
        self.assertEqual(201, created.status_code)
        self.assertEqual(401, unauthenticated.status_code)
        self.assertEqual(403, forbidden.status_code)
        self.assertEqual(422, invalid.status_code)
        self.assertEqual(200, updated.status_code)
        self.assertEqual("35.00", updated.json()["price"])
        self.assertFalse(updated.json()["active"])
        self.assertEqual(404, missing.status_code)

    def test_professional_list_requires_token_and_missing_professional_returns_404(self):
        without_token = self.client.get("/api/professionals")
        missing = self.client.get("/api/professionals/999999", headers=self._admin_headers())

        self.assertEqual(401, without_token.status_code)
        self.assertEqual(404, missing.status_code)

    def test_admin_updates_professional_specialty_and_active_status(self):
        updated = self.client.patch(
            f"/api/professionals/{self.professional_id}",
            headers=self._admin_headers(),
            json={"specialty": "Colorimetria QA", "active": False},
        )
        active_only = self.client.get(
            "/api/professionals?active_only=true",
            headers=self._admin_headers(),
        )

        self.assertEqual(200, updated.status_code)
        self.assertEqual("Colorimetria QA", updated.json()["specialty"])
        self.assertFalse(updated.json()["active"])
        self.assertNotIn(self.professional_id, [row["id"] for row in active_only.json()])

    def test_availability_crud_validation_and_permissions(self):
        created = self._create_availability("09:00:00", "12:00:00")
        listed = self.client.get(
            f"/api/professionals/{self.professional_id}/availability",
            headers=self._admin_headers(),
        )
        invalid_time = self.client.post(
            f"/api/professionals/{self.professional_id}/availability",
            headers=self._admin_headers(),
            json={
                "day_of_week": self.target_day.weekday(),
                "start_time": "13:00:00",
                "end_time": "12:00:00",
            },
        )
        invalid_day = self.client.post(
            f"/api/professionals/{self.professional_id}/availability",
            headers=self._admin_headers(),
            json={"day_of_week": 7, "start_time": "13:00:00", "end_time": "14:00:00"},
        )
        overlap = self.client.post(
            f"/api/professionals/{self.professional_id}/availability",
            headers=self._admin_headers(),
            json={
                "day_of_week": self.target_day.weekday(),
                "start_time": "11:00:00",
                "end_time": "13:00:00",
            },
        )
        forbidden_delete = self.client.delete(
            f"/api/availability/{created.json()['id']}",
            headers=self._client_headers(),
        )
        deleted = self.client.delete(
            f"/api/availability/{created.json()['id']}",
            headers=self._admin_headers(),
        )
        after_delete = self.client.get(
            f"/api/professionals/{self.professional_id}/availability",
            headers=self._admin_headers(),
        )

        self.assertEqual(201, created.status_code)
        self.assertEqual(200, listed.status_code)
        self.assertEqual(1, len(listed.json()))
        self.assertEqual(422, invalid_time.status_code)
        self.assertEqual(422, invalid_day.status_code)
        self.assertEqual(409, overlap.status_code)
        self.assertEqual(403, forbidden_delete.status_code)
        self.assertEqual(204, deleted.status_code)
        self.assertEqual([], after_delete.json())

    def test_appointments_reject_inactive_service_past_date_and_inactive_professional(self):
        self._create_availability()

        inactive_service = self.client.post(
            "/api/appointments",
            headers=self._client_headers(),
            json=self._appointment_payload(service_id=self.inactive_service_id),
        )
        past_date = self.client.post(
            "/api/appointments",
            headers=self._client_headers(),
            json={
                **self._appointment_payload(),
                "scheduled_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            },
        )
        inactive_professional = self.client.post(
            "/api/appointments",
            headers=self._client_headers(),
            json=self._appointment_payload(professional_id=self.inactive_professional_id),
        )

        self.assertEqual(400, inactive_service.status_code)
        self.assertIn("inativo", inactive_service.json()["detail"].lower())
        self.assertEqual(400, past_date.status_code)
        self.assertIn("futuro", past_date.json()["detail"].lower())
        self.assertEqual(400, inactive_professional.status_code)
        self.assertIn("indispon", inactive_professional.json()["detail"].lower())


if __name__ == "__main__":
    unittest.main()
