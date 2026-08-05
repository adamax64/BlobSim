from data.model.translation import Translation
from domain.dtos.translations_dto import TranslationsDto

DEFAULT_LANGUAGE = "en"


def build_translations_dto(translation: Translation | None) -> list[TranslationsDto]:
    """Map a Translation composite (en, hu) into a list of per-language TranslationsDto entries."""
    if translation is None:
        return []
    return [
        TranslationsDto(language="en", text=translation.en),
        TranslationsDto(language="hu", text=translation.hu),
    ]


def get_translation_text(translations: list[TranslationsDto], language: str = DEFAULT_LANGUAGE) -> str:
    """Resolve the text for the given language, falling back to the default language, then the first entry."""
    for translation in translations:
        if translation.language == language:
            return translation.text
    for translation in translations:
        if translation.language == DEFAULT_LANGUAGE:
            return translation.text
    return translations[0].text if translations else ""
