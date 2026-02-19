import pytest
from app import create_app
from models import db


@pytest.fixture
def app():
    app = create_app()
    # Use an in-memory SQLite DB for isolated tests
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')

    # Ensure a clean schema for each test session
    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    # Teardown: drop all tables
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
