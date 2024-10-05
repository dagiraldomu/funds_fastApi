import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.main import app
from app.models.funds import get_db
from app.settings.config import settings


async def override_get_db():
    client_db = AsyncIOMotorClient(settings.mongo_db_url)  # You can use a test database
    test_db = client_db.test_investment_db

    # Override the app's db with the test_db
    app.mongodb = test_db

    # Ensure the collections are cleared before each test
    await test_db.funds.delete_many({})
    await test_db.initialization.delete_many({})

    yield test_db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_fund():
    response = client.post("/api/funds", json={"name": "FUND", "minimum_investment": 100000, 'category': 'FPV'})
    assert response.status_code == 200
    data = response.json()
    assert "_id" in data
    assert data["name"] == "FUND"
    assert data["minimum_investment"] == 100000

def test_create_client():
    response = client.post("/api/clients", json={"name": "Jane Doe", "email": 'jane@example.com', 'phone': '1234567890', 'notification_preference': 'email'})
    assert response.status_code == 200
    data = response.json()
    assert "_id" in data
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane@example.com"
    assert data["phone"] == "1234567890"
    assert data["notification_preference"] == "email"
