import sys
from alembic.config import Config
from alembic import command

from data.db.db_engine import DEBUG_DB_URL, PROD_DB_URL


def startup():
    is_debug = "debug" in sys.argv
    # Apply database migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", DEBUG_DB_URL if is_debug else PROD_DB_URL)
    command.upgrade(alembic_cfg, "head")
