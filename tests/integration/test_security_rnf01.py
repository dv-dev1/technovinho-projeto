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
from sqlalchemy import select  # noqa: E402

from app.db.base import Base  # noqa: E402
from app.db.session import SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models.user import User  # noqa: E402


class SecurityRNF01Tests(unittest.TestCase):
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
            for user in db.scalars(select(User)).all():
                db.delete(user)
            db.commit()

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


if __name__ == "__main__":
    unittest.main()
