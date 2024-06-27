# Starlette
from starlette.middleware.cors import CORSMiddleware

# FastAPI
from fastapi import FastAPI
from src.core.router import api_router

# Env
from decouple import config, Csv

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
    print("*" * 20, flush=True)
    print("Starting up...", flush=True)
    print("*" * 20, flush=True)


@app.on_event("shutdown")
def shutdown_event():
    print("*" * 20, flush=True)
    print("Shutting down...", flush=True)
    print("*" * 20, flush=True)


app.include_router(api_router)