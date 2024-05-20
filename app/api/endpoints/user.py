from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from app.core.dependecies import create_user
from app.schema.user import CreateUserResponse



router = APIRouter()


@router.post(
    '',
    status_code=HTTP_200_OK,
    response_description='create user',
    name='user:create',
    response_model_exclude_none=True,
    response_model=CreateUserResponse,
)
def create_user(
    user_created: CreateUserResponse= Depends(create_user)
):
    return user_created