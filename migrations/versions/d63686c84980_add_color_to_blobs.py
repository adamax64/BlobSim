"""add color to blobs

Revision ID: d63686c84980
Revises:
Create Date: 2024-03-19 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd63686c84980'
down_revision: Union[str, None] = '1aef587a340c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add color column with default value
    op.add_column('blobs', sa.Column('color', sa.String(), nullable=False, server_default='#888888'), schema="BCS")


def downgrade() -> None:
    # Remove color column
    op.drop_column('blobs', 'color', schema="BCS")
