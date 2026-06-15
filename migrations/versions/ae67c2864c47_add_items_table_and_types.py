"""add items table and types

Revision ID: ae67c2864c47
Revises: 9e1448823996
Create Date: 2026-06-15 21:05:33.254761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from data.model.item_type import ItemType


# revision identifiers, used by Alembic.
revision: str = 'ae67c2864c47'
down_revision: Union[str, None] = '9e1448823996'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("type", sa.Enum(ItemType, name="itemtype", schema="BCS"), nullable=False),
        sa.Column("blob_id", sa.Integer(), sa.ForeignKey("BCS.blobs.id"), nullable=False),
        sa.Column("durability", sa.Integer(), nullable=False),
        schema="BCS",
    )


def downgrade() -> None:
    op.drop_table("items", schema="BCS")
    op.execute("DROP TYPE IF EXISTS \"BCS\".itemtype")
