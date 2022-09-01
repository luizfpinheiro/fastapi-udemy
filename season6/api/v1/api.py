from sys import api_version
from fastapi import APIRouter
from api.v1.endpoints import user, article

api_router = APIRouter()
api_router.include_router(article.router, prefix='/articles', tags=['articles'])
api_router.include_router(user.router, prefix='/users', tags=['users'])
