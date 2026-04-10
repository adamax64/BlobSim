"""add table retirement focus

Revision ID: 50ea619ed710
Revises: b3002bb97150
Create Date: 2026-04-08 18:22:13.425701

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "50ea619ed710"
down_revision: Union[str, None] = "b3002bb97150"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    focustype = sa.Enum(
        "LEGACY", "PROLONGED_LIFE", name="retirementfocustype", schema="BCS"
    )

    op.create_table(
        "retirement_focus",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "blob_id",
            sa.Integer(),
            sa.ForeignKey("BCS.blobs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("focus_type", focustype, nullable=False),
        schema="BCS",
    )

    op.execute(
        "ALTER TYPE \"BCS\".activitytype ADD VALUE IF NOT EXISTS 'APPLY_FOR_HEIR'"
    )


def downgrade() -> None:
    op.drop_table("retirement_focus")
