"""remove incorrect news

Revision ID: 70f65e7261db
Revises: g2b3c4d5e6f7
Create Date: 2025-10-25 10:01:59.808715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70f65e7261db'
down_revision: Union[str, None] = 'g2b3c4d5e6f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove any NEW_GRANDMASTER news whose computed season is not divisible by 4.
    # Season calculation in the app: season = int(date / CYCLES_PER_SEASON) + 1
    # CYCLES_PER_SEASON = EPOCHS_PER_SEASON * CYCLES_PER_EPOCH = 32 * 4 = 128
    op.execute(
        sa.text(
            "DELETE FROM \"BCS\".news WHERE news_type = 'NEW_GRANDMASTER' AND ((date / 128) + 1) % 4 != 0"
        )
    )


def downgrade() -> None:
    pass
