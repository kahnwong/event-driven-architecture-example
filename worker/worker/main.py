import os
from time import sleep

from dotenv import load_dotenv
from fastapi import BackgroundTasks
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Security
from fastapi import status
from fastapi.security import APIKeyHeader
from sqlmodel import select
from sqlmodel import Session

from worker.models import Foo
from worker.models import RequestItem
from worker.models import ResponseItem
from worker.utils.db import create_postgres_engine
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


@app.post("/", response_model=ResponseItem)
async def main(
    request: RequestItem,
    background_tasks: BackgroundTasks,
    api_key: str = Security(get_api_key),
) -> ResponseItem:
    logger.info(f"request_id: {request.request_id}")

    background_tasks.add_task(func=task, request_id=request.request_id)

    return ResponseItem(success=True)


def task(request_id: str):
    session = Session(create_postgres_engine())
    query = select(Foo).where(Foo.request_id == request_id)
    item = session.exec(query).first()

    # update progress
    for i in range(4):
        sleep(1)

        item.progress += 25  # type: ignore
        logger.info(item)

        session.add(item)
        session.commit()
        session.refresh(item)

    # mark as done
    item = session.exec(query).first()
    if item.progress == 100:  # type: ignore
        item.is_done = True  # type: ignore

        session.add(item)
        session.commit()
        session.refresh(item)
