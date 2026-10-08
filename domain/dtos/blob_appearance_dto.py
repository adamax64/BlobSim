from pydantic import BaseModel, ConfigDict

from domain.enums.appearance_type_dto import AppearanceTypeDto


class BlobAppearanceDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    appearance_type: AppearanceTypeDto = AppearanceTypeDto.SOLID
    colors: list[str] = []
    params: list[str] = []
