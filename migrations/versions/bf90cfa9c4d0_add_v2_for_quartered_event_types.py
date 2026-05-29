"""add v2 for quartered event types

Revision ID: bf90cfa9c4d0
Revises: 50ea619ed710
Create Date: 2026-05-29 17:31:41.929047

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bf90cfa9c4d0"
down_revision: Union[str, None] = "50ea619ed710"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TYPE \"BCS\".eventtype ADD VALUE IF NOT EXISTS 'QUARTERED_ONE_SHOT_SCORING_V2';"
    )
    op.execute(
        "ALTER TYPE \"BCS\".eventtype ADD VALUE IF NOT EXISTS 'QUARTERED_TWO_SHOT_SCORING_V2';"
    )
    # Commit the DDL so new enum values are visible for subsequent updates
    op.execute("COMMIT;")
    op.execute("BEGIN;")

    op.execute(
        "UPDATE \"BCS\".calendar SET event_type = 'QUARTERED_ONE_SHOT_SCORING_V2' WHERE event_type = 'QUARTERED_ONE_SHOT_SCORING' AND concluded = FALSE;"
    )
    op.execute(
        "UPDATE \"BCS\".calendar SET event_type = 'QUARTERED_TWO_SHOT_SCORING_V2' WHERE event_type = 'QUARTERED_TWO_SHOT_SCORING' AND concluded = FALSE;"
    )

    # Drop constraint since the enum values are checked anyway through the field type
    op.drop_constraint("ck_records_event_type", "records", schema="BCS")
    op.execute(
        "UPDATE \"BCS\".records SET event_type = 'QUARTERED_ONE_SHOT_SCORING_V2' WHERE event_type = 'QUARTERED_ONE_SHOT_SCORING';"
    )
    op.execute(
        "UPDATE \"BCS\".records SET event_type = 'QUARTERED_TWO_SHOT_SCORING_V2' WHERE event_type = 'QUARTERED_TWO_SHOT_SCORING';"
    )


def downgrade() -> None:
    op.execute(
        "UPDATE \"BCS\".calendar SET event_type = 'QUARTERED_ONE_SHOT_SCORING' WHERE event_type = 'QUARTERED_ONE_SHOT_SCORING_V2' AND concluded = FALSE;"
    )
    op.execute(
        "UPDATE \"BCS\".calendar SET event_type = 'QUARTERED_TWO_SHOT_SCORING' WHERE event_type = 'QUARTERED_TWO_SHOT_SCORING_V2' AND concluded = FALSE;"
    )

    op.execute(
        "UPDATE \"BCS\".records SET event_type = 'QUARTERED_ONE_SHOT_SCORING' WHERE event_type = 'QUARTERED_ONE_SHOT_SCORING_V2';"
    )
    op.execute(
        "UPDATE \"BCS\".records SET event_type = 'QUARTERED_TWO_SHOT_SCORING' WHERE event_type = 'QUARTERED_TWO_SHOT_SCORING_V2';"
    )
    # Note: We cannot remove enum values from PostgreSQL enum types,
    # so we revert calendar and records rows instead.
