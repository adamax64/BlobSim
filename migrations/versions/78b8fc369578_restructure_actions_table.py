"""restructure actions table

Revision ID: 78b8fc369578
Revises: c3164685596c
Create Date: 2025-08-19 15:44:53.103465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78b8fc369578'
down_revision: Union[str, None] = 'c3164685596c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create a new temporary table with the new schema
    op.create_table(
        'actions_tmp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('blob_id', sa.Integer, nullable=False),
        sa.Column('event_id', sa.Integer, nullable=False),
        sa.Column('scores', sa.ARRAY(sa.Float), nullable=False),
        schema="BCS"
    )

    # 2. Copy and aggregate data into the new table
    op.execute('''
        INSERT INTO "BCS".actions_tmp (blob_id, event_id, scores)
            SELECT blob_id, event_id, ARRAY_AGG(score ORDER BY id) AS scores
            FROM "BCS".actions
            GROUP BY blob_id, event_id
            ORDER BY event_id
    ''')

    # 3. Drop the old actions table
    op.drop_table('actions', schema="BCS")

    # 4. Rename the new table to actions
    op.rename_table('actions_tmp', 'actions', schema="BCS")


def downgrade() -> None:
    # 1. Recreate the old actions table with score and tick
    op.create_table(
        'actions_old',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('blob_id', sa.Integer, nullable=False),
        sa.Column('event_id', sa.Integer, nullable=False),
        sa.Column('score', sa.Float, nullable=True),
        sa.Column('tick', sa.Integer, nullable=True),
        schema="BCS"
    )

    # 2. Expand scores array back to individual rows (only first score per group for downgrade)
    op.execute('''
        INSERT INTO "BCS".actions_old (blob_id, event_id, score)
        SELECT blob_id, event_id, scores[1]
        FROM "BCS".actions
    ''')

    # 3. Drop the new actions table
    op.drop_table('actions', schema="BCS")

    # 4. Rename actions_old back to actions
    op.rename_table('actions_old', 'actions', schema="BCS")
