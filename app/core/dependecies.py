from typing import AsyncGenerator, Callable, Type, Optional, Literal
from datetime import datetime

from fastapi import Depends, Body
from pymongo import MongoClient
from starlette.requests import Request
from pydantic import conint

from app.repository.base import BaseRepository
from app.repository.user import UserRepository
from app.model.user import User
from app.schema.user import CreateUserRequest, CreateUserResponse
from app.core.config import MONGO_COLLECTION_USERS



def _get_mongo_client(request: Request) -> MongoClient:
    return request.app.state.mongo_client

def get_mongodb_repo(repo_type: Type[BaseRepository]) -> Callable:
    async def _get_repo(
         mongo_client: MongoClient = Depends(_get_mongo_client),
    ) -> AsyncGenerator[BaseRepository, None]:
        yield repo_type(mongo_client)

    return _get_repo


def create_user(
        create_req: CreateUserRequest = Body(..., ),
        user_repo: UserRepository = Depends(get_mongodb_repo(UserRepository))
) -> CreateUserResponse:

    user_in_db = User(email=create_req.email,
                      name= create_req.name,
                      password=create_req.password,
                      created_at= datetime.utcnow())
    user_created= user_repo.create(user_in_db, MONGO_COLLECTION_USERS)
    create_user_response = CreateUserResponse(user_id= str(user_created.id),
                                              email= user_created.email,
                                              name= user_created.name,
                                              created_at=user_created.created_at)
    return create_user_response