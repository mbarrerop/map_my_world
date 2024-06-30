from fastapi import APIRouter
from src.v1.views import locations, categories, reviews

router = APIRouter(prefix="/v1")

router.include_router(locations.router)
router.include_router(categories.router)
router.include_router(reviews.router)