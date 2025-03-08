from datetime import datetime
from pydantic import BaseModel


class NameSuggestionDto(BaseModel):
    id: int
    name: str
    created: datetime
