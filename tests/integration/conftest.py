import os
import sys
import tempfile
from pathlib import Path

import pytest
from sqlalchemy import delete


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"

sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(ROOT))

DB_FILE = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
DB_FILE.close()

os.environ["DATABASE_URL"] = f"sqlite:///{DB_FILE.name}"
os.environ["JWT_SECRET"] = "test-secret"

from app.db.base import Base  # noqa: E402
from app.db.session import engine  # noqa: E402
from app.models.appointment import Appointment  # noqa: E402
from app.models.availability import Availability  # noqa: E402
from app.models.professional import Professional  # noqa: E402
from app.models.service import Service  # noqa: E402
from app.models.user import User  # noqa: E402


def clean_integration_db(db):
    for model in (Appointment, Availability, Professional, Service, User):
        db.execute(delete(model))
    db.commit()


@pytest.fixture(scope="session", autouse=True)
def integration_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    try:
        os.unlink(DB_FILE.name)
    except OSError:
        pass
