# Map My World API

## Overview

The Map My World API allows users to explore and review different locations and categories around the world, such as restaurants, parks, and museums. The goal is to provide an interactive map where users can discover new locations and see recommendations based on specific categories. The API is built using FastAPI, PostgreSQL, and PostGIS for spatial data support.

## Table of Contents

- [Models](#models)
  - [Location](#location)
  - [Category](#category)
  - [LocationCategoryReviewed](#locationcategoryreviewed)
- [Endpoints](#endpoints)
  - [Location Endpoints](#location-endpoints)
  - [Category Endpoints](#category-endpoints)
  - [Review Endpoints](#review-endpoints)
- [Environment Configuration](#environment-configuration)
- [Installation](#installation)
  - [Install PostGIS Plugin on Linux](#install-postgis-plugin-on-linux)
  - [Setup Python Environment](#setup-python-environment)
  - [Docker Deployment](#docker-deployment)
- [Running the Application](#running-the-application)
  - [Docker](#docker)
  - [Locally](#locally)
- [Tests](#tests)
  - [Test Files](#test-files)
  - [Running Tests](#running-tests)
  - [Example Test Case](#example-test-case)

## Models

### Location

```python
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
```

### Category

```python
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
```

### LocationCategoryReviewed

```python
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
```

## Endpoints

### Location Endpoints
  
- **GET /api/v1/locations/{location_id}**: Get a location by ID.
  - **Response Model**: `Location`
  - **Description**: Returns a location by its ID.
  
- **POST /api/v1/locations**: Create a new location.
  - **Request Body**: `LocationCreate`
  - **Response Model**: `Location`
  - **Description**: Creates a new location.

### Category Endpoints
  
- **GET /api/v1/categories/{category_id}**: Get a category by ID.
  - **Response Model**: `Category`
  - **Description**: Returns a category by its ID.
  
- **POST /api/v1/categories**: Create a new category.
  - **Request Body**: `CategoryCreate`
  - **Response Model**: `Category`
  - **Description**: Creates a new category.

### Review Endpoints

- **GET /api/v1/reviews/{review_id}**: Get a location-category review by ID.
  - **Response Model**: `LocationCategoryReviewed`
  - **Description**: Returns a location-category review by its ID.
  
- **POST /api/v1/reviews**: Create a new location-category review.
  - **Request Body**: `LocationCategoryReviewedCreate`
  - **Response Model**: `LocationCategoryReviewed`
  - **Description**: Creates a new location-category review.
  
- **PUT /api/v1/reviews/{review_id}**: Update a location-category review by ID.
  - **Request Body**: `LocationCategoryReviewedCreate`
  - **Response Model**: `LocationCategoryReviewed`
  - **Description**: Updates a location-category review by its ID.

  **GET /api/v1/reviews/recommendations**: Get a recommendations set to review.
  - **Response Model**: `List[LocationCategoryReviewed]`
  - **Description**: Returns recommendations list of location-category combinations that 
  have never been reviewed and/or whose last review was more than 30 days ago.
  

# Environment Configuration

## Installation

### Install PostGIS Plugin on Linux

To install the PostGIS plugin on a Linux machine, follow these steps:

```sh
sudo apt-get update
sudo apt-get install postgis postgresql-12-postgis-3
```

### Setup Python Environment

1. Create a virtual environment with Python 3.11:

```sh
python3.11 -m venv venv
source venv/bin/activate
```

2. Install the required Python packages:

```sh
pip install -r requirements.txt
```

## Running the Application

### Docker
To start the application using Docker:

```sh
docker build -t map_my_world .
docker run -d --name map_my_world_container map_my_world
```
### Locally
To start the application locally:
```sh
uvicorn src.v1.main:app --host 0.0.0.0 --port 8000
```

