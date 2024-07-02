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
  - [Install PostgreSQL & PostGIS Plugin on Linux](#Install-Posgresql-&-PostGIS-Plugin-on-Linux)
  - [Setup Python Environment](#setup-python-environment)
  - [Docker Deployment](#docker-deployment)
- [Running the Application](#running-the-application)
  - [Docker](#docker)
  - [Locally](#locally)
- [License](#License)

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
After enviroment configuration and running you can prove and see docs in **{your_server}/docs** or http://127.0.0.1:8000/docs (if the running is locally)
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

### Install Posgresql & PostGIS Plugin on Linux

To install the PostGIS plugin on a Linux machine, follow these steps:

```sh
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install postgis postgresql-12-postgis-3
```

In a terminal access to psql as superuser:
```sh
sudo -i -u postgres
```
Open PostgreSQL interpreter:
```sh
psql
```
Add postgis plugin
 ```sql
CREATE EXTENSION postgis;
```
### Optional settings
Create a database:
```sql
CREATE DATABASE mydatabase;
CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
```

## Setup Python Environment

1. Create a virtual environment with Python 3.11:

```sh
python3.11 -m venv venv
source venv/bin/activate
```

2. Install the required Python packages:

```sh
pip install -r requirements.txt
```
3. In the main folder, create a `.env` file with the following variables:

```python
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
DRIVER_NAME=postgresql+psycopg2
DB_USER=your_db_user
DB_PASS=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
DB_NAME=your_db_name
```

## Running the Application

### Docker
To start the application using Docker:

Build the image
```sh
docker build -t map_my_world .
```
Run docker
```sh
docker run -d --name map_my_world_container map_my_world
```
### Locally
To start the application locally:
```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

# License
This project is distributed under the MIT License. You can find more details in the LICENSE file.

The MIT License is an open-source license that allows for free distribution and modification of the software, provided that the copyright notice is included in all copies. It is one of the most permissive and widely used licenses in the world of open-source software.

**Summary of the MIT License:**

- You can use, copy, modify, merge, publish, distribute, sublicense, and/or sell the software.
- You must include a copy of the copyright notice in all copies or substantial portions of the software.
- The software is provided "as is," without any warranties.

Be sure to refer to the [LICENSE](LICENSE) file for the full text of the MIT License and legal details. If you wish to use a different license, make sure to provide a link to the full text of that license instead of the MIT License.