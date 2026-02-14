"""add INTENSE_PRACTICE to activitytype enum

Revision ID: h7f8e9d6c5b4
Revises: h3c4d5e6f7g8
Create Date: 2026-02-14 00:00:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "h7f8e9d6c5b4"
down_revision = "h3c4d5e6f7g8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new value to the existing ENUM type in Postgres
    op.execute(
        "ALTER TYPE \"BCS\".activitytype ADD VALUE IF NOT EXISTS 'INTENSE_PRACTICE';"
    )


def downgrade() -> None:
    # Removing a value from a PostgreSQL enum is non-trivial and not supported here.
    pass
