"""Add speed column to blobs

Revision ID: c3164685596c
Revises: d1429827152b
Create Date: 2025-07-08 20:49:48.247526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3164685596c'
down_revision: Union[str, None] = 'd1429827152b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('blobs', sa.Column('speed', sa.Double(), nullable=True), schema='BCS')
    op.execute('UPDATE "BCS".blobs SET speed = strength')
    op.alter_column('blobs', 'speed', nullable=False, schema='BCS')


def downgrade() -> None:
    op.drop_column('blobs', 'speed', schema='BCS')
