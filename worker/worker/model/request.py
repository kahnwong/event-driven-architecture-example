from pydantic import BaseModel


class RequestItem(BaseModel):
    request_id: str
    message: str
