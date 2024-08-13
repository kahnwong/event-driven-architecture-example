import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Security
from fastapi import status
from fastapi.security import APIKeyHeader

from backend.model.submit import SubmitRequestItem
from backend.model.submit import SubmitResponseItem
from backend.utils.log import init_logger

logger = init_logger(__name__)
load_dotenv()

app = FastAPI(
    title="backend",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

api_key_header = APIKeyHeader(name="X-API-Key")


def get_api_key(
    api_key_header: str = Security(api_key_header),
) -> str:
    api_keys = [os.getenv("BACKEND_API_KEY")]

    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


#######################
# routes
#######################
@app.get("/version")
async def root():
    return {"version": "0.1.0"}


@app.post("/submit", response_model=SubmitResponseItem)
async def submit(
    request: SubmitRequestItem, api_key: str = Security(get_api_key)
) -> SubmitResponseItem:
    response = SubmitResponseItem(request_id=request.request_id, success=True)
    return response
