from pydantic import BaseModel, ConfigDict

from domain.dtos.standings_dtos.standings_result_dto import StandingsResultDTO


class StandingsDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    blob_id: int
    name: str
    color: str
    is_contract_ending: bool
    is_rookie: bool
    results: list[StandingsResultDTO]
    num_of_rounds: int
    total_points: int
