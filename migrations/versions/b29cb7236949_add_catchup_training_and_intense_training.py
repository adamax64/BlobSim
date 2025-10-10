"""add catchup training and intense training enum values

Revision ID: b29cb7236949
Revises: 8c5b132a3815
Create Date: 2025-10-10 13:51:13.006442

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b29cb7236949'
down_revision: Union[str, None] = '8c5b132a3815'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('ALTER TYPE "BCS".eventtype ADD VALUE IF NOT EXISTS \'CATCHUP_TRAINING\';')
    op.execute('ALTER TYPE "BCS".activitytype ADD VALUE IF NOT EXISTS \'INTENSE_TRAINING\';')


def downgrade() -> None:
    pass
