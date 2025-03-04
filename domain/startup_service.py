import os
from alembic.config import Config
from alembic import command

from data.db.db_engine import DEBUG_DB_URL, PROD_DB_URL


def startup():
    is_debug = os.environ.get("MODE", "dev") == "dev"
    print(f"INFO  [domain.startup_service.startup] Running in {'debug' if is_debug else 'production'} mode")
    # Apply database migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", DEBUG_DB_URL if is_debug else PROD_DB_URL)
    command.upgrade(alembic_cfg, "head")
