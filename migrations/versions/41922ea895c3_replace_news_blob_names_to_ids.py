"""replace news blob names to ids

Revision ID: 41922ea895c3
Revises: b29cb7236949
Create Date: 2025-10-10 18:06:31.294708

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '41922ea895c3'
down_revision: Union[str, None] = 'b29cb7236949'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _find_blob_id_by_full_name(connection, full_name: str):
    parts = full_name.split(' ', 1)
    if len(parts) == 0:
        return None
    first = parts[0]
    last = parts[1] if len(parts) > 1 else ''
    # try exact match on first and last
    res = connection.execute(
        text(
            'SELECT id FROM "BCS".blobs '
            'WHERE first_name = :first AND last_name = :last LIMIT 1'
        ),
        {'first': first, 'last': last}
    ).fetchone()
    if res:
        return res[0]
    # try last token as last name if name had more than two words
    if ' ' in full_name:
        toks = full_name.split()
        first = toks[0]
        last = toks[-1]
        res = connection.execute(
            text(
                'SELECT id FROM "BCS".blobs '
                'WHERE first_name = :first AND last_name = :last LIMIT 1'
            ),
            {'first': first, 'last': last}
        ).fetchone()
        if res:
            return res[0]
    return None


def upgrade() -> None:
    conn = op.get_bind()
    # use mappings() so each row can be accessed by column name (dict-like)
    news_rows = conn.execute(
        text('SELECT id, news_type, news_data FROM "BCS".news')
    ).mappings().all()

    for row in news_rows:
        nid = row['id']
        ntype = row['news_type']
        # make a mutable copy of news_data; if it's NULL or not a sequence, use empty list
        raw_data = row['news_data']
        data = list(raw_data) if raw_data is not None else []
        changed = False

        try:
            if ntype in ('BLOB_CREATED', 'BLOB_TERMINATED', 'NEW_GRANDMASTER') and len(data) >= 1:
                if isinstance(data[0], str):
                    blob_id = _find_blob_id_by_full_name(conn, data[0])
                else:
                    blob_id = None
                if blob_id is not None:
                    data[0] = str(blob_id)
                    changed = True

            elif ntype == 'EVENT_ENDED' and len(data) >= 5:
                # data: [leagueName, round, first, second, third]
                for idx in (2, 3, 4):
                    if idx < len(data) and isinstance(data[idx], str):
                        blob_id = _find_blob_id_by_full_name(conn, data[idx])
                        if blob_id is not None:
                            data[idx] = str(blob_id)
                            changed = True

            elif ntype == 'SEASON_ENDED' and len(data) >= 2:
                # data: [leagueName, winner]
                if len(data) > 1 and isinstance(data[1], str):
                    blob_id = _find_blob_id_by_full_name(conn, data[1])
                    if blob_id is not None:
                        data[1] = str(blob_id)
                        changed = True

            elif ntype == 'ROOKIE_OF_THE_YEAR' and len(data) >= 1:
                if len(data) > 0 and isinstance(data[0], str):
                    blob_id = _find_blob_id_by_full_name(conn, data[0])
                    if blob_id is not None:
                        data[0] = str(blob_id)
                        changed = True

            elif ntype == 'NEW_SEASON' and len(data) >= 1:
                # data format:
                # [season, league_count,
                #  for each league: leagueName, blobs_count, *blob_names...,
                #  ..., retired_count, *retired_names..., rookies_count, *rookie_names...]
                # we'll parse accordingly
                idx = 1
                if idx >= len(data):
                    pass
                else:
                    league_num = int(data[idx])
                    for _ in range(league_num):
                        idx += 1
                        # league name
                        if idx >= len(data):
                            break
                        # league = data[idx]
                        idx += 1
                        if idx >= len(data):
                            break
                        blobs_num = int(data[idx])
                        for _ in range(blobs_num):
                            idx += 1
                            if idx >= len(data):
                                break
                            if isinstance(data[idx], str):
                                blob_id = _find_blob_id_by_full_name(conn, data[idx])
                                if blob_id is not None:
                                    data[idx] = str(blob_id)
                                    changed = True
                    # after transfers, retired
                    idx += 1
                    if idx < len(data):
                        retired_num = int(data[idx])
                        for _ in range(retired_num):
                            idx += 1
                            if idx >= len(data):
                                break
                            if isinstance(data[idx], str):
                                blob_id = _find_blob_id_by_full_name(conn, data[idx])
                                if blob_id is not None:
                                    data[idx] = str(blob_id)
                                    changed = True
                    # rookies
                    idx += 1
                    if idx < len(data):
                        rookies_num = int(data[idx])
                        for _ in range(rookies_num):
                            idx += 1
                            if idx >= len(data):
                                break
                            if isinstance(data[idx], str):
                                blob_id = _find_blob_id_by_full_name(conn, data[idx])
                                if blob_id is not None:
                                    data[idx] = str(blob_id)
                                    changed = True
        except Exception:
            # keep going on error for a row
            continue

        if changed:
            conn.execute(text('UPDATE "BCS".news SET news_data = :data WHERE id = :id'), {'data': data, 'id': nid})


def downgrade() -> None:
    # This migration is not reversible automatically
    pass
