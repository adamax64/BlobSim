"""add current activity to blob

Revision ID: e4a15851f853
Revises: 9316047c307c
Create Date: 2025-09-07 10:09:55.323934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4a15851f853'
down_revision: Union[str, None] = '9316047c307c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the new ENUM type for activitytype
    activity_type_enum = sa.Enum(
        'EVENT', 'MAINTENANCE', 'PRACTICE', 'LABOUR', 'IDLE',
        name='activitytype', schema='BCS'
    )
    activity_type_enum.create(op.get_bind(), checkfirst=True)

    # Add the new column to the blobs table
    op.add_column(
        'blobs',
        sa.Column(
            'current_activity',
            activity_type_enum,
            server_default='IDLE',
            nullable=False
        ),
        schema='BCS'
    )


def downgrade() -> None:
    # Drop the current_activity column from the blobs table
    op.drop_column('blobs', 'current_activity', schema='BCS')
