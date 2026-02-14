"""add traits and states tables

Revision ID: h3c4d5e6f7g8
Revises: bd5c2e512c10
Create Date: 2026-02-14 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "h3c4d5e6f7g8"
down_revision = "bd5c2e512c10"
branch_labels = None
depends_on = None


def upgrade():
    traittype = sa.Enum(
        "HARD_WORKING", "DETERMINED", "LAZY", name="traittype", schema="BCS"
    )

    statetype = sa.Enum(
        "INJURED", "TIRED", "GLOOMY", "FOCUSED", name="statetype", schema="BCS"
    )

    op.create_table(
        "traits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "blob_id", sa.Integer(), sa.ForeignKey("BCS.blobs.id"), nullable=False
        ),
        sa.Column("type", traittype, nullable=False),
        schema="BCS",
    )

    op.create_table(
        "states",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "blob_id", sa.Integer(), sa.ForeignKey("BCS.blobs.id"), nullable=False
        ),
        sa.Column("type", statetype, nullable=False),
        sa.Column("effect_until", sa.Integer(), nullable=False),
        schema="BCS",
    )


def downgrade():
    op.drop_table("states", schema="BCS")
    op.drop_table("traits", schema="BCS")
