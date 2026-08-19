from pydantic import BaseModel

from domain.dtos.blob_dtos.blob_stats_dto import BlobStatsDto
from domain.dtos.sim_time_dto import SimTimeDto


class MineWinnerDto(BaseModel):
    date: SimTimeDto
    blob: BlobStatsDto
    amount: int


class MineWinnersDto(BaseModel):
    winners: list[MineWinnerDto]
