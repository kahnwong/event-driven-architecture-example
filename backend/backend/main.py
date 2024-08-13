import os

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
from backend.transcribe.get import transcribe_to_text
from backend.transcribe.request import transcribe_request
from backend.transcribe.status import transcribe_status
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

    # submit task
    operation_name = transcribe_request(
        request_id=request.request_id, gcs_uri=request.gcs_uri
    )

    # write data to db
    item = Foo(
        request_id=request.request_id,
        gcs_uri=request.gcs_uri,
        operation_name=operation_name,
    )

    session.add(item)
    session.commit()
    session.refresh(item)

    # # submit task
    # r = requests.post(
    #     url=os.getenv("WORKER_API_ENDPOINT"),
    #     headers={"X-API-Key": os.getenv("WORKER_API_KEY")},
    #     data=json.dumps(request.model_dump()),
    # )
    # assert r.status_code == 200

    return SubmitResponseItem(request_id=request.request_id, success=True)


@app.post("/status", response_model=StatusResponseItem)
async def status_polling(
    *,
    request: StatusRequestItem,
    session: Session = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> StatusResponseItem:
    logger.info(f"/status - request_id: {request.request_id}")

    # query
    query = select(Foo).where(Foo.request_id == request.request_id)
    item = session.exec(query).first()

    item.progress = transcribe_status(operation_name=item.operation_name)  # type: ignore

    # extract response if done
    if (item.progress == 100) & (item.transcript == ""):  # type: ignore
        item.transcript = transcribe_to_text(  # type: ignore
            operation_name=item.operation_name, gcs_uri=item.gcs_uri  # type: ignore
        )

    # update db
    session.add(item)
    session.commit()
    session.refresh(item)

    return StatusResponseItem(
        request_id=request.request_id, progress=item.progress  # type: ignore
    )
