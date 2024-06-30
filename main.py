# Starlette
from starlette.middleware.cors import CORSMiddleware

# FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Core
from src.core.router import api_router
from src.core.exceptions import DataNotFoundException, GeneralException, ValidationException

# Env
from decouple import config, Csv

# Database
from sqlalchemy.sql import text
from config.database import engine, Base

import logging

app = FastAPI(
    title="Map my World", 
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=config("CORS_ORIGINS", cast=Csv()),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


@app.on_event("startup")
def startup_event():
    init_db()
    print("*" * 20, flush=True)
    print("Starting up...", flush=True)
    print("*" * 20, flush=True)


@app.on_event("shutdown")
def shutdown_event():
    print("*" * 20, flush=True)
    print("Shutting down...", flush=True)
    print("*" * 20, flush=True)


app.include_router(api_router)


def init_db():
    
    try:
        logging.info("Creating entities...")
        Base.metadata.create_all(bind=engine)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = result.fetchall()
            logging.info(f"Current entities: {tables}")
    except Exception as e:
        logging.error(f"Error al crear las tablas: {e}")
        

# Exceptions handlers
        
@app.exception_handler(DataNotFoundException)
async def data_not_found_exception_handler(request: Request, exc: DataNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
    
@app.exception_handler(GeneralException)
async def general_exception_handler(request: Request, exc: GeneralException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
    
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred: "},
    )
    
@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )