from fastapi import APIRouter

from app.api.routes import auth_routes, user_routes

api_router = APIRouter()


@api_router.get("/")
async def root():
    return {"msg": "Up and Running"}


api_router.include_router(auth_routes.auth_router)
api_router.include_router(user_routes.user_router)
