from fastapi import APIRouter
from src.v1.views import locations

router = APIRouter(prefix="/api")

router.include_router(locations.router)