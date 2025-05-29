"""Add parent_id to blob and name_suggestions table

Revision ID: 6c6b8a6b6b87
Revises: ea57d90019b8
Create Date: 2025-05-29 20:58:16.066749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c6b8a6b6b87'
down_revision: Union[str, None] = 'ea57d90019b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add parent_id to blobs table
    with op.batch_alter_table('blobs') as batch_op:
        batch_op.add_column(sa.Column('parent_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_blob_parent', 'blobs', ['parent_id'], ['id'])

    # Add parent_id to name_suggestions table
    with op.batch_alter_table('name_suggestions') as batch_op:
        batch_op.add_column(sa.Column('parent_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_name_suggestions_parent', 'blobs', ['parent_id'], ['id'])


def downgrade() -> None:
    # Remove parent_id from name_suggestions table
    with op.batch_alter_table('name_suggestions') as batch_op:
        batch_op.drop_constraint('fk_name_suggestions_parent', type_='foreignkey')
        batch_op.drop_column('parent_id')

    # Remove parent_id from blobs table
    with op.batch_alter_table('blobs') as batch_op:
        batch_op.drop_constraint('fk_blob_parent', type_='foreignkey')
        batch_op.drop_column('parent_id')
