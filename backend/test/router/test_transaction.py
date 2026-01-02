from fastapi.testclient import TestClient
from backend.src.main import app
from dependencies import get_session 
from sqlmodel import Session, SQLModel, create_engine



client = TestClient(app)

def get_test_session():
    return session

app.dependency_overrides[get_session] = get_test_session

def test_get_transactions():
    response = client.get("/transactions/")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_transaction_by_id():
    response = client.get("/transactions/1")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["amount"] == 100.0            
    

