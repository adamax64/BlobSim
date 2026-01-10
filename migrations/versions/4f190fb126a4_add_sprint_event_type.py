"""add sprint event type

Revision ID: 4f190fb126a4
Revises: 9f8e7d6c5b4a
Create Date: 2025-12-25 11:50:18.446720

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4f190fb126a4'
down_revision: Union[str, None] = '9f8e7d6c5b4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('ALTER TYPE "BCS".eventtype ADD VALUE IF NOT EXISTS \'SPRINT_RACE\';')

    # Update the check constraint to include SPRINT_RACE
    op.drop_constraint('ck_records_event_type', 'records', schema='BCS')
    op.create_check_constraint(
        'ck_records_event_type',
        'records',
        (
            "event_type IN ("
            "'QUARTERED_ONE_SHOT_SCORING', "
            "'QUARTERED_TWO_SHOT_SCORING', "
            "'ENDURANCE_RACE', "
            "'SPRINT_RACE', "
            "'ELIMINATION_SCORING'"
            ")"
        ),
        schema='BCS'
    )


def downgrade() -> None:
    # Restore the constraint without SPRINT_RACE
    op.drop_constraint('ck_records_event_type', 'records', schema='BCS')
    op.create_check_constraint(
        'ck_records_event_type',
        'records',
        (
            "event_type IN ("
            "'QUARTERED_ONE_SHOT_SCORING', "
            "'QUARTERED_TWO_SHOT_SCORING', "
            "'ENDURANCE_RACE', "
            "'ELIMINATION_SCORING'"
            ")"
        ),
        schema='BCS'
    )
    # Note: We cannot remove the enum value 'SPRINT_RACE' from PostgreSQL enum types
