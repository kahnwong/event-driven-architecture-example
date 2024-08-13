from pydantic import BaseModel
from sqlmodel import Field
from sqlmodel import SQLModel


# api
class RequestItem(BaseModel):
    request_id: str
    message: str


class ResponseItem(BaseModel):
    success: bool


# database
class Foo(SQLModel, table=True):
    request_id: str = Field(primary_key=True, unique=True, index=True)
    message: str
    progress: int = 0  # from 0-100
    is_done: bool = False
