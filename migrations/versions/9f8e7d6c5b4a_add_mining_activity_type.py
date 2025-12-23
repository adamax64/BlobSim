"""add mining activity type

Revision ID: 9f8e7d6c5b4a
Revises: 3f7a9b1c2d4e
Create Date: 2025-12-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '9f8e7d6c5b4a'
down_revision: Union[str, None] = '3f7a9b1c2d4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add MINING enum value to activitytype
    op.execute('ALTER TYPE "BCS".activitytype ADD VALUE IF NOT EXISTS \'MINING\';')


def downgrade() -> None:
    # Removing enum values in PostgreSQL is non-trivial and not implemented here.
    pass
