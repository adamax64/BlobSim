from pydantic import BaseModel, ConfigDict


class TranslationsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    language: str
    text: str
