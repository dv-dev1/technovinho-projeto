import unittest
from datetime import datetime, time, timedelta, timezone

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import select  # noqa: E402

from app.core.security import hash_password  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.main import app  # noqa: E402
from app.models.appointment import Appointment, AppointmentStatus  # noqa: E402
from app.models.availability import Availability  # noqa: E402
from app.models.professional import Professional  # noqa: E402
from app.models.service import Service  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402
from tests.integration.conftest import clean_integration_db  # noqa: E402


class AppointmentFlowIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.target_day = (datetime.now(timezone.utc) + timedelta(days=7)).date()
        with SessionLocal() as db:
            clean_integration_db(db)
            client_user = User(
                name="Cliente Teste",
                email="cliente@test.com",
                password=hash_password("senha12345"),
                role=UserRole.client,
            )
            admin_user = User(
                name="Admin Teste",
                email="admin@test.com",
                password=hash_password("senha12345"),
                role=UserRole.admin,
            )
            barber_user = User(
                name="Barbeiro Teste",
                email="barbeiro@test.com",
                password=hash_password("senha12345"),
                role=UserRole.barber,
            )
            service = Service(
                name="Corte masculino",
                description="Corte tradicional",
                duration=45,
                price=35,
                active=True,
            )
            db.add_all([client_user, admin_user, barber_user, service])
            db.commit()
            db.refresh(barber_user)
            db.refresh(service)

            professional = Professional(user_id=barber_user.id, specialty="Cortes", active=True)
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

    def _login_token(self):
        login_response = self.client.post(
            "/api/auth/login",
            json={"email": "cliente@test.com", "password": "senha12345"},
        )
        self.assertEqual(200, login_response.status_code)
        return login_response.json()["access_token"]

    def _admin_token(self):
        response = self.client.post(
            "/api/auth/login",
            json={"email": "admin@test.com", "password": "senha12345"},
        )
        self.assertEqual(200, response.status_code)
        return response.json()["access_token"]

    def _appointment_payload(self, scheduled_time=time(14, 0)):
        return {
            "professional_id": self.professional_id,
            "service_id": self.service_id,
            "scheduled_at": datetime.combine(self.target_day, scheduled_time).isoformat(),
            "notes": "Preferencia por maquina 2",
        }

    def _insert_past_appointment(self):
        with SessionLocal() as db:
            client = db.scalar(select(User).where(User.email == "cliente@test.com"))
            row = Appointment(
                client_id=client.id,
                professional_id=self.professional_id,
                service_id=self.service_id,
                scheduled_at=datetime.now(timezone.utc) - timedelta(hours=1),
                status=AppointmentStatus.confirmed,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return row.id

    def test_client_can_create_appointment_and_row_is_persisted(self):
        token = self._login_token()
        create_response = self.client.post(
            "/api/appointments",
            headers={"Authorization": f"Bearer {token}"},
            json=self._appointment_payload(),
        )

        self.assertEqual(201, create_response.status_code)
        body = create_response.json()
        self.assertEqual("pending", body["status"])
        self.assertEqual("Corte masculino", body["service_name"])
        self.assertEqual("Barbeiro Teste", body["professional_name"])

        with SessionLocal() as db:
            rows = db.scalars(select(Appointment)).all()
            self.assertEqual(1, len(rows))
            self.assertEqual(body["id"], rows[0].id)
            self.assertEqual("Preferencia por maquina 2", rows[0].notes)

    def test_service_duration_must_fit_available_range(self):
        response = self.client.post(
            "/api/appointments",
            headers={"Authorization": f"Bearer {self._login_token()}"},
            json=self._appointment_payload(time(17, 30)),
        )

        self.assertEqual(400, response.status_code)
        self.assertIn("indispon", response.json()["detail"].lower())

    def test_professional_cannot_receive_overlapping_appointments(self):
        headers = {"Authorization": f"Bearer {self._login_token()}"}
        first = self.client.post("/api/appointments", headers=headers, json=self._appointment_payload())
        second = self.client.post(
            "/api/appointments",
            headers=headers,
            json=self._appointment_payload(time(14, 30)),
        )

        self.assertEqual(201, first.status_code)
        self.assertEqual(409, second.status_code)

    def test_client_can_cancel_own_appointment_before_deadline(self):
        headers = {"Authorization": f"Bearer {self._login_token()}"}
        created = self.client.post("/api/appointments", headers=headers, json=self._appointment_payload())

        response = self.client.patch(
            f"/api/appointments/{created.json()['id']}/cancel",
            headers=headers,
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("cancelled", response.json()["status"])

    def test_cancellation_is_rejected_after_deadline(self):
        with SessionLocal() as db:
            client = db.scalar(select(User).where(User.email == "cliente@test.com"))
            row = Appointment(
                client_id=client.id,
                professional_id=self.professional_id,
                service_id=self.service_id,
                scheduled_at=datetime.now(timezone.utc) + timedelta(hours=1),
                status="pending",
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            appointment_id = row.id

        response = self.client.patch(
            f"/api/appointments/{appointment_id}/cancel",
            headers={"Authorization": f"Bearer {self._login_token()}"},
        )

        self.assertEqual(400, response.status_code)
        self.assertIn("24h", response.json()["detail"])

    def test_admin_can_cancel_client_appointment(self):
        headers = {"Authorization": f"Bearer {self._login_token()}"}
        created = self.client.post("/api/appointments", headers=headers, json=self._appointment_payload())

        response = self.client.patch(
            f"/api/appointments/{created.json()['id']}/cancel",
            headers={"Authorization": f"Bearer {self._admin_token()}"},
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("cancelled", response.json()["status"])

    def test_admin_marks_past_appointment_done_and_client_sees_history(self):
        appointment_id = self._insert_past_appointment()

        completed = self.client.patch(
            f"/api/appointments/{appointment_id}/complete",
            headers={"Authorization": f"Bearer {self._admin_token()}"},
        )
        history = self.client.get(
            "/api/appointments",
            params={"status": "done", "mine": "true"},
            headers={"Authorization": f"Bearer {self._login_token()}"},
        )

        self.assertEqual(200, completed.status_code)
        self.assertEqual("done", completed.json()["status"])
        self.assertEqual([appointment_id], [row["id"] for row in history.json()])
        self.assertEqual("35.00", history.json()[0]["service_price"])

    def test_future_appointment_cannot_be_completed(self):
        created = self.client.post(
            "/api/appointments",
            headers={"Authorization": f"Bearer {self._login_token()}"},
            json=self._appointment_payload(),
        )

        response = self.client.patch(
            f"/api/appointments/{created.json()['id']}/complete",
            headers={"Authorization": f"Bearer {self._admin_token()}"},
        )

        self.assertEqual(400, response.status_code)
        self.assertIn("futuro", response.json()["detail"].lower())


if __name__ == "__main__":
    unittest.main()
