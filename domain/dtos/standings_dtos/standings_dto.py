from pydantic import BaseModel, ConfigDict

from domain.dtos.blob_appearance_dto import BlobAppearanceDto
from domain.dtos.standings_dtos.standings_result_dto import StandingsResultDTO


class StandingsDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    blob_id: int
    name: str
    appearance: BlobAppearanceDto
    is_contract_ending: bool
    is_rookie: bool
    results: list[StandingsResultDTO]
    num_of_rounds: int
    total_points: int
    position_change: int | None = None
