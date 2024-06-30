from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from src.v1.schemas.categories import Category



class LocationBase(BaseModel):
    name: str = Field(..., description="Location name", example="Central Park")
    description: Optional[str] = Field(None, description="Location description", example="A large public park in Madrid city")
    latitude: float = Field(..., description="Location latitude", example=40.785091)
    longitude: float = Field(..., description="Location longitude", example=-73.968285)
    category_id: int = Field(..., description="ID of the category this location belongs to", example=1)
    category: Optional[Category] = None
    
    
class Location(LocationBase):
    id: UUID = Field(default_factory=uuid4, description="Location ID", example="123e4567-e89b-12d3-a456-426614174000")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp", example="2024-01-01T00:00:00Z")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp", example="2024-01-02T00:00:00Z")
    
    class Config:
        orm_mode = True
        from_attributes = True
    
    
class LocationCreate(LocationBase):
    pass