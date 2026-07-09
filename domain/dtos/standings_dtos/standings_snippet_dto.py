from pydantic import BaseModel


class StandingsSnippetDto(BaseModel):
    blob_id: int
    blob_name: str
    blob_color: str
    position: int
    points: int
