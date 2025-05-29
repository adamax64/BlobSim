from datetime import datetime
from pydantic import BaseModel


class NameSuggestionDto(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str
    created: datetime
    parent_id: int | None = None
