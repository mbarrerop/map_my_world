# FastAPI
from fastapi import APIRouter, status, Body, Depends, Request, Response,  File, UploadFile, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder


router = APIRouter(prefix="/locations")


@router.post("", status_code=status.HTTP_200_OK)
async def add_location(request: Request):
    pass