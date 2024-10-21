import pytest
from fastapi.testclient import TestClient
from app.main import app
import httpx

client = TestClient(app)


@pytest.fixture
def registered_user():
    response = client.post(
        "/register",
        json={"name": "testuser", "email": "testuser@example.com",
              "password": "testpassword"}
    )
    assert response.status_code in [200, 409]
    if response.status_code == 409:
        print("usuário já existe. prosseguindo com o login")


@pytest.fixture
def auth_token(registered_user):
    response = client.post(
        "/login",
        json={"email": "testuser@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]


def test_protected_data(auth_token):
    """
    usa a fixture auth_token para testar o login e obter o token de autenticação

    por sua vez, a fixture auth_token usa a fixture registered_user para testar o registro do usuário

    no fim, o teste usa o token de autenticação para acessar a rota protegida e testar a resposta
    """

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/external-data", headers=headers)

    print(f'status_code: {response.status_code}')
    print(f'response: {response.json()}')

    assert response.status_code == 200
    assert "facts" in response.json()
    assert isinstance(response.json()["facts"], list)
    assert len(response.json()["facts"]) == 3
    assert all(isinstance(fact, str) for fact in response.json()["facts"])
