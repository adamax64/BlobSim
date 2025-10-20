"""Populate records from existing action scores

Revision ID: g2b3c4d5e6f7
Revises: f1a2b3c4d5e6
Create Date: 2025-01-04 16:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'g2b3c4d5e6f7'
down_revision: Union[str, None] = 'f1a2b3c4d5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Populate records table with the best scores from actions
    # For each league and event type combination, find the maximum score
    # and create a record entry for it

    connection = op.get_bind()

    # Insert records for quartered events (QUARTERED_ONE_SHOT_SCORING and QUARTERED_TWO_SHOT_SCORING)
    connection.execute(text("""
        INSERT INTO "BCS".records (league_id, event_type, competitor_id, score)
        SELECT DISTINCT ON (e.league_id, e.type)
            e.league_id,
            e.type,
            a.blob_id,
            MAX(unnest_score)
        FROM "BCS".events e
        JOIN "BCS".actions a ON e.id = a.event_id
        CROSS JOIN LATERAL unnest(a.scores) AS unnest_score
        WHERE e.type IN ('QUARTERED_ONE_SHOT_SCORING', 'QUARTERED_TWO_SHOT_SCORING')
        GROUP BY e.league_id, e.type, a.blob_id, unnest_score
        ORDER BY e.league_id, e.type, MAX(unnest_score) DESC
    """))

    # Insert records for elimination events
    connection.execute(text("""
        INSERT INTO "BCS".records (league_id, event_type, competitor_id, score)
        SELECT DISTINCT ON (e.league_id, e.type)
            e.league_id,
            e.type,
            a.blob_id,
            MAX(unnest_score)
        FROM "BCS".events e
        JOIN "BCS".actions a ON e.id = a.event_id
        CROSS JOIN LATERAL unnest(a.scores) AS unnest_score
        WHERE e.type = 'ELIMINATION_SCORING'
        GROUP BY e.league_id, e.type, a.blob_id, unnest_score
        ORDER BY e.league_id, e.type, MAX(unnest_score) DESC
    """))

    # Insert records for endurance races
    connection.execute(text("""
        INSERT INTO "BCS".records (league_id, event_type, competitor_id, score)
        SELECT DISTINCT ON (e.league_id, e.type)
            e.league_id,
            e.type,
            a.blob_id,
            MAX(unnest_score)
        FROM "BCS".events e
        JOIN "BCS".actions a ON e.id = a.event_id
        CROSS JOIN LATERAL unnest(a.scores) AS unnest_score
        WHERE e.type = 'ENDURANCE_RACE'
        GROUP BY e.league_id, e.type, a.blob_id, unnest_score
        ORDER BY e.league_id, e.type, MAX(unnest_score) DESC
    """))


def downgrade() -> None:
    # Remove all records that were populated from actions
    connection = op.get_bind()
    connection.execute(text('DELETE FROM "BCS".records'))
