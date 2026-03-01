import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from database import get_db
from fastapi.testclient import TestClient


# Créer une base de données en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

#----------------------
#client fixture
#--------------------
@pytest.fixture(scope="function")
def client():
    """
    Crée une base de données fraîche pour chaque test.
    """
    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)
    # Créer une session
    db = TestingSessionLocal()
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    db.close()
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

#-----------
# Fixtuture auth.
#---------------------
#token user:
@pytest.fixture
def user_token(client):
    client.post("/auth/signup", json={
        "username": "user",
        "password": "secret"
    })

    login_response = client.post("/auth/login", json={
        "username": "user",
        "password": "secret"
    })

    token = login_response.json()["access_token"]
    return token

# Fixture for a second user:
@pytest.fixture
def second_user_token(client):
    client.post("/auth/signup", json={
        "username": "user2",
        "password": "secret"
    })

    login = client.post("/auth/login", json={
        "username": "user2",
        "password": "secret"
    })

    return login.json()["access_token"]

#-------------------
# Fixture for create games

@pytest.fixture(params=["easy", "medium", "hard"])
def create_game (client, user_token,request):
    #GIVEN
    headers = {"Authorization": f"Bearer {user_token}"}
    #WHEN
    response = client.post(
        "/game/create",
        json = {

        "difficulty": request.param
        },
        headers = headers
    )
    #THEN
    assert response.status_code == 201
    game_id = response.json()["id"]
    return game_id
