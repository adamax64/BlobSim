"""add administration activity type

Revision ID: 3f7a9b1c2d4e
Revises: af12b3c4d5e6
Create Date: 2025-12-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '3f7a9b1c2d4e'
down_revision: Union[str, None] = 'af12b3c4d5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add ADMINISTRATION enum value to activitytype
    op.execute('ALTER TYPE "BCS".activitytype ADD VALUE IF NOT EXISTS \'ADMINISTRATION\';')


def downgrade() -> None:
    # Removing enum values in PostgreSQL is non-trivial and not implemented here.
    pass
