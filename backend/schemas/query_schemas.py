from pydantic import BaseModel


class Query(BaseModel):
    message: str

