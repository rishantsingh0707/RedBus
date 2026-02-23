from routes import user_routes
from fastapi import APIRouter

router = APIRouter()

router.include_router(user_routes.router, prefix="/users", tags=["users"])
# router = APIRouter()
