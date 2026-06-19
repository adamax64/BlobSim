"""add adventure related type values

Revision ID: 695abcd5cbfa
Revises: ae67c2864c47
Create Date: 2026-06-15 22:02:40.666818

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '695abcd5cbfa'
down_revision: Union[str, None] = 'ae67c2864c47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('ALTER TYPE "BCS".activitytype ADD VALUE IF NOT EXISTS \'ADVENTURE\';')
    op.execute('ALTER TYPE "BCS".traittype ADD VALUE IF NOT EXISTS \'ADVENTUROUS\';')


def downgrade() -> None:
    pass
