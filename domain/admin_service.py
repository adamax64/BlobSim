from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.persistence.admin_settings_repository import (
    get_enabled_cronjobs as repository_get_enabled_cronjobs,
    set_enabled_cronjobs as repository_set_enabled_cronjobs,
)


@transactional
def get_enabled_cronjobs(session: Session) -> bool:
    return repository_get_enabled_cronjobs(session)


@transactional
def set_enabled_cronjobs(session: Session, enabled: bool) -> None:
    return repository_set_enabled_cronjobs(session, enabled)
