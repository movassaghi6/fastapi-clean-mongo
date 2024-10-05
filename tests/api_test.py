# tests/api_test.py
import pytest
from fastapi.testclient import TestClient
from app.model.user import User
from unittest.mock import patch, MagicMock
from bson import ObjectId
from datetime import datetime, timezone
from fastapi import HTTPException, Depends
from app.model.user import PyObjectId
from unittest import mock
from pymongo import MongoClient
from app.main import app  # Assuming app.main has your FastAPI app instance
from app.schema.user import User, CreateUserRequest
from app.core.dependencies import create_user_dep, get_user
from app.repository.user import UserRepository
from app.core.dependencies import get_mongodb_repo, _get_mongo_client
from app.core.config import MONGO_COLLECTION_USERS
from app.core.database import get_mongodb


'''@pytest.fixture
def client():
    client = TestClient(app=app)
    return client'''

client = TestClient(app)


class MockMongoClient:
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        return self.db

    def __exit__(self, *args):
        pass

@pytest.fixture
def mock_mongodb():
    def mock_get_mongodb():
        mock_client = MongoClient()
        return MockMongoClient(mock_client.db)

    return mock_get_mongodb



def test_get_user_by_id(mock_mongodb):
    app.dependency_overrides[get_mongodb] = mock_mongodb
    response = client.get("/v1/user/666e9adbd881b76ee1a9867a")

    assert response.status_code == 200
    #assert response.status_code == 200