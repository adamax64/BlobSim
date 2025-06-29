from alembic.config import Config
from alembic import command

from data.db.db_engine import DB_URL


def startup():    # Apply database migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", DB_URL)
    command.upgrade(alembic_cfg, "head")
