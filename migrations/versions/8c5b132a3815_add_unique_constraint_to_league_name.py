"""add unique constraint to league name

Revision ID: 8c5b132a3815
Revises: 2b79abfa62a2
Create Date: 2025-10-10 13:44:57.033547

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '8c5b132a3815'
down_revision: Union[str, None] = '2b79abfa62a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add a unique constraint on the `name` column of the `leagues` table
    # in the `BCS` schema. The constraint name is chosen to be stable so it
    # can be dropped in downgrade.
    op.create_unique_constraint(
        constraint_name="uq_leagues_name",
        table_name="leagues",
        columns=["name"],
        schema="BCS",
    )


def downgrade() -> None:
    # Drop the unique constraint added in upgrade.
    # Use type_='unique' to be explicit for some backends.
    op.drop_constraint(
        constraint_name="uq_leagues_name",
        table_name="leagues",
        type_="unique",
        schema="BCS",
    )
