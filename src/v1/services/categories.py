from sqlalchemy.orm import Session
from src.v1.schemas.categories import CategoryCreate
from src.v1.models import Location as LocationDB
from src.v1.services import persistence as ps


async def create_category_service(db: Session, category: CategoryCreate):
    return await ps.create_category(db, category)

async def get_category_service(db: Session, category_id: int):
    return await ps.get_category(db, category_id)