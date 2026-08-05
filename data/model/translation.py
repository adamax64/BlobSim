from dataclasses import dataclass


# Frozen so composite() values are hashable/immutable, matching SQLAlchemy's composite column guidance.
@dataclass(frozen=True)
class Translation:
    en: str
    hu: str
