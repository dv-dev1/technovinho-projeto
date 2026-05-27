import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def _current_database_url() -> str:
    return os.getenv("DATABASE_URL", settings.database_url)


def _engine_kwargs(database_url: str) -> dict:
    kwargs = {"pool_pre_ping": True}
    if database_url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
    return kwargs


_database_url = None
_engine = None
_session_factory = None


def _ensure_session_factory():
    global _database_url, _engine, _session_factory

    database_url = _current_database_url()
    if _session_factory is not None and _engine is not None and _database_url == database_url:
        return

    if _engine is not None:
        _engine.dispose()

    _engine = create_engine(database_url, **_engine_kwargs(database_url))
    _session_factory = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    _database_url = database_url


class _EngineProxy:
    def __getattr__(self, name):
        _ensure_session_factory()
        return getattr(_engine, name)


class _SessionFactoryProxy:
    def __call__(self, *args, **kwargs):
        _ensure_session_factory()
        return _session_factory(*args, **kwargs)

    def __getattr__(self, name):
        _ensure_session_factory()
        return getattr(_session_factory, name)


engine = _EngineProxy()
SessionLocal = _SessionFactoryProxy()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
