import os
import sys
import tempfile
import unittest
from datetime import datetime, time, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(ROOT))

DB_FILE = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
DB_FILE.close()
os.environ["DATABASE_URL"] = f"sqlite:///{DB_FILE.name}"
os.environ["JWT_SECRET"] = "test-secret"

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import delete, select  # noqa: E402

from app.core.security import hash_password  # noqa: E402
from app.db.base import Base  # noqa: E402
from app.db.session import SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models.appointment import Appointment, AppointmentStatus  # noqa: E402
from app.models.availability import Availability  # noqa: E402
from app.models.professional import Professional  # noqa: E402
from app.models.service import Service  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402
from frontend.lib import dashboard  # noqa: E402


class Sprint3E2ETests(unittest.TestCase):
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
        self.today_slot = datetime.now(timezone.utc) + timedelta(hours=2)
        self.future_slot = datetime.now(timezone.utc) + timedelta(days=3)
        with SessionLocal() as db:
            for model in (Appointment, Availability, Professional, Service, User):
                db.execute(delete(model))
            db.commit()

            client_user = User(
                name="Cliente E2E",
                email="cliente.e2e@test.com",
                password=hash_password("senha12345"),
                role=UserRole.client,
            )
            admin_user = User(
                name="Admin E2E",
                email="admin.e2e@test.com",
                password=hash_password("senha12345"),
                role=UserRole.admin,
            )
            barber_user = User(
                name="Barbeiro E2E",
                email="barbeiro.e2e@test.com",
                password=hash_password("senha12345"),
                role=UserRole.barber,
            )
            service = Service(
                name="Corte E2E",
                description="Servico usado nos cenarios E2E da Sprint 3",
                duration=30,
                price=50,
                active=True,
            )
            db.add_all([client_user, admin_user, barber_user, service])
            db.commit()
            db.refresh(client_user)
            db.refresh(barber_user)
            db.refresh(service)

            professional = Professional(user_id=barber_user.id, specialty="Cortes", active=True)
            db.add(professional)
            db.commit()
            db.refresh(professional)

            for day in {self.today_slot.weekday(), self.future_slot.weekday()}:
                db.add(
                    Availability(
                        professional_id=professional.id,
                        day_of_week=day,
                        start_time=time(0, 0),
                        end_time=time(23, 59),
                    )
                )
            db.commit()

            self.client_user_id = client_user.id
            self.service_id = service.id
            self.professional_id = professional.id

    def _token(self, email: str) -> str:
        response = self.client.post(
            "/api/auth/login",
            json={"email": email, "password": "senha12345"},
        )
        self.assertEqual(200, response.status_code)
        return response.json()["access_token"]

    def _client_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token('cliente.e2e@test.com')}"}

    def _admin_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token('admin.e2e@test.com')}"}

    def _appointment_payload(self, scheduled_at: datetime) -> dict:
        return {
            "professional_id": self.professional_id,
            "service_id": self.service_id,
            "scheduled_at": scheduled_at.isoformat(),
            "notes": "Fluxo E2E Sprint 3",
        }

    def _create_appointment(self, scheduled_at: datetime):
        response = self.client.post(
            "/api/appointments",
            headers=self._client_headers(),
            json=self._appointment_payload(scheduled_at),
        )
        self.assertEqual(201, response.status_code)
        return response.json()

    def _insert_past_appointment(self) -> int:
        with SessionLocal() as db:
            row = Appointment(
                client_id=self.client_user_id,
                professional_id=self.professional_id,
                service_id=self.service_id,
                scheduled_at=datetime.now(timezone.utc) - timedelta(hours=2),
                status=AppointmentStatus.confirmed,
                notes="Atendimento para historico",
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return row.id

    def test_admin_dashboard_shows_today_metrics(self):
        created = self._create_appointment(self.today_slot)

        appointments = self.client.get("/api/appointments", headers=self._admin_headers()).json()
        services = self.client.get("/api/services", headers=self._admin_headers()).json()
        professionals = self.client.get("/api/professionals", headers=self._admin_headers()).json()

        today_rows = dashboard.today_appointments(appointments, today=self.today_slot.date())

        self.assertEqual([created["id"]], [row["id"] for row in today_rows])
        self.assertEqual(50.0, dashboard.estimated_revenue(today_rows, services))
        self.assertEqual(1, dashboard.active_professionals_count(professionals))
        self.assertEqual("Cliente E2E", dashboard.dashboard_rows(today_rows)[0]["Cliente"])

    def test_client_booking_appears_in_admin_dashboard_source_data(self):
        created = self._create_appointment(self.today_slot)

        admin_rows = self.client.get("/api/appointments", headers=self._admin_headers())
        today_rows = dashboard.today_appointments(admin_rows.json(), today=self.today_slot.date())

        self.assertEqual(200, admin_rows.status_code)
        self.assertIn(created["id"], [row["id"] for row in today_rows])

    def test_client_cancels_own_appointment_before_deadline(self):
        created = self._create_appointment(self.future_slot)

        cancelled = self.client.patch(
            f"/api/appointments/{created['id']}/cancel",
            headers=self._client_headers(),
        )

        self.assertEqual(200, cancelled.status_code)
        self.assertEqual("cancelled", cancelled.json()["status"])

    def test_cancellation_after_deadline_is_rejected(self):
        created = self._create_appointment(self.today_slot)

        response = self.client.patch(
            f"/api/appointments/{created['id']}/cancel",
            headers=self._client_headers(),
        )

        self.assertEqual(400, response.status_code)
        self.assertIn("24h", response.json()["detail"])

    def test_history_lists_only_done_appointments_for_client(self):
        appointment_id = self._insert_past_appointment()

        completed = self.client.patch(
            f"/api/appointments/{appointment_id}/complete",
            headers=self._admin_headers(),
        )
        history = self.client.get(
            "/api/appointments",
            params={"status": "done", "mine": "true"},
            headers=self._client_headers(),
        )

        self.assertEqual(200, completed.status_code)
        self.assertEqual("done", completed.json()["status"])
        self.assertEqual([appointment_id], [row["id"] for row in history.json()])
        self.assertEqual("Corte E2E", history.json()[0]["service_name"])


if __name__ == "__main__":
    unittest.main()
