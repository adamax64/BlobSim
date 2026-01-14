"""add champions and grandmasters table

Revision ID: bd5c2e512c10
Revises: 4f190fb126a4
Create Date: 2026-01-02 12:09:10.010920

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bd5c2e512c10"
down_revision: Union[str, None] = "4f190fb126a4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# IMPORTANT! The queries that initially populate the champions and grandmasters
# tables add records for the current incomplete season/eon. These records are
# then deleted to ensure that only complete seasons/eons are represented in
# the tables. This approach assumes that the migration is run at a time when
# the current season/eon is not yet complete and there are data for the current incomplete season/eon.
# If the migration is run at the start of a new season/eon, the most recent valid records will be deleted!
# In this case, add the necessary data for the current season/eon manually after running the migration.
def upgrade() -> None:
    # Ensure event dates are set for old events which were added in the initial data populating migration.
    op.execute('UPDATE "BCS".events SET date = 27 WHERE id = 1;')
    op.execute('UPDATE "BCS".events SET date = 55 WHERE id = 2;')
    op.execute('UPDATE "BCS".events SET date = 87 WHERE id = 3;')
    op.execute('UPDATE "BCS".events SET date = 115 WHERE id = 4;')
    op.execute('UPDATE "BCS".events SET date = 155 WHERE id = 5;')
    op.execute('UPDATE "BCS".events SET date = 183 WHERE id = 6;')
    op.execute('UPDATE "BCS".events SET date = 215 WHERE id = 7;')
    op.execute('UPDATE "BCS".events SET date = 243 WHERE id = 8;')

    # Create a physical table `BCS.champions` and populate it with the
    # champion (highest total points) per league per season. Season is
    # computed as (event date / 128) + 1. Exclude events with NULL date.
    op.execute('DROP TABLE IF EXISTS "BCS".champions;')
    op.execute(
        """
    CREATE TABLE "BCS".champions AS
    WITH totals AS (
        SELECT
            e.league_id,
            ((e.date / 128) + 1) AS season,
            r.blob_id,
            SUM(COALESCE(r.points, 0)) AS points
        FROM "BCS".results r
        JOIN "BCS".events e ON r.event_id = e.id
        WHERE e.date IS NOT NULL
        GROUP BY e.league_id, ((e.date / 128) + 1), r.blob_id
    )
    SELECT league_id, season, blob_id
    FROM (
        SELECT t.*, ROW_NUMBER() OVER (PARTITION BY league_id, season ORDER BY points DESC, blob_id) AS rn
        FROM totals t
    ) s
    WHERE rn = 1;
    """
    )

    # Remove all champions rows that have the maximal season value.
    # This deletes every champion record where `season` equals the
    # current maximum season present in the table.
    op.execute(
        """
    DELETE FROM "BCS".champions c
    WHERE c.season = (
        SELECT MAX(season) FROM "BCS".champions
    );
    """
    )

    # Add foreign-key constraints for `champions` to reference `blobs` and `leagues`.
    op.execute(
        'ALTER TABLE "BCS".champions ADD CONSTRAINT champions_blob_fk FOREIGN KEY (blob_id) REFERENCES "BCS".blobs(id);'
    )
    op.execute(
        'ALTER TABLE "BCS".champions ADD CONSTRAINT champions_league_fk FOREIGN KEY (league_id) REFERENCES "BCS".leagues(id);'
    )

    # Create grandmasters table: one grandmaster per eon (4 seasons)
    # Determine top league per eon (most championships in those 4 seasons),
    # then pick the blob in that league with most championships; tiebreakers:
    # most wins (1st places), most seconds, most thirds, most points in that eon.
    op.execute('DROP TABLE IF EXISTS "BCS".grandmasters;')
    op.execute(
        """
    CREATE TABLE "BCS".grandmasters AS
    WITH champs AS (
        SELECT league_id, season, blob_id, ((season - 1) / 4) + 1 AS eon
        FROM "BCS".champions
    ),
    -- Only consider champions from top-level leagues (level = 1)
    top_level_champs AS (
        SELECT c.*
        FROM champs c
        JOIN "BCS".leagues l ON c.league_id = l.id
        WHERE l.level = 1
    ),
    blob_stats AS (
        SELECT
            tlc.eon,
            tlc.blob_id,
            COUNT(*) AS championships,
            COALESCE(SUM(CASE WHEN r.position = 1 THEN 1 ELSE 0 END), 0) AS wins,
            COALESCE(SUM(CASE WHEN r.position = 2 THEN 1 ELSE 0 END), 0) AS seconds,
            COALESCE(SUM(CASE WHEN r.position = 3 THEN 1 ELSE 0 END), 0) AS thirds,
            COALESCE(SUM(COALESCE(r.points, 0)), 0) AS points
        FROM top_level_champs tlc
        LEFT JOIN "BCS".events e2 ON ((e2.date / 128) + 1) BETWEEN ((tlc.eon - 1) * 4 + 1) AND (tlc.eon * 4)
            AND e2.league_id = tlc.league_id
        LEFT JOIN "BCS".results r ON r.event_id = e2.id AND r.blob_id = tlc.blob_id
        GROUP BY tlc.eon, tlc.league_id, tlc.blob_id
    )
    SELECT eon, blob_id
    FROM (
        SELECT bs.*, ROW_NUMBER() OVER (
            PARTITION BY eon
            ORDER BY championships DESC, wins DESC, seconds DESC, thirds DESC, points DESC, blob_id
        ) AS rn
        FROM blob_stats bs
    ) t
    WHERE rn = 1;
    """
    )

    # Remove the single grandmasters row with the maximal eon (tie-broken
    # by blob_id) to delete the latest grandmaster record.
    op.execute(
        """
    DELETE FROM "BCS".grandmasters g
    WHERE g.eon = (
        SELECT MAX(eon) FROM "BCS".grandmasters
    );
    """
    )

    # Add foreign-key constraint for `grandmasters` to reference `blobs`.
    op.execute(
        'ALTER TABLE "BCS".grandmasters ADD CONSTRAINT grandmasters_blob_fk FOREIGN KEY (blob_id) REFERENCES "BCS".blobs(id);'
    )


def downgrade() -> None:
    # Revert the event date changes applied in upgrade
    op.execute('UPDATE "BCS".events SET date = NULL WHERE id = 1;')
    op.execute('UPDATE "BCS".events SET date = NULL WHERE id = 2;')
    op.execute('UPDATE "BCS".events SET date = NULL WHERE id = 3;')
    op.execute('UPDATE "BCS".events SET date = NULL WHERE id = 4;')
    op.execute('UPDATE "BCS".events SET date = NULL WHERE id = 5;')
    op.execute('UPDATE "BCS".events SET date = NULL WHERE id = 6;')
    op.execute('UPDATE "BCS".events SET date = NULL WHERE id = 7;')
    op.execute('UPDATE "BCS".events SET date = NULL WHERE id = 8;')
    # Drop the physical table
    op.execute('DROP TABLE IF EXISTS "BCS".champions;')
    op.execute('DROP TABLE IF EXISTS "BCS".grandmasters;')
