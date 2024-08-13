import json
import os

import requests  # type: ignore
from dotenv import load_dotenv
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Security
from fastapi import status
from fastapi.security import APIKeyHeader
from sqlmodel import select
from sqlmodel import Session

from backend.models import Foo
from backend.models import StatusRequestItem
from backend.models import StatusResponseItem
from backend.models import SubmitRequestItem
from backend.models import SubmitResponseItem
from backend.utils.db import get_session
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
    *,
    request: SubmitRequestItem,
    session: Session = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> SubmitResponseItem:
    logger.info(f"/submit - request_id: {request.request_id}")

    item = Foo(request_id=request.request_id, message=request.message)
    session.add(item)
    session.commit()
    session.refresh(item)

    # submit task
    r = requests.post(
        url=os.getenv("WORKER_API_ENDPOINT"),
        headers={"X-API-Key": os.getenv("WORKER_API_KEY")},
        data=json.dumps(request.model_dump()),
    )
    assert r.status_code == 200

    return SubmitResponseItem(request_id=request.request_id, success=True)


@app.post("/status", response_model=StatusResponseItem)
async def status_polling(
    *,
    request: StatusRequestItem,
    session: Session = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> StatusResponseItem:
    logger.info(f"/status - request_id: {request.request_id}")

    query = select(Foo).where(Foo.request_id == request.request_id)
    item = session.exec(query).first()

    return StatusResponseItem(
        request_id=request.request_id, progress=item.progress, is_done=item.is_done  # type: ignore
    )
