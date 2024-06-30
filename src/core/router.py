# FastAPI
from fastapi import APIRouter

from src.v1.router import router as router_v1
from src.core.healthcheck import router as hc

api_router = APIRouter()

api_router.include_router(router_v1, prefix="/api", tags=["Locations API"])
api_router.include_router(hc, tags=["healthcheck"])