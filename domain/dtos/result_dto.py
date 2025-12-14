from pydantic import BaseModel

from domain.dtos.blob_stats_dto import BlobStatsDto


class ResultDto(BaseModel):
    blob: BlobStatsDto
    position: int
    points: int
