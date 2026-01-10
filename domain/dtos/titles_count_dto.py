from dataclasses import dataclass

from domain.dtos.blob_stats_dto import BlobStatsDto


@dataclass
class TitleCountDto:
    blob: BlobStatsDto
    count: int


@dataclass
class TitlesCountSummaryDto:
    grandmasters: list[TitleCountDto]
    championships: list[TitleCountDto]
    top_wins: list[TitleCountDto]
    top_podiums: list[TitleCountDto]
    season_victories: list[TitleCountDto]
    lower_wins: list[TitleCountDto]
    lower_podiums: list[TitleCountDto]
