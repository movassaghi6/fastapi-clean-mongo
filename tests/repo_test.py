import pytest
from pymongo import MongoClient
from app.core.config import MONGO_COLLECTION_USERS, MONGO_DATABASE
from app.model.user import User
from app.repository.user import UserRepository
from datetime import datetime


@pytest.fixture(scope="module")
def mongo_client():
    client = MongoClient("mongodb://localhost:27017")
    yield client
    client.close()

@pytest.fixture(scope="module")
def user_repository(mongo_client):
    repository = UserRepository(mongo_client[MONGO_DATABASE])
    yield repository

    mongo_client[MONGO_DATABASE][MONGO_COLLECTION_USERS].delete_many({})

def test_create(user_repository):
    created_at = datetime.now()
    user = User(name="Amir Mov", email= "AmirEmail@yahoo.com", password="32rdeegft43", created_at=created_at)
    created_user = user_repository.create(user, MONGO_COLLECTION_USERS)


    assert created_user is not None
    assert created_user.name == "Amir Mov"
    assert created_user.email == "AmirEmail@yahoo.com"

def test_get_by_id(user_repository):
    created_at = datetime.now()
    user = User(name="Amirdag2", email="Amirdfs@yahoo.com", password="32dsat37", created_at=created_at)
    created_user = user_repository.create(user, MONGO_COLLECTION_USERS)

    retrieved_user = user_repository.get_by_id(MONGO_COLLECTION_USERS, str(created_user.id))

    assert retrieved_user.id == created_user.id
    assert retrieved_user.name == "Amirdag2"
    assert retrieved_user.email == "Amirdfs@yahoo.com"

def test_get_list(user_repository):
    created_at = datetime.now()
    users = [
        User(name="Amirdag5", email="Amirdf6@yahoo.com", password="32dsat3666", created_at=created_at),
        User(name="Amirdag6", email="Amirdf66@yahoo.com", password="32dsat6667", created_at=created_at),
        User(name="Amirdag7", email="Amirdf666@yahoo.com", password="32dsat3654", created_at=created_at),
    ]
    for user in users:
        user_repository.create(user, MONGO_COLLECTION_USERS)

    retrieved_users, total = user_repository.get_list(MONGO_COLLECTION_USERS)

    assert len(retrieved_users) >= 3
    assert total >=3