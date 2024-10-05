from fastapi import APIRouter
from api.endpoints import user as user_router



router = APIRouter()


# Include user-related routes under the /api/v1 prefix and tag them as 'USER V1'
router.include_router(user_router.router, tags=['USER V1'], prefix='/api/v1')
