from apis.version1 import route_articles
from apis.version1 import route_login
from apis.version1 import route_users
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(route_login.router, prefix="/login", tags=["login"])