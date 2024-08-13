import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Security
from fastapi import status
from fastapi.security import APIKeyHeader

from worker.model.request import RequestItem
from worker.utils.log import init_logger

logger = init_logger(__name__)
load_dotenv()

app = FastAPI(
    title="worker",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

api_key_header = APIKeyHeader(name="X-API-Key")


def get_api_key(
    api_key_header: str = Security(api_key_header),
) -> str:
    api_keys = [os.getenv("WORKER_API_KEY")]

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


@app.post("/")
async def main(request: RequestItem, api_key: str = Security(get_api_key)):
    print(request)
