# FastAPI
from fastapi import APIRouter

from src.v1.router import router as router_v1

api_router = APIRouter()

api_router.include_router(router_v1, prefix="/v1", tags=["v1"])