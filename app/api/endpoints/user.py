from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_200_OK
from typing import Literal, Annotated
from core.dependencies import (
    get_user_dep, get_users_dep, delete_user_dep, update_user_dep, create_user_dep, authenticate_user, get_user_id_dep
)
from schema.user import ListUsersResponse, UpdateUserResponse, User
from fastapi.security import OAuth2PasswordRequestForm
from schema.user import Token
from core.security import create_access_token
from datetime import timedelta
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES



router = APIRouter()


# Create a new user
@router.post(
    '/users',
    status_code=HTTP_200_OK,
    response_description='create user',
    name='user:create',
    response_model_exclude_none=True,
    response_model=User,
)
def create_user(
    user_created: User= Depends(create_user_dep)
):
    return user_created


# Login to generate access token
@router.post('/token')
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect ID or password',
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# Get current logged-in user details
@router.get('/users/me/',
            response_model= User
)
async def read_users_me(
        current_user: Annotated[User, Depends(get_user_dep)],
):
    return current_user


# Get user by ID
@router.get(
    '/users/{userId}',
    status_code= HTTP_200_OK,
    response_description=' get user by id',
    name= 'user: get_by_id',
    response_model_exclude_none= True,
    response_model = User,
)
def get_user_by_id(
        current_user: Annotated[User, Depends(get_user_dep)],
        userId: str = Depends(get_user_id_dep),
):
    return userId


# Sort options for user list
SortOrder = Literal["created_at_asc", "created_at_desc", "name_asc", "name_desc"]


# Get list of users with sorting options
@router.get(
    '/users',
    status_code= HTTP_200_OK,
    response_description= 'get users list',
    name= 'user: list_users',
    response_model_exclude_none= True,
    response_model= ListUsersResponse
)
def get_users_list(
    current_user: Annotated[User, Depends(get_user_dep)],
    usersList: ListUsersResponse= Depends(get_users_dep),
):
    return usersList


# Delete user by ID
@router.delete(
    '/users/{userId}',
    status_code= HTTP_200_OK,
    response_description= 'delete user by id',
    name= 'user: delete_by_id',
    response_model_exclude_none= True,
)
def delete_user_by_id(
        current_user: Annotated[User, Depends(get_user_dep)],
        userId = Depends(delete_user_dep),
):
    return userId


# Update user by ID
@router.patch(
    '/users/{userId}',
    status_code=HTTP_200_OK,
    response_description='update user',
    name='user: update',
    response_model_exclude_none=True,
)
def update_user(
        current_user: Annotated[User, Depends(get_user_dep)],
        userId=Depends(update_user_dep),
) -> UpdateUserResponse:
    return userId