from fastapi import APIRouter

from app.api.routes import root, predict

api_router = APIRouter()
api_router.include_router(root.router, tags=["root"])
api_router.include_router(predict.router, tags=["predict"])