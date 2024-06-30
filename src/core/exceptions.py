from fastapi import HTTPException
from src.core.utils import clean_text


class DataNotFoundException(HTTPException):
    def __init__(self, detail: str):
        detail = clean_text(detail)
        super().__init__(status_code=404, detail=detail)

    
class GeneralException(HTTPException):
    def __init__(self, detail: str = "An unexpected error occurred"):
        super().__init__(status_code=500, detail=detail)
        
       
class ValidationException(HTTPException):
    def __init__(self, detail: str):
        detail = clean_text(detail)
        super().__init__(status_code=422, detail=detail)