from dataclasses import dataclass


@dataclass
class TranslationsDto:
    language: str
    text: str
