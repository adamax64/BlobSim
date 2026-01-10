from dataclasses import dataclass

from domain.dtos.blob_stats_dto import BlobStatsDto
from domain.dtos.league_dto import LeagueDto


@dataclass
class ChampionDto:
    season: int
    blob: BlobStatsDto


@dataclass
class LeagueChampionsDto:
    league: LeagueDto
    champions: list[ChampionDto]


@dataclass
class GrandmasterDto:
    eon: int
    blob: BlobStatsDto


@dataclass
class TitlesChronologyDto:
    league_champions: list[LeagueChampionsDto]
    grandmasters: list[GrandmasterDto]
