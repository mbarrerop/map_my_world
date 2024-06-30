from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

class LocationCategoryReviewedBase(BaseModel):
    location_id: UUID = Field(..., description="Location id", example="123e4567-e89b-12d3-a456-426614174000")
    category_id: int = Field(..., description="Category id", example=1)
    review_notes: Optional[str] = Field(None, description="Notes about the review", example="Checked and verified.")


class LocationCategoryReviewedCreate(LocationCategoryReviewedBase):
    pass


class LocationCategoryReviewed(LocationCategoryReviewedBase):
    id: UUID = Field(default_factory=uuid4, description="Review ID", example="123e4567-e89b-12d3-a456-426614174000")
    review_date: Optional[datetime] = Field(None, description="Date of the review", example="2024-01-01T00:00:00Z")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp", example="2024-01-01T00:00:00Z")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp", example="2024-01-02T00:00:00Z")

    class Config:
        orm_mode = True
        from_attributes = True
        
class LocationCategoryReviewedUpdate(BaseModel):
    review_notes: str = Field(..., description="Notes about the review", example="Checked and verified.")
    
    class Config:
        orm_mode = True
        from_attributes = True
        
