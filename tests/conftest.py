import os

# setdefault: no pisa si ya viene del CI o del entorno
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost/test")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-pytest-only-1234567890ab")
os.environ.setdefault("ANIME1V_URL", "http://localhost:3000")
os.environ.setdefault("ANIME1V_KEY", "test-key")
os.environ.setdefault("DB_SSLMODE", "disable")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Engine SQLite en memoria — tests rápidos sin necesitar PostgreSQL
_test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestSession = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)

# Parchamos ANTES de que la app importe el engine original
import API.database.config as _db_cfg
_db_cfg.engine = _test_engine
_db_cfg.SessionLocal = _TestSession

from API.database.config import Base, get_db
from API.src.core.config import get_settings
from API.app import app

get_settings.cache_clear()
Base.metadata.create_all(bind=_test_engine)


@pytest.fixture(autouse=True)
def limpiar_tablas():
    yield
    with _test_engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()


@pytest.fixture
def db():
    session = _TestSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
