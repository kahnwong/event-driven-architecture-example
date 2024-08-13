from pydantic import BaseModel
from sqlmodel import Field
from sqlmodel import SQLModel


# api
class SubmitRequestItem(BaseModel):
    request_id: str
    gcs_uri: str


class SubmitResponseItem(BaseModel):
    request_id: str
    success: bool


class StatusRequestItem(BaseModel):
    request_id: str


class StatusResponseItem(BaseModel):
    request_id: str
    progress: int


# database
class Foo(SQLModel, table=True):
    request_id: str = Field(primary_key=True, unique=True, index=True)
    gcs_uri: str
    operation_name: str
    progress: int = 0  # from 0-100
    is_done: bool = False
    transcription: str = ""
