"""add weather, wind and season temperature to sim_data

Revision ID: i4j5k6l7m8n9
Revises: b3002bb97150
Create Date: 2026-07-22 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "i4j5k6l7m8n9"
down_revision: Union[str, None] = "d4e5f6a7b8c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    weather_type_enum = sa.Enum(
        "SUNNY",
        "SUNNY_CLOUDY",
        "CLOUDY",
        "SUNNY_RAIN",
        "RAIN",
        "HEAVY_RAIN",
        "STORM",
        "HEAT",
        "SNOWY",
        "FREEZY",
        "FOGGY",
        name="weathertype",
        schema="BCS",
    )
    weather_type_enum.create(op.get_bind(), checkfirst=True)

    season_temperature_enum = sa.Enum(
        "COLD", "NEUTRAL", "WARM", name="seasontemperature", schema="BCS"
    )
    season_temperature_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "sim_data",
        sa.Column(
            "weather", weather_type_enum, server_default="SUNNY", nullable=False
        ),
        schema="BCS",
    )
    op.add_column(
        "sim_data",
        sa.Column("wind", sa.Float(), server_default="0.5", nullable=False),
        schema="BCS",
    )
    op.add_column(
        "sim_data",
        sa.Column(
            "season_temperature",
            season_temperature_enum,
            server_default="NEUTRAL",
            nullable=False,
        ),
        schema="BCS",
    )


def downgrade() -> None:
    op.drop_column("sim_data", "season_temperature", schema="BCS")
    op.drop_column("sim_data", "wind", schema="BCS")
    op.drop_column("sim_data", "weather", schema="BCS")
    op.execute('DROP TYPE IF EXISTS "BCS".seasontemperature')
    op.execute('DROP TYPE IF EXISTS "BCS".weathertype')
