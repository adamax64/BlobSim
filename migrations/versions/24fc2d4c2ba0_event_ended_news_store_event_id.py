"""event ended news store event id

Revision ID: 24fc2d4c2ba0
Revises: 70f65e7261db
Create Date: 2025-12-14 17:45:47.999742

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '24fc2d4c2ba0'
down_revision: Union[str, None] = '70f65e7261db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    # select all news rows so we can transform EVENT_ENDED entries
    news_rows = conn.execute(
        text('SELECT id, date, news_type, news_data FROM "BCS".news WHERE news_type = :nt'),
        {'nt': 'EVENT_ENDED'}
    ).mappings().all()

    for row in news_rows:
        nid = row['id']
        raw = row['news_data']
        data = list(raw) if raw is not None else []

        # preserve first and second values (leagueName and round)
        first = data[0] if len(data) > 0 else ''
        second = data[1] if len(data) > 1 else ''

        # find event with the same date as the news; migration assumes one exists
        ev = conn.execute(
            text('SELECT id FROM "BCS".events WHERE date = :date LIMIT 1'),
            {'date': row['date']}
        ).fetchone()
        if ev is None:
            raise Exception(f'No event found for news id {nid} with date {row["date"]}')

        event_id = ev[0]

        new_data = [first, second, str(event_id)]

        conn.execute(
            text('UPDATE "BCS".news SET news_data = :data WHERE id = :id'),
            {'data': new_data, 'id': nid}
        )


def downgrade() -> None:
    # No downgrade possible
    pass
