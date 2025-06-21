from pydantic import BaseModel


class ParentDto(BaseModel):
    name: str
    color: str
