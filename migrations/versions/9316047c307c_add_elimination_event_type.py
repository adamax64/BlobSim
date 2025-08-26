"""add elimination event type

Revision ID: 9316047c307c
Revises: 78b8fc369578
Create Date: 2025-08-26 18:12:59.099804

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9316047c307c'
down_revision: Union[str, None] = '78b8fc369578'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('ALTER TYPE "BCS".eventtype ADD VALUE IF NOT EXISTS \'ELIMINATION_SCORING\';')


def downgrade() -> None:
    pass
