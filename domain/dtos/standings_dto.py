from typing import List
from dataclasses import dataclass

from domain.dtos.standings_result_dto import StandingsResultDTO


@dataclass
class StandingsDTO:
    blob_id: int
    name: str
    results: List[StandingsResultDTO]
    total_points: int
