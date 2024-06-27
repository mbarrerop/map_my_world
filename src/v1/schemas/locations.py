from pydantic import BaseModel, Field
from typing import Optional

class LocationBase(BaseModel):
    name: str = Field(..., description="Location name", example="Central Park")
    description: Optional[str] = Field(None, description="Location description", example="A large public park in Madrid city")
    latitude: float = Field(..., description="Location latitude", example=40.785091)
    longitude: float = Field(..., description="Location longitude", example=-73.968285)
    category_id: int = Field(..., description="ID of the category this location belongs to", example=1)
    
class Location(LocationBase):
    id: int = Field(..., description="Location ID", example=1)
    created_at: str = Field(..., description="Creation timestamp", example="2024-01-01T00:00:00Z")
    updated_at: str = Field(..., description="Last update timestamp", example="2024-01-02T00:00:00Z")