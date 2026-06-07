"""add premium practice activity type

Revision ID: 9e1448823996
Revises: bf90cfa9c4d0
Create Date: 2026-06-07 18:08:26.293497

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9e1448823996"
down_revision: Union[str, None] = "bf90cfa9c4d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TYPE \"BCS\".activitytype ADD VALUE IF NOT EXISTS 'PREMIUM_PRACTICE';"
    )


def downgrade() -> None:
    # Removing enum values in PostgreSQL is non-trivial and not implemented here.
    pass
