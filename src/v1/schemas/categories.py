from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str = Field(..., description="Category name", example="Park")
    description: Optional[str] = Field(None, description="Category description", example="A category for public parks")


class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int = Field(..., description="Category ID", example=1)
    created_at: Optional[datetime] = Field(None, description="Creation timestamp", example="2024-01-01T00:00:00Z")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp", example="2024-01-02T00:00:00Z")

    class Config:
        orm_mode = True
        from_attributes = True