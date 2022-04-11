import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from data.database import get_db, Base, SessionLocal, SQLALCHEMY_DATABASE_URL
from data.JWT import check_if_active_user, check_if_superuser
from data.schemas import User


async def avoid_token():
    return User(
        user_id=1,
        name="name",
        email="email",
        password="password",
        is_active=True,
        is_admin=False
    )


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="module")
def db(db_engine):
    connection = db_engine.connect()
    connection.begin()
    db = SessionLocal(bind=connection)
    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[check_if_active_user] = avoid_token
    app.dependency_overrides[check_if_superuser] = avoid_token
    with TestClient(app) as c:
        yield c
