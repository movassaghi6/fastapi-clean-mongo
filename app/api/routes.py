from fastapi import APIRouter, Request

from app.api.endpoints import user as user_router



router = APIRouter()

router.include_router(user_router.router, tags=['USER V1'], prefix='/api/v1')



@router.get(
    '/api/v1/hello',
    name= 'probe:liveness'
)
def hello_world(request: Request):
    return {'message': 'Hello World', 'root_path': request.scope.get('root_path')}
