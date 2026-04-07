from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.admin_settings import AdminSettings


@transactional
def get_enabled_cronjobs(session: Session) -> bool:
    setting = session.query(AdminSettings).first()
    return setting.enable_cronjobs if setting else False


@transactional
def set_enabled_cronjobs(session: Session, enabled: bool) -> None:
    setting = session.query(AdminSettings).first()
    if setting:
        setting.enable_cronjobs = enabled
    else:
        setting = AdminSettings(enable_cronjobs=enabled)
        session.add(setting)
    session.commit()
