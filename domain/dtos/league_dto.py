from dataclasses import dataclass

from domain.dtos.translations_dto import TranslationsDto


@dataclass
class LeagueDto:
    id: int
    name: list[TranslationsDto]
    field_size: int
    level: int
