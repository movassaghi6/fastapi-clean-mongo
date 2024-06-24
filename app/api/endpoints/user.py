from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK
from typing import Literal




from app.core.dependencies import create_user_dep, get_user_dep, get_users_dep, delete_user_dep, update_user_dep
from app.schema.user import CreateUserResponse, ListUsersResponse, UpdateUserResponse



router = APIRouter()


@router.post(
    '/users',
    status_code=HTTP_200_OK,
    response_description='create user',
    name='user:create',
    response_model_exclude_none=True,
    response_model=CreateUserResponse,
)
def create_user(
    user_created: CreateUserResponse= Depends(create_user_dep)
):
    return user_created

@router.get(
    '/users/{userId}',
    status_code= HTTP_200_OK,
    response_description=' get user by id',
    name= 'user: get_by_id',
    response_model_exclude_none= True,
    response_model = CreateUserResponse,
)
def get_user_by_id(
        userId: CreateUserResponse = Depends(get_user_dep)
):
    return userId


SortOrder = Literal["created_at_asc", "created_at_desc", "name_asc", "name_desc"]

@router.get(
    '/users',
    status_code= HTTP_200_OK,
    response_description= 'get users list',
    name= 'user: list_users',
    response_model_exclude_none= True,
    response_model= ListUsersResponse
)
def get_users_list(
    usersList: ListUsersResponse= Depends(get_users_dep)
):
    return usersList

@router.delete(
    '/users/{userId}',
    status_code= HTTP_200_OK,
    response_description= 'delete user by id',
    name= 'user: delete_by_id',
    response_model_exclude_none= True,
)
def delete_user_by_id(
        userId = Depends(delete_user_dep)
):
    return userId


@router.put(
    '/users/{userId}',
    status_code=HTTP_200_OK,
    response_description='update user',
    name='user: update',
    response_model_exclude_none=True,
)
def update_user(
        userId=Depends(update_user_dep)
) -> UpdateUserResponse:
    return userId