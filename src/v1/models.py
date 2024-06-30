from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from config.database import Base
import uuid



class Location(Base):
    __tablename__ = "locations"

    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, unique=True)
    description = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    location = Column(Geometry("POINT"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    category = relationship("Category", back_populates="locations")
    reviews = relationship("LocationCategoryReviewed", back_populates="location")
    
    


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_defaul=func.now(), onupdate=func.now())
    
    locations = relationship("Location", back_populates="category")
    reviews = relationship("LocationCategoryReviewed", back_populates="category")
    

class LocationCategoryReviewed(Base):
    __tablename__ = "location_category_reviewed"

    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey('locations.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    review_date = Column(DateTime, onupdate=func.now())
    review_notes = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    location = relationship("Location", back_populates="reviews")
    category = relationship("Category", back_populates="reviews")
    
    __table_args__ = (UniqueConstraint('location_id', 'category_id', name='_location_category_uc'),)