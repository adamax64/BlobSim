"""add policies table

Revision ID: af12b3c4d5e6
Revises: 24fc2d4c2ba0
Create Date: 2025-12-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'af12b3c4d5e6'
down_revision = '24fc2d4c2ba0'
branch_labels = None
depends_on = None


def upgrade():
    policytype = sa.Enum(
        'PENSION_SCHEME',
        'FACTORY_MODERNIZATION',
        'LABOUR_SUBSIDIES',
        'GYM_IMPROVEMENT',
        name='policytype',
        schema='BCS'
    )

    op.create_table(
        'policies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('policy_type', policytype),
        sa.Column('effect_until', sa.BigInteger()),
        sa.Column('applied_level', sa.Integer()),
        schema='BCS'
    )


def downgrade():
    op.drop_table('policies', schema='BCS')
