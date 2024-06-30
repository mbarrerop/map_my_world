# FastAPI
from fastapi import APIRouter, status, Body, Depends, Request

from sqlalchemy.orm import Session
from config.database import get_db
from src.v1.schemas.categories import CategoryCreate, Category
from uuid import UUID

from src.core.exceptions import DataNotFoundException as NotFound

from src.v1.services.categories import create_category_service, get_category_service


router = APIRouter(prefix="/categories")



@router.get("/{category_id}", response_model=Category)
async def get_category(request: Request, 
                       category_id: int, 
                       db: Session = Depends(get_db)):

    db_category = await get_category_service(db, category_id)
    
    if not db_category:
        raise NotFound(detail=f"Category with ID {category_id} not found")
    return db_category
    
        

@router.post("", status_code=status.HTTP_200_OK, response_model=Category)
async def add_category(request: Request, 
                       data: CategoryCreate = Body(...), 
                       db: Session = Depends(get_db)):

    db_category = await create_category_service(db, data)
    return db_category
