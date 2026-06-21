"""add pre event item state types

Revision ID: d4e5f6a7b8c9
Revises: 695abcd5cbfa
Create Date: 2026-06-19 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, None] = '695abcd5cbfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        'ALTER TYPE "BCS".statetype ADD VALUE IF NOT EXISTS \'COOKIE_BOOST\';'
    )
    op.execute(
        'ALTER TYPE "BCS".statetype ADD VALUE IF NOT EXISTS \'ENERGY_CELL_BOOST\';'
    )
    op.execute(
        'ALTER TYPE "BCS".statetype ADD VALUE IF NOT EXISTS \'CACHE_BOOST\';'
    )
    op.execute(
        'ALTER TYPE "BCS".statetype ADD VALUE IF NOT EXISTS \'POWER_BANK_BOOST\';'
    )
    op.execute(
        'ALTER TYPE "BCS".statetype ADD VALUE IF NOT EXISTS \'OVERCLOCKING_DEVICE_BOOST\';'
    )


def downgrade() -> None:
    pass
