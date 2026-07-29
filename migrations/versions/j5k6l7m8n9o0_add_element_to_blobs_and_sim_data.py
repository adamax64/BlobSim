"""add element to blobs and element tokens to sim_data

Revision ID: j5k6l7m8n9o0
Revises: i4j5k6l7m8n9
Create Date: 2026-07-29 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "j5k6l7m8n9o0"
down_revision: Union[str, None] = "i4j5k6l7m8n9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    element_enum = sa.Enum(
        "NONE",
        "FIRE",
        "WIND",
        "WATER",
        "ICE",
        "BEAST",
        name="elementtype",
        schema="BCS",
    )
    element_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "blobs",
        sa.Column("element", element_enum, server_default="NONE", nullable=False),
        schema="BCS",
    )

    for column_name in (
        "fire_tokens",
        "wind_tokens",
        "water_tokens",
        "ice_tokens",
        "beast_tokens",
        "neutral_tokens",
    ):
        op.add_column(
            "sim_data",
            sa.Column(column_name, sa.Integer(), server_default="0", nullable=False),
            schema="BCS",
        )


def downgrade() -> None:
    for column_name in (
        "fire_tokens",
        "wind_tokens",
        "water_tokens",
        "ice_tokens",
        "beast_tokens",
        "neutral_tokens",
    ):
        op.drop_column("sim_data", column_name, schema="BCS")

    op.drop_column("blobs", "element", schema="BCS")
    op.execute('DROP TYPE IF EXISTS "BCS".elementtype')
