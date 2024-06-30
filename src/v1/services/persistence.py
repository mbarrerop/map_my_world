from typing import List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from uuid import UUID
from src.v1.schemas.locations import LocationCreate
from src.v1.schemas.categories import CategoryCreate
from src.v1.schemas.reviews import (LocationCategoryReviewedCreate, 
                                    LocationCategoryReviewedUpdate, 
                                    LocationCategoryReviewed)
from src.v1.models import (Location as LocationDB, 
                           Category as CategoryDB,
                           LocationCategoryReviewed as LocationCategoryReviewedDB)

from src.core.exceptions import ValidationException

from datetime import datetime, timedelta


# Locations persistence

async def get_location(db: Session, location_id: UUID):
    return (
        db.query(LocationDB)
        .options(joinedload(LocationDB.category))
        .filter(LocationDB.id == location_id)
        .first()
    )

async def create_location(db: Session, location: LocationCreate):
    
    try:
        db_location = LocationDB(
            name=location.name,
            description=location.description,
            latitude=location.latitude,
            longitude=location.longitude,
            location=f'SRID=4326;POINT({location.longitude} {location.latitude})',
            category_id=location.category_id,
        )
        
        db.add(db_location)
        db.commit()
        db.refresh(db_location)
        
        db_review = LocationCategoryReviewedDB(
            location_id=db_location.id,
            category_id=db_location.category_id
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
        return db_location
    except IntegrityError as e:
        db.rollback()
        raise ValidationException(detail=f"Integrity error: {str(e.orig)}")


# Categories persistence

async def get_category(db: Session, category_id: int):
    return (db.query(CategoryDB)
            .filter(CategoryDB.id == category_id)
            .first())


async def create_category(db: Session, category: CategoryCreate):
    
    try:
        db_object = CategoryDB(
            name=category.name,
            description=category.description
        )
        
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        
        return db_object
    except IntegrityError as e:
        db.rollback()
        raise ValidationException(detail=f"Integrity error: {str(e.orig)}.")



# Reviews persistence

async def get_location_category_reviewed(db: Session, review_id: UUID):
    return (db.query(LocationCategoryReviewedDB)
            .filter(LocationCategoryReviewedDB.id == review_id)
            .first())


async def create_location_category_reviewed(db: Session, review: LocationCategoryReviewedCreate):
    
    try:
        db_object = LocationCategoryReviewedDB(
            location_id=review.location_id,
            category_id=review.category_id,
            review_notes=review.review_notes
        )
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        
        return db_object
    except IntegrityError as e:
        db.rollback()
        raise ValidationException(detail=f"Integrity error: {str(e.orig)} ")
    
    
async def update_location_category_reviewed(db: Session, review_id: UUID, review: LocationCategoryReviewedUpdate):
    try:
        db_review = (db.query(LocationCategoryReviewedDB)
                    .filter(LocationCategoryReviewedDB.id == review_id)
                    .first())
        if db_review is None:
            return db_review
        else:
            for key, value in review.dict().items():
                setattr(db_review, key, value)
            
            db.commit()
            db.refresh(db_review)
            return db_review
    except IntegrityError as e:
        db.rollback()
        raise ValidationException(detail=f"Integrity error: {str(e.orig)}")

    
async def get_recommendations(db: Session) -> list:
    recommendations = None
    thirty_days = datetime.utcnow() - timedelta(days=30)
    
    never_reviewed = (db.query(LocationCategoryReviewedDB)
                      .filter(LocationCategoryReviewedDB.review_date.is_(None))
                      .order_by(func.random())
                      .limit(10)
                      .all())

    if len(never_reviewed) < 10:
        reviewed_older_than_30_days = (db.query(LocationCategoryReviewedDB)
                                       .filter(LocationCategoryReviewedDB.review_date <= thirty_days)
                                       .order_by(func.random())
                                       .limit(10 - len(never_reviewed))
                                       .all())

        recommendations = never_reviewed + reviewed_older_than_30_days
    else:
        recommendations = never_reviewed
        
    if recommendations:
        recommendations = [LocationCategoryReviewed.from_orm(rec) for rec in recommendations]

    return recommendations
    
    
    
    
    
    