"""replace league name with a translation composite type (en, hu)

Revision ID: k6l7m8n9o0p1
Revises: j5k6l7m8n9o0
Create Date: 2026-08-04 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'k6l7m8n9o0p1'
down_revision: Union[str, None] = 'j5k6l7m8n9o0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE TYPE "BCS".translation AS (en varchar, hu varchar)')

    op.drop_constraint('uq_leagues_name', 'leagues', type_='unique', schema='BCS')

    op.execute('ALTER TABLE "BCS".leagues ADD COLUMN name_tmp "BCS".translation')
    op.execute('UPDATE "BCS".leagues SET name_tmp = ROW(name, name)::"BCS".translation')
    op.alter_column('leagues', 'name_tmp', nullable=False, schema='BCS')

    op.drop_column('leagues', 'name', schema='BCS')
    op.alter_column('leagues', 'name_tmp', new_column_name='name', schema='BCS')


def downgrade() -> None:
    op.add_column('leagues', sa.Column('name_tmp', sa.String()), schema='BCS')
    op.execute('UPDATE "BCS".leagues SET name_tmp = (name).en')
    op.alter_column('leagues', 'name_tmp', nullable=False, schema='BCS')

    op.drop_column('leagues', 'name', schema='BCS')
    op.alter_column('leagues', 'name_tmp', new_column_name='name', schema='BCS')

    op.create_unique_constraint('uq_leagues_name', 'leagues', ['name'], schema='BCS')

    op.execute('DROP TYPE "BCS".translation')
