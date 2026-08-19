"""add mine_winners json column to sim_data

Revision ID: l7m8n9o0p1q2
Revises: k6l7m8n9o0p1
Create Date: 2026-08-18 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "l7m8n9o0p1q2"
down_revision: Union[str, None] = "k6l7m8n9o0p1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "sim_data",
        sa.Column("mine_winners", sa.JSON(), server_default="[]", nullable=False),
        schema="BCS",
    )


def downgrade() -> None:
    op.drop_column("sim_data", "mine_winners", schema="BCS")
