from pydantic import BaseModel, ConfigDict

from domain.dtos.blob_dtos.blob_stats_dto import BlobStatsDto


class TitleCountDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    blob: BlobStatsDto
    count: int


class TitlesCountSummaryDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    grandmasters: list[TitleCountDto]
    championships: list[TitleCountDto]
    top_wins: list[TitleCountDto]
    top_podiums: list[TitleCountDto]
    season_victories: list[TitleCountDto]
    lower_wins: list[TitleCountDto]
    lower_podiums: list[TitleCountDto]
