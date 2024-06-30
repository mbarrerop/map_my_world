from sqlalchemy.orm import Session
from src.v1.schemas.reviews import LocationCategoryReviewedCreate
from src.v1.services import persistence as ps
from uuid import UUID


async def create_location_category_reviewed_service(db: Session, review: LocationCategoryReviewedCreate):
    return await ps.create_location_category_reviewed(db, review)


async def get_location_category_reviewed_service(db: Session, review_id: UUID):
    return await ps.get_location_category_reviewed(db, review_id)


async def update_location_category_reviewed_service(db: Session, review_id: UUID, review: LocationCategoryReviewedCreate):
    return await ps.update_location_category_reviewed(db, review_id, review)


async def get_remcommendations_service(db: Session):
    return await ps.get_recommendations(db)