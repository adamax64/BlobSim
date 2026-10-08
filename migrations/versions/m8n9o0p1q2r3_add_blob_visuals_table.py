"""add blob_visuals table

Revision ID: m8n9o0p1q2r3
Revises: l7m8n9o0p1q2
Create Date: 2026-08-24 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "m8n9o0p1q2r3"
down_revision: Union[str, None] = "l7m8n9o0p1q2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the blob_appearances table
    op.create_table(
        "blob_appearances",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "blob_id", sa.Integer(), sa.ForeignKey("BCS.blobs.id"), nullable=False
        ),
        sa.Column(
            "appearance_type",
            sa.Enum(
                "SOLID", "BICOLOR", "TRICOLOR", name="appearance_type_dbo", schema="BCS"
            ),
            nullable=False,
            server_default="SOLID",
        ),
        sa.Column("colors", sa.ARRAY(sa.String), nullable=False),
        sa.Column("params", sa.ARRAY(sa.String), nullable=False),
        sa.UniqueConstraint("blob_id", name="unique_blob_appearances_blob_id"),
        schema="BCS",
    )

    # Populate blob_appearances for existing blobs with SOLID type and their current color
    op.execute("""
        INSERT INTO "BCS".blob_appearances (blob_id, appearance_type, colors, params)
        SELECT id, 'SOLID'::"BCS".appearance_type_dbo,
               ARRAY[COALESCE(NULLIF(color, ''), '#888888')],
               '{}'
        FROM "BCS".blobs
        """)

    op.drop_column("blobs", "color", schema="BCS")


def downgrade() -> None:
    # Remove the blob_appearances table
    op.drop_table("blob_appearances", schema="BCS")
    op.execute('DROP TYPE IF EXISTS "BCS".appearance_type_dbo')
    op.add_column(
        "blobs",
        sa.Column("color", sa.String(), nullable=False, server_default="#888888"),
        schema="BCS",
    )
