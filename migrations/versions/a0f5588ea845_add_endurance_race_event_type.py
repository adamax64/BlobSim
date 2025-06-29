"""Add endurance race event type

Revision ID: a0f5588ea845
Revises: d63686c84980
Create Date: 2025-06-29 16:48:16.017791

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'a0f5588ea845'
down_revision: Union[str, None] = 'd63686c84980'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE \"BCS\".eventtype ADD VALUE IF NOT EXISTS 'ENDURANCE_RACE'")


def downgrade() -> None:
    op.execute("ALTER TYPE \"BCS\".eventtype DROP VALUE IF EXISTS 'ENDURANCE_RACE'")
