# FastAPI
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

# Database
from time import time
from datetime import datetime

router = APIRouter()


@router.get("/",status_code=status.HTTP_200_OK)
def healthcheck():
    
    """Healthcheck service"""
    
    start = time()
    date = None
    
    try:
        date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        if not date:
            raise Exception('Container internal error')
    except Exception as e:
        content = {"error": str(e)}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            content=content)
    
    response_time = time() - start
    content = {"server_date": date, "response_time": response_time}
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)