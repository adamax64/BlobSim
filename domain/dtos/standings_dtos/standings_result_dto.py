from pydantic import BaseModel, ConfigDict


class StandingsResultDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    position: int
    points: int
    standings_position: int | None = None
    position_change: int | None = None
