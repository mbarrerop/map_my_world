from sqlalchemy.orm import Session
from src.v1.schemas.locations import LocationCreate
from src.v1.services import persistence as ps
from uuid import UUID


async def create_location_service(db: Session, location: LocationCreate):
    return await ps.create_location(db, location)

async def get_location_service(db: Session, location_id: UUID):
    return await ps.get_location(db, location_id)