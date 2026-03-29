from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

def success_response(message: str, data=None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    #把任何FastAPI，Pydantic,ORM对象，正常响应，
    return JSONResponse(content=jsonable_encoder(content))

