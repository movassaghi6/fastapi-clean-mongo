from typing import AsyncGenerator, Callable, Type, Optional, Literal, Annotated
from fastapi import Depends, Body, HTTPException, status
from pymongo import MongoClient
import pymongo
from starlette.requests import Request
from pydantic import conint
from repository.base import BaseRepository
from repository.user import UserRepository
from model.user import UserDB
from schema.user import ListUsersResponse, DeleteUserResponse, CreateUserRequest
from schema.user import UpdateUserRequest, UpdateUserResponse
from core.config import MONGO_COLLECTION_USERS
import jwt
from jwt.exceptions import InvalidTokenError
from schema.user import TokenData, User
from core.config import SECRET_KEY, ALGORITHM, MONGODB_URL
from core.security import oauth2_scheme, verify_password, get_password_hash



# Dependency to retrieve the MongoClient from the request
def _get_mongo_client(request: Request) -> MongoClient:
    return request.app.state.mongo_client


# Get a repository instance with the MongoDB client
def get_mongodb_repo(repo_type: Type[BaseRepository]) -> Callable:
    async def _get_repo(
         mongo_client: MongoClient = Depends(_get_mongo_client),
    ) -> AsyncGenerator[BaseRepository, None]:
        yield repo_type(mongo_client)

    return _get_repo


# Fetch a user by username from the database
def get_user(
        username: str,
   ):
    mongo_client = MongoClient(MONGODB_URL)
    user_repo = UserRepository(mongo_client)
    user_in_db = user_repo.get_by_name(MONGO_COLLECTION_USERS, username)
    return user_in_db


# Authenticate a user by verifying username and password
def authenticate_user(username: str, password: str):
    user = get_user(username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Create a new user and return the response schema
def create_user_dep(
        create_req: CreateUserRequest = Body(..., ),
        user_repo: UserRepository = Depends(get_mongodb_repo(UserRepository))
) -> User:

    user_in_db = UserDB(email=create_req.email,
                        hashed_password=get_password_hash(create_req.password),
                        username= create_req.username
                       )
                      
    user_created= user_repo.create(model=user_in_db, collection=MONGO_COLLECTION_USERS)
    create_user_response = User(user_id= str(user_created.id),
                                email= user_created.email,
                                username= user_created.username,
                                created_at=user_created.created_at
                               )
    return create_user_response


# Fetch the authenticated user based on the JWT token
async def get_user_dep(
        token: Annotated[User, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return User(user_id = str(user.id),
                email= user.email,
                username=user.username,
                created_at= user.created_at
               )


# Fetch a user by ID
def get_user_id_dep(
        ID: str,
        user_repo: UserRepository= Depends(get_mongodb_repo(UserRepository))
) -> User:

    user_in_db = user_repo.get_by_id(MONGO_COLLECTION_USERS, ID)
    if user_in_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
    create_user_response= User(user_id= str(user_in_db.id),
                                             email = user_in_db.email,
                                             username= user_in_db.username,
                                             created_at= user_in_db.created_at)
    return create_user_response


# Get a list of users with pagination and sorting options
def get_users_dep(
        sort: Literal["created_at_asc", "created_at_desc", "name_asc", "name_desc"] = None,
        page: Optional[int] = 1,
        limit: int = 10,
        user_repo: UserRepository= Depends(get_mongodb_repo(UserRepository))
) -> ListUsersResponse:
    
    # Apply conint validation
    page = conint(ge=1)(page)  # Ensure page number is at least 1
    limit = conint(ge=5, multiple_of=5)(limit)  # Limit must be a multiple of 5, minimum 5
    
    # Determine sorting field and order
    sort_field, sort_order = 'created_at', pymongo.DESCENDING
    if sort == "created_at_desc":
        sort_field, sort_order = 'created_at', pymongo.DESCENDING
    elif sort == "created_at_asc":
        sort_field, sort_order = 'created_at', pymongo.ASCENDING
    elif sort == "name_asc":
        sort_field, sort_order = 'name', pymongo.ASCENDING
    elif sort == "name_desc":
        sort_field, sort_order = 'name', pymongo.DESCENDING

    user_list_db, total= user_repo.get_list(collection=MONGO_COLLECTION_USERS,
                                            sort_field=sort_field,
                                            sort_order=sort_order,
                                            skip=(page - 1) * limit,
                                            limit=limit)

    return ListUsersResponse(users=[
        User(user_id=str(user_in_db.id),
                           email=user_in_db.email,
                           username=user_in_db.username,
                           created_at=user_in_db.created_at)
        for user_in_db in user_list_db
    ],
        meta={
            'page': page,
            'limit': limit,
            'total': total
        })


# Delete a user by ID
def delete_user_dep(
        ID: str,
        user_repo: UserRepository = Depends(get_mongodb_repo(UserRepository))
):
    user_in_db = user_repo.get_by_id(MONGO_COLLECTION_USERS, ID)
    if user_in_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    user_repo.delete(MONGO_COLLECTION_USERS, ID)

    delete_user_response= DeleteUserResponse(user_id=str(user_in_db.id))

    return f"user with this info {delete_user_response} deleted successfully."


# Update a user by ID
def update_user_dep(
        ID: str,
        user_repo: UserRepository = Depends(get_mongodb_repo(UserRepository)),
        req: UpdateUserRequest = None
) -> UpdateUserResponse:
    update_user = user_repo.update(MONGO_COLLECTION_USERS,id= ID, req= req)

    return UpdateUserResponse(user_id= str(update_user.id),
                              email = update_user.email,
                              name = update_user.name,
                              created_at= update_user.created_at
                              )
