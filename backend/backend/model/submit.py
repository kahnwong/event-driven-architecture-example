from pydantic import BaseModel


class SubmitRequestItem(BaseModel):
    request_id: str
    message: str


class SubmitResponseItem(BaseModel):
    request_id: str
    success: bool
