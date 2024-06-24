from typing import AsyncGenerator, Callable, Type, Optional, Literal
from datetime import datetime, timezone
from fastapi import Depends, Body, HTTPException, status
from pymongo import MongoClient
import pymongo
from starlette.requests import Request
from pydantic import conint
from app.repository.base import BaseRepository
from app.repository.user import UserRepository
from app.model.user import User
from app.schema.user import CreateUserRequest, CreateUserResponse, ListUsersResponse, DeleteUserResponse
from app.schema.user import UpdateUserRequest, UpdateUserResponse
from app.core.config import MONGO_COLLECTION_USERS





def _get_mongo_client(request: Request) -> MongoClient:
    return request.app.state.mongo_client

def get_mongodb_repo(repo_type: Type[BaseRepository]) -> Callable:
    async def _get_repo(
         mongo_client: MongoClient = Depends(_get_mongo_client),
    ) -> AsyncGenerator[BaseRepository, None]:
        yield repo_type(mongo_client)

    return _get_repo


def create_user_dep(
        create_req: CreateUserRequest = Body(..., ),
        user_repo: UserRepository = Depends(get_mongodb_repo(UserRepository))
) -> CreateUserResponse:

    user_in_db = User(email=create_req.email,
                      name= create_req.name,
                      password=create_req.password,
                      created_at= datetime.now(timezone.utc))
    user_created= user_repo.create(model=user_in_db, collection=MONGO_COLLECTION_USERS)
    create_user_response = CreateUserResponse(user_id= str(user_created.id),
                                              email= user_created.email,
                                              name= user_created.name,
                                              created_at=user_created.created_at)
    return create_user_response

def get_user_dep(
        ID: str,
        user_repo: UserRepository= Depends(get_mongodb_repo(UserRepository))
) -> CreateUserResponse:

    user_in_db = user_repo.get_by_id(MONGO_COLLECTION_USERS, ID)
    if user_in_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
    create_user_response= CreateUserResponse(user_id= str(user_in_db.id),
                                             email = user_in_db.email,
                                             name= user_in_db.name,
                                             created_at= user_in_db.created_at)
    return create_user_response


def get_users_dep(
        sort: Literal["created_at_asc", "created_at_desc", "name_asc", "name_desc"] = None,
        page: Optional[conint(ge=1)] = 1,
        limit: conint(ge=5, multiple_of=5) = 10,
        user_repo: UserRepository= Depends(get_mongodb_repo(UserRepository))
) -> ListUsersResponse:

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
        CreateUserResponse(user_id=str(user_in_db.id),
                           email=user_in_db.email,
                           name=user_in_db.name,
                           created_at=user_in_db.created_at)
        for user_in_db in user_list_db
    ],
        meta={
            'page': page,
            'limit': limit,
            'total': total
        })


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
