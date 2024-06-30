from typing import List
from uuid import UUID

# FastAPI
from fastapi import APIRouter, Body, Depends, Request

from sqlalchemy.orm import Session
from config.database import get_db
from src.core.exceptions import DataNotFoundException as NotFound
from src.v1.schemas.reviews import (LocationCategoryReviewed, 
                                    LocationCategoryReviewedCreate, 
                                    LocationCategoryReviewedUpdate)
from src.v1.services.reviews import (get_remcommendations_service, 
                                     create_location_category_reviewed_service,
                                     get_location_category_reviewed_service,
                                     update_location_category_reviewed_service)


router = APIRouter(prefix="/reviews")


@router.get("/{review_id}", response_model=LocationCategoryReviewed)
async def get_review_location(request: Request,
                              review_id: UUID,
                              db: Session = Depends(get_db)):

    review = await get_location_category_reviewed_service(db, review_id)
    return review

@router.post("", response_model=LocationCategoryReviewed)
async def add_review_location(request: Request, 
                                 data: LocationCategoryReviewedCreate = Body(...), 
                                 db: Session = Depends(get_db)):

    review = await create_location_category_reviewed_service(db, data)
    return review

@router.put("/{review_id}", response_model=LocationCategoryReviewed)
async def update_review_location(review_id: UUID, 
                                 data: LocationCategoryReviewedUpdate = Body(...), 
                                 db: Session = Depends(get_db)):
    
    updated_review = await update_location_category_reviewed_service(db, review_id, data)
    if not updated_review:
        raise NotFound(detail=f"Review ID {review_id} not found")
    return updated_review

@router.get("/recommendations", response_model=List[LocationCategoryReviewed])
async def get_recommendations(request: Request, db: Session = Depends(get_db)):

    db_recom = await get_remcommendations_service(db)
    
    if not db_recom or len(db_recom) == 0:
        raise NotFound(detail=f"Recommendations not found")
    return db_recom