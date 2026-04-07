"""add admin settings

Revision ID: b3002bb97150
Revises: h7f8e9d6c5b4
Create Date: 2026-04-07 18:21:15.743596

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b3002bb97150"
down_revision: Union[str, None] = "h7f8e9d6c5b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "admin_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("enable_cronjobs", sa.Boolean(), nullable=False, unique=True),
        sa.PrimaryKeyConstraint("id"),
        schema="BCS",
    )
    op.execute(
        """INSERT INTO "BCS".admin_settings (id, enable_cronjobs) VALUES (1, true);"""
    )


def downgrade() -> None:
    op.drop_table("admin_settings")
