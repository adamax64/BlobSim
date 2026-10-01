from pydantic import BaseModel, ConfigDict

from domain.dtos.blob_dtos.blob_stats_dto import BlobStatsDto
from domain.dtos.league_dto import LeagueDto


class ChampionDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    season: int
    blob: BlobStatsDto


class LeagueChampionsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    league: LeagueDto
    champions: list[ChampionDto]


class GrandmasterDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    eon: int
    blob: BlobStatsDto


class TitlesChronologyDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    league_champions: list[LeagueChampionsDto]
    grandmasters: list[GrandmasterDto]
