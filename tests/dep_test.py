from app.schema.user import User, CreateUserRequest, ListUsersResponse
from app.repository.user import UserRepository
from app.core.config import MONGO_COLLECTION_USERS, MONGODB_URL, MONGO_DATABASE
from app.core.dependencies import create_user, get_user, get_users
import pymongo
import pytest

@pytest.fixture
def mongo_client():
    # create a MongoDB client for testing
    client = pymongo.MongoClient(MONGODB_URL)
    yield client
    client.close()

@pytest.fixture
def create_user_fixture(mongo_client):
    # create an instance of UserRepository with the mongo_client fixture
    repo = UserRepository(mongo_client)
    return lambda create_req: create_user(create_req=create_req, user_repo=repo)

@pytest.fixture
def get_user_fixture(mongo_client):
    repo = UserRepository(mongo_client)
    return lambda ID: get_user(ID=ID, user_repo=repo)

@pytest.fixture
def get_users_fixture(mongo_client):
    repo = UserRepository(mongo_client)
    return lambda sort, page, limit: get_users(sort=sort, page=page, limit=limit, user_repo=repo)

def test_create_user(create_user_fixture, mongo_client):

    request = CreateUserRequest(email="amirasef@d.com", name="dsaf2", password="2323j423")
    # get the database from the mongo_client fixture
    db = mongo_client[MONGO_DATABASE]

    created_user: User= create_user_fixture(create_req = request)

    assert created_user is not None
    assert created_user.name == "dsaf2"
    assert created_user.email == "amirasef@d.com"
    # check that the user was created in the database
    user_doc = db[MONGO_COLLECTION_USERS].find_one({"email": "amirasef@d.com"})
    assert user_doc is not None

def test_get_user(create_user_fixture,get_user_fixture, mongo_client):

    request= CreateUserRequest(email='sadfa2@dasf.com', name='dsafdsa', password='314543143d')

    created_user: User= create_user_fixture(create_req= request)

    get_user : User = get_user_fixture(ID=created_user.user_id)

    assert get_user is not None
    assert get_user.name == "dsafdsa"
    assert get_user.email == "sadfa2@dasf.com"

def test_get_users(create_user_fixture, get_users_fixture, mongo_client):
    request1= CreateUserRequest(email='sad33@dasf.com', name='dsafdsa', password='314543143d')
    request2= CreateUserRequest(email='sad44@dasf.com', name='dsafdsa', password='314543143d')
   
    get_users: ListUsersResponse= get_users_fixture(sort="created_at_desc", page=1, limit=10)

    assert get_users is not None
    assert len([user for user in get_users.users]) >= 2




