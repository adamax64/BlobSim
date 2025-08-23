from dataclasses import dataclass

from domain.dtos.standings_result_dto import StandingsResultDTO


@dataclass
class StandingsDTO:
    blob_id: int
    name: str
    color: str
    is_contract_ending: bool
    is_rookie: bool
    results: list[StandingsResultDTO]
    num_of_rounds: int
    total_points: int
