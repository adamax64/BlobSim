"""Add records table

Revision ID: f1a2b3c4d5e6
Revises: 41922ea895c3
Create Date: 2025-01-04 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f1a2b3c4d5e6'
down_revision: Union[str, None] = '41922ea895c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('records',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('league_id', sa.Integer(), nullable=False),
                    sa.Column(
                        'event_type',
                        sa.String(50),
                        nullable=False
                    ),
                    sa.Column('competitor_id', sa.Integer(), nullable=False),
                    sa.Column('score', sa.Double(), nullable=False),
                    sa.ForeignKeyConstraint(['competitor_id'], ['BCS.blobs.id'], ),
                    sa.ForeignKeyConstraint(['league_id'], ['BCS.leagues.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    schema="BCS"
                    )

    # Add check constraint to ensure event_type values match the enum
    op.create_check_constraint(
        'ck_records_event_type',
        'records',
        (
            "event_type IN ("
            "'QUARTERED_ONE_SHOT_SCORING', "
            "'QUARTERED_TWO_SHOT_SCORING', "
            "'ENDURANCE_RACE', "
            "'ELIMINATION_SCORING', "
            "'CATCHUP_TRAINING'"
            ")"
        ),
        schema='BCS'
    )


def downgrade() -> None:
    op.drop_constraint('ck_records_event_type', 'records', schema='BCS')
    op.drop_table('records', schema="BCS")
