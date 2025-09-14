"""add news table

Revision ID: 2b79abfa62a2
Revises: e4a15851f853
Create Date: 2025-09-14 17:42:01.821656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b79abfa62a2'
down_revision: Union[str, None] = 'e4a15851f853'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    newstype = sa.Enum(
        'BLOB_CREATED',
        'BLOB_IN_CREATION',
        'BLOB_TERMINATED',
        'EVENT_STARTED',
        'ONGOING_EVENT',
        'EVENT_ENDED',
        'SEASON_ENDED',
        'ROOKIE_OF_THE_YEAR',
        'NEW_SEASON',
        'NEW_GRANDMASTER',
        name='newstype',
        schema='BCS'
    )

    op.create_table(
        'news',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.BigInteger(), nullable=False),
        sa.Column('news_type', newstype, nullable=False),
        sa.Column('news_data', sa.ARRAY(sa.String), nullable=False),
        schema="BCS"
    )


def downgrade() -> None:
    op.drop_table('news', schema="BCS")
