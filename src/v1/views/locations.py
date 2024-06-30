# FastAPI
from fastapi import APIRouter, status, Body, Depends, Request

from sqlalchemy.orm import Session
from config.database import get_db
from src.v1.schemas.locations import Location, LocationCreate
from uuid import UUID

from src.core.exceptions import DataNotFoundException as NotFound

from src.v1.services.locations import create_location_service, get_location_service


router = APIRouter(prefix="/locations")



@router.get("/{location_id}", response_model=Location)
async def read_location(request: Request, 
                        location_id: UUID, 
                        db: Session = Depends(get_db)):

    db_location = await get_location_service(db, location_id)
    
    if not db_location:
        raise NotFound(detail=f"Location with ID {location_id} not found")
    return db_location
    
        

@router.post("", status_code=status.HTTP_200_OK, response_model=Location)
async def add_location(request: Request, 
                       data: LocationCreate = Body(...), 
                       db: Session = Depends(get_db)):

    db_location = await create_location_service(db, data)
    return db_location
