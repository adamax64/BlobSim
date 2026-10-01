from pydantic import BaseModel, ConfigDict

from domain.dtos.translations_dto import TranslationsDto


class LeagueDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: list[TranslationsDto]
    field_size: int
    level: int
