"""Initialize database

Revision ID: e4a5670babb4
Revises: 
Create Date: 2025-01-04 15:33:44.172229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4a5670babb4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('database_changelog',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('date', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('leagues',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('level', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('level')
                    )
    op.create_table('sim_data',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('sim_time', sa.BigInteger(), nullable=True),
                    sa.Column('factory_progress', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('email', sa.String(), nullable=True),
                    sa.Column('password', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('blobs',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('strength', sa.Double(), nullable=True),
                    sa.Column('learning', sa.Double(), nullable=True),
                    sa.Column('integrity', sa.Integer(), nullable=True),
                    sa.Column('born', sa.BigInteger(), nullable=True),
                    sa.Column('terminated', sa.BigInteger(), nullable=True),
                    sa.Column('debut', sa.Integer(), nullable=True),
                    sa.Column('contract', sa.Integer(), nullable=True),
                    sa.Column('money', sa.Integer(), nullable=True),
                    sa.Column('points', sa.Integer(), nullable=True),
                    sa.Column('bronze_medals', sa.Integer(), nullable=True),
                    sa.Column('silver_medals', sa.Integer(), nullable=True),
                    sa.Column('gold_medals', sa.Integer(), nullable=True),
                    sa.Column('season_victories', sa.Integer(), nullable=True),
                    sa.Column('bronze_trophies', sa.Integer(), nullable=True),
                    sa.Column('silver_trophies', sa.Integer(), nullable=True),
                    sa.Column('gold_trophies', sa.Integer(), nullable=True),
                    sa.Column('championships', sa.Integer(), nullable=True),
                    sa.Column('grandmasters', sa.Integer(), nullable=True),
                    sa.Column('league_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['league_id'], ['leagues.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('calendar',
                    sa.Column('date', sa.BigInteger(), nullable=False),
                    sa.Column('league_id', sa.Integer(), nullable=True),
                    sa.Column('concluded', sa.Boolean(), nullable=True),
                    sa.Column('event_type', sa.Enum('QUARTERED_ONE_SHOT_SCORING', 'QUARTERED_TWO_SHOT_SCORING', name='eventtype'), nullable=True),
                    sa.ForeignKeyConstraint(['league_id'], ['leagues.id'], ),
                    sa.PrimaryKeyConstraint('date')
                    )
    op.create_table('events',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('league_id', sa.Integer(), nullable=True),
                    sa.Column('date', sa.BigInteger(), nullable=True),
                    sa.Column('season', sa.Integer(), nullable=True),
                    sa.Column('round', sa.Integer(), nullable=True),
                    sa.Column('type', sa.Enum('QUARTERED_ONE_SHOT_SCORING', 'QUARTERED_TWO_SHOT_SCORING', name='eventtype'), nullable=True),
                    sa.ForeignKeyConstraint(['league_id'], ['leagues.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('actions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('event_id', sa.Integer(), nullable=True),
                    sa.Column('tick', sa.Integer(), nullable=True),
                    sa.Column('blob_id', sa.Integer(), nullable=True),
                    sa.Column('score', sa.Double(), nullable=True),
                    sa.ForeignKeyConstraint(['blob_id'], ['blobs.id'], ),
                    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('results',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('event_id', sa.Integer(), nullable=True),
                    sa.Column('blob_id', sa.Integer(), nullable=True),
                    sa.Column('position', sa.Integer(), nullable=True),
                    sa.Column('points', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['blob_id'], ['blobs.id'], ),
                    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # Insert initial data into the tables
    op.bulk_insert(
        sa.table('leagues',
                 sa.column('id', sa.Integer),
                 sa.column('name', sa.String),
                 sa.column('level', sa.Integer)),
        [
            {'id': 1, 'name': 'Masters League', 'level': 1},
            {'id': 2, 'name': 'queue', 'level': 10},
            {'id': 3, 'name': 'Dropout League', 'level': 0},
        ]
    )

    op.bulk_insert(
        sa.table('users',
                 sa.column('id', sa.Integer),
                 sa.column('name', sa.String),
                 sa.column('email', sa.String),
                 sa.column('password', sa.String)),
        [
            {'id': 1, 'name': 'Test User', 'email': 'testuser@insertyouremailaddress.com', 'password': '<insert_password_here>'},
        ]
    )

    op.bulk_insert(
        sa.table('blobs',
                 sa.column('id', sa.Integer),
                 sa.column('name', sa.String),
                 sa.column('strength', sa.Float),
                 sa.column('learning', sa.Float),
                 sa.column('integrity', sa.Integer),
                 sa.column('born', sa.BigInteger),
                 sa.column('debut', sa.Integer),
                 sa.column('contract', sa.Integer),
                 sa.column('money', sa.Integer),
                 sa.column('points', sa.Integer),
                 sa.column('bronze_trophies', sa.Integer),
                 sa.column('silver_trophies', sa.Integer),
                 sa.column('gold_trophies', sa.Integer),
                 sa.column('championships', sa.Integer),
                 sa.column('grandmasters', sa.Integer),
                 sa.column('league_id', sa.Integer),
                 sa.column('bronze_medals', sa.Integer),
                 sa.column('silver_medals', sa.Integer),
                 sa.column('gold_medals', sa.Integer),
                 sa.column('season_victories', sa.Integer),
                 sa.column('terminated', sa.BigInteger)),
        [
            {'id': 1, 'name': 'Michael Prime', 'strength': 3.1735510250328396, 'learning': 0.9484769912, 'integrity': 3834, 'born': 0, 'debut': 1, 'contract': 4, 'money': 7, 'points': 79, 'bronze_trophies': 2, 'silver_trophies': 1, 'gold_trophies': 2, 'championships': 0, 'grandmasters': 0, 'league_id': 1, 'bronze_medals': 0, 'silver_medals': 0, 'gold_medals': 0, 'season_victories': 0, 'terminated': None},
            {'id': 2, 'name': 'Jeremy Salusa', 'strength': 2.226099787677672, 'learning': 0.5987557392, 'integrity': 3834, 'born': 0, 'debut': 1, 'contract': 6, 'money': 12, 'points': 77, 'bronze_trophies': 3, 'silver_trophies': 5, 'gold_trophies': 1, 'championships': 1, 'grandmasters': 0, 'league_id': 1, 'bronze_medals': 0, 'silver_medals': 0, 'gold_medals': 0, 'season_victories': 0, 'terminated': None},
            {'id': 3, 'name': 'George Vritas', 'strength': 3.0875950205940756, 'learning': 0.8672848692, 'integrity': 3771, 'born': 0, 'debut': 1, 'contract': 3, 'money': 27, 'points': 89, 'bronze_trophies': 3, 'silver_trophies': 2, 'gold_trophies': 3, 'championships': 0, 'grandmasters': 0, 'league_id': 1, 'bronze_medals': 0, 'silver_medals': 0, 'gold_medals': 0, 'season_victories': 0, 'terminated': None},
            {'id': 4, 'name': 'Mark Bruss', 'strength': 2.0367083816058518, 'learning': 0.527368779, 'integrity': 3803, 'born': 0, 'debut': 1, 'contract': 5, 'money': 2, 'points': 74, 'bronze_trophies': 1, 'silver_trophies': 4, 'gold_trophies': 1, 'championships': 0, 'grandmasters': 0, 'league_id': 1, 'bronze_medals': 0, 'silver_medals': 0, 'gold_medals': 0, 'season_victories': 0, 'terminated': None},
            {'id': 5, 'name': 'Oliver Quenta', 'strength': 2.527164715581371, 'learning': 0.6105550684, 'integrity': 3771, 'born': 0, 'debut': 1, 'contract': 5, 'money': 27, 'points': 75, 'bronze_trophies': 3, 'silver_trophies': 1, 'gold_trophies': 2, 'championships': 1, 'grandmasters': 0, 'league_id': 1, 'bronze_medals': 0, 'silver_medals': 0, 'gold_medals': 0, 'season_victories': 0, 'terminated': None},
            {'id': 6, 'name': 'Alia Sixtum', 'strength': 2.8446778608935808, 'learning': 0.8307200812, 'integrity': 3771, 'born': 0, 'debut': 1, 'contract': 4, 'money': 16, 'points': 72, 'bronze_trophies': 1, 'silver_trophies': 0, 'gold_trophies': 4, 'championships': 0, 'grandmasters': 0, 'league_id': 1, 'bronze_medals': 0, 'silver_medals': 0, 'gold_medals': 0, 'season_victories': 0, 'terminated': None},
            {'id': 7, 'name': 'Elisabeth Taladan', 'strength': 1.6383992728642083, 'learning': 0.5590903629, 'integrity': 3915, 'born': 144, 'debut': 2, 'contract': 4, 'money': 30, 'points': 45, 'bronze_trophies': 0, 'silver_trophies': 0, 'gold_trophies': 1, 'championships': 0, 'grandmasters': 0, 'league_id': 1, 'bronze_medals': 0, 'silver_medals': 0, 'gold_medals': 0, 'season_victories': 0, 'terminated': None},
            {'id': 8, 'name': 'Jaroslava Vitalik', 'strength': 1.571316958945388, 'learning': 0.8130876006, 'integrity': 3944, 'born': 173, 'debut': 3, 'contract': 5, 'money': 32, 'points': 25, 'bronze_trophies': 0, 'silver_trophies': 1, 'gold_trophies': 0, 'championships': 0, 'grandmasters': 0, 'league_id': 1, 'bronze_medals': 0, 'silver_medals': 0, 'gold_medals': 0, 'season_victories': 0, 'terminated': None},
            {'id': 9, 'name': 'Paul Dechen', 'strength': 1.4116313783782566, 'learning': 0.7117629892, 'integrity': 3970, 'born': 230, 'debut': 3, 'contract': 5, 'money': 28, 'points': 18, 'bronze_trophies': 1, 'silver_trophies': 0, 'gold_trophies': 0, 'championships': 0, 'grandmasters': 0, 'league_id': 1, 'bronze_medals': 0, 'silver_medals': 0, 'gold_medals': 0, 'season_victories': 0, 'terminated': None},
            {'id': 10, 'name': 'Andrew Perle', 'strength': 1.1235468249979363, 'learning': 0.6612005084, 'integrity': 4022, 'born': 282, 'debut': None, 'contract': None, 'money': 26, 'points': 0, 'bronze_trophies': 0, 'silver_trophies': 0, 'gold_trophies': 0, 'championships': 0, 'grandmasters': 0, 'league_id': 2, 'bronze_medals': 0, 'silver_medals': 0, 'gold_medals': 0, 'season_victories': 0, 'terminated': None},
            {'id': 11, 'name': 'Kadahara Nokoma', 'strength': 1.026347983677317, 'learning': 0.8726407676871863, 'integrity': 4066, 'born': 326, 'debut': None, 'contract': None, 'money': 12, 'points': 0, 'bronze_trophies': 0, 'silver_trophies': 0, 'gold_trophies': 0, 'championships': 0, 'grandmasters': 0, 'league_id': 2, 'bronze_medals': 0, 'silver_medals': 0, 'gold_medals': 0, 'season_victories': 0, 'terminated': None},
        ]
    )

    op.bulk_insert(
        sa.table('calendar',
                 sa.column('date', sa.BigInteger),
                 sa.column('league_id', sa.Integer),
                 sa.column('concluded', sa.Boolean),
                 sa.column('event_type', sa.Enum('QUARTERED_ONE_SHOT_SCORING', 'QUARTERED_TWO_SHOT_SCORING', name='eventtype'))),
        [
            {'date': 271, 'league_id': 1, 'concluded': True, 'event_type': 'QUARTERED_TWO_SHOT_SCORING'},
            {'date': 283, 'league_id': 1, 'concluded': True, 'event_type': 'QUARTERED_ONE_SHOT_SCORING'},
            {'date': 299, 'league_id': 1, 'concluded': True, 'event_type': 'QUARTERED_TWO_SHOT_SCORING'},
            {'date': 311, 'league_id': 1, 'concluded': True, 'event_type': 'QUARTERED_ONE_SHOT_SCORING'},
            {'date': 331, 'league_id': 1, 'concluded': True, 'event_type': 'QUARTERED_TWO_SHOT_SCORING'},
            {'date': 343, 'league_id': 1, 'concluded': True, 'event_type': 'QUARTERED_ONE_SHOT_SCORING'},
            {'date': 359, 'league_id': 1, 'concluded': False, 'event_type': 'QUARTERED_TWO_SHOT_SCORING'},
            {'date': 371, 'league_id': 1, 'concluded': False, 'event_type': 'QUARTERED_ONE_SHOT_SCORING'},
        ]
    )

    op.bulk_insert(
        sa.table('events',
                 sa.column('id', sa.Integer),
                 sa.column('league_id', sa.Integer),
                 sa.column('date', sa.BigInteger),
                 sa.column('season', sa.Integer),
                 sa.column('round', sa.Integer),
                 sa.column('type', sa.Enum('QUARTERED_ONE_SHOT_SCORING', 'QUARTERED_TWO_SHOT_SCORING', name='eventtype'))),
        [
            {'id': 1, 'league_id': 1, 'date': None, 'season': 1, 'round': 1, 'type': 'QUARTERED_ONE_SHOT_SCORING'},
            {'id': 2, 'league_id': 1, 'date': None, 'season': 1, 'round': 2, 'type': 'QUARTERED_ONE_SHOT_SCORING'},
            {'id': 3, 'league_id': 1, 'date': None, 'season': 1, 'round': 3, 'type': 'QUARTERED_ONE_SHOT_SCORING'},
            {'id': 4, 'league_id': 1, 'date': None, 'season': 1, 'round': 4, 'type': 'QUARTERED_ONE_SHOT_SCORING'},
            {'id': 5, 'league_id': 1, 'date': None, 'season': 2, 'round': 1, 'type': 'QUARTERED_ONE_SHOT_SCORING'},
            {'id': 6, 'league_id': 1, 'date': None, 'season': 2, 'round': 2, 'type': 'QUARTERED_ONE_SHOT_SCORING'},
            {'id': 7, 'league_id': 1, 'date': None, 'season': 2, 'round': 3, 'type': 'QUARTERED_ONE_SHOT_SCORING'},
            {'id': 8, 'league_id': 1, 'date': None, 'season': 2, 'round': 4, 'type': 'QUARTERED_ONE_SHOT_SCORING'},
            {'id': 9, 'league_id': 1, 'date': 271, 'season': 3, 'round': 1, 'type': 'QUARTERED_TWO_SHOT_SCORING'},
            {'id': 10, 'league_id': 1, 'date': 283, 'season': 3, 'round': 2, 'type': 'QUARTERED_ONE_SHOT_SCORING'},
            {'id': 11, 'league_id': 1, 'date': 299, 'season': 3, 'round': 3, 'type': 'QUARTERED_TWO_SHOT_SCORING'},
            {'id': 12, 'league_id': 1, 'date': 311, 'season': 3, 'round': 4, 'type': 'QUARTERED_ONE_SHOT_SCORING'},
            {'id': 13, 'league_id': 1, 'date': 331, 'season': 3, 'round': 5, 'type': 'QUARTERED_TWO_SHOT_SCORING'},
            {'id': 14, 'league_id': 1, 'date': 343, 'season': 3, 'round': 6, 'type': 'QUARTERED_ONE_SHOT_SCORING'},
        ]
    )

    op.bulk_insert(
        sa.table('results',
                 sa.column('id', sa.Integer),
                 sa.column('event_id', sa.Integer),
                 sa.column('blob_id', sa.Integer),
                 sa.column('position', sa.Integer),
                 sa.column('points', sa.Integer)),
        [
            {'id': 1, 'event_id': 1, 'blob_id': 2, 'position': 2, 'points': 5},
            {'id': 2, 'event_id': 1, 'blob_id': 4, 'position': 4, 'points': 3},
            {'id': 3, 'event_id': 1, 'blob_id': 6, 'position': 1, 'points': 7},
            {'id': 4, 'event_id': 1, 'blob_id': 3, 'position': 3, 'points': 4},
            {'id': 5, 'event_id': 1, 'blob_id': 1, 'position': 5, 'points': 2},
            {'id': 6, 'event_id': 1, 'blob_id': 5, 'position': 6, 'points': 1},
            {'id': 7, 'event_id': 2, 'blob_id': 2, 'position': 3, 'points': 4},
            {'id': 8, 'event_id': 2, 'blob_id': 4, 'position': 2, 'points': 5},
            {'id': 9, 'event_id': 2, 'blob_id': 6, 'position': 1, 'points': 7},
            {'id': 10, 'event_id': 2, 'blob_id': 3, 'position': 6, 'points': 1},
            {'id': 11, 'event_id': 2, 'blob_id': 1, 'position': 4, 'points': 3},
            {'id': 12, 'event_id': 2, 'blob_id': 5, 'position': 5, 'points': 2},
            {'id': 13, 'event_id': 3, 'blob_id': 2, 'position': 4, 'points': 3},
            {'id': 14, 'event_id': 3, 'blob_id': 4, 'position': 1, 'points': 7},
            {'id': 15, 'event_id': 3, 'blob_id': 6, 'position': 6, 'points': 1},
            {'id': 16, 'event_id': 3, 'blob_id': 3, 'position': 2, 'points': 5},
            {'id': 17, 'event_id': 3, 'blob_id': 1, 'position': 5, 'points': 2},
            {'id': 18, 'event_id': 3, 'blob_id': 5, 'position': 3, 'points': 4},
            {'id': 19, 'event_id': 4, 'blob_id': 2, 'position': 1, 'points': 7},
            {'id': 20, 'event_id': 4, 'blob_id': 4, 'position': 4, 'points': 3},
            {'id': 21, 'event_id': 4, 'blob_id': 6, 'position': 5, 'points': 2},
            {'id': 22, 'event_id': 4, 'blob_id': 3, 'position': 3, 'points': 4},
            {'id': 23, 'event_id': 4, 'blob_id': 1, 'position': 2, 'points': 5},
            {'id': 24, 'event_id': 4, 'blob_id': 5, 'position': 6, 'points': 1},
            {'id': 25, 'event_id': 5, 'blob_id': 5, 'position': 2, 'points': 6},
            {'id': 26, 'event_id': 5, 'blob_id': 1, 'position': 7, 'points': 1},
            {'id': 27, 'event_id': 5, 'blob_id': 2, 'position': 3, 'points': 6},
            {'id': 28, 'event_id': 5, 'blob_id': 4, 'position': 5, 'points': 4},
            {'id': 29, 'event_id': 5, 'blob_id': 7, 'position': 4, 'points': 5},
            {'id': 30, 'event_id': 5, 'blob_id': 6, 'position': 1, 'points': 8},
            {'id': 31, 'event_id': 5, 'blob_id': 3, 'position': 6, 'points': 2},
            {'id': 32, 'event_id': 6, 'blob_id': 5, 'position': 5, 'points': 3},
            {'id': 33, 'event_id': 6, 'blob_id': 1, 'position': 1, 'points': 9},
            {'id': 34, 'event_id': 6, 'blob_id': 2, 'position': 6, 'points': 2},
            {'id': 35, 'event_id': 6, 'blob_id': 4, 'position': 2, 'points': 7},
            {'id': 36, 'event_id': 6, 'blob_id': 7, 'position': 7, 'points': 1},
            {'id': 37, 'event_id': 6, 'blob_id': 6, 'position': 3, 'points': 5},
            {'id': 38, 'event_id': 6, 'blob_id': 3, 'position': 4, 'points': 5},
            {'id': 39, 'event_id': 7, 'blob_id': 5, 'position': 1, 'points': 8},
            {'id': 40, 'event_id': 7, 'blob_id': 1, 'position': 4, 'points': 7},
            {'id': 41, 'event_id': 7, 'blob_id': 2, 'position': 2, 'points': 6},
            {'id': 42, 'event_id': 7, 'blob_id': 4, 'position': 3, 'points': 5},
            {'id': 43, 'event_id': 7, 'blob_id': 7, 'position': 5, 'points': 3},
            {'id': 44, 'event_id': 7, 'blob_id': 6, 'position': 7, 'points': 1},
            {'id': 45, 'event_id': 7, 'blob_id': 3, 'position': 6, 'points': 2},
            {'id': 46, 'event_id': 8, 'blob_id': 5, 'position': 3, 'points': 8},
            {'id': 47, 'event_id': 8, 'blob_id': 1, 'position': 4, 'points': 4},
            {'id': 48, 'event_id': 8, 'blob_id': 2, 'position': 2, 'points': 6},
            {'id': 49, 'event_id': 8, 'blob_id': 4, 'position': 5, 'points': 3},
            {'id': 50, 'event_id': 8, 'blob_id': 7, 'position': 1, 'points': 8},
            {'id': 51, 'event_id': 8, 'blob_id': 6, 'position': 7, 'points': 1},
            {'id': 52, 'event_id': 8, 'blob_id': 3, 'position': 6, 'points': 2},
            {'id': 53, 'event_id': 9, 'blob_id': 3, 'position': 1, 'points': 15},
            {'id': 54, 'event_id': 9, 'blob_id': 1, 'position': 4, 'points': 7},
            {'id': 55, 'event_id': 9, 'blob_id': 5, 'position': 5, 'points': 5},
            {'id': 56, 'event_id': 9, 'blob_id': 2, 'position': 3, 'points': 8},
            {'id': 57, 'event_id': 9, 'blob_id': 4, 'position': 2, 'points': 10},
            {'id': 58, 'event_id': 9, 'blob_id': 6, 'position': 6, 'points': 4},
            {'id': 59, 'event_id': 9, 'blob_id': 8, 'position': 8, 'points': 2},
            {'id': 60, 'event_id': 9, 'blob_id': 9, 'position': 7, 'points': 3},
            {'id': 61, 'event_id': 9, 'blob_id': 7, 'position': 9, 'points': 1},
            {'id': 62, 'event_id': 10, 'blob_id': 3, 'position': 3, 'points': 9},
            {'id': 63, 'event_id': 10, 'blob_id': 1, 'position': 1, 'points': 14},
            {'id': 64, 'event_id': 10, 'blob_id': 5, 'position': 5, 'points': 5},
            {'id': 65, 'event_id': 10, 'blob_id': 2, 'position': 2, 'points': 10},
            {'id': 66, 'event_id': 10, 'blob_id': 4, 'position': 7, 'points': 3},
            {'id': 67, 'event_id': 10, 'blob_id': 6, 'position': 4, 'points': 7},
            {'id': 68, 'event_id': 10, 'blob_id': 8, 'position': 6, 'points': 4},
            {'id': 69, 'event_id': 10, 'blob_id': 9, 'position': 8, 'points': 2},
            {'id': 70, 'event_id': 10, 'blob_id': 7, 'position': 9, 'points': 1},
            {'id': 71, 'event_id': 11, 'blob_id': 3, 'position': 2, 'points': 11},
            {'id': 72, 'event_id': 11, 'blob_id': 1, 'position': 3, 'points': 8},
            {'id': 73, 'event_id': 11, 'blob_id': 5, 'position': 1, 'points': 15},
            {'id': 74, 'event_id': 11, 'blob_id': 2, 'position': 9, 'points': 1},
            {'id': 75, 'event_id': 11, 'blob_id': 4, 'position': 5, 'points': 5},
            {'id': 76, 'event_id': 11, 'blob_id': 6, 'position': 6, 'points': 4},
            {'id': 77, 'event_id': 11, 'blob_id': 8, 'position': 8, 'points': 2},
            {'id': 78, 'event_id': 11, 'blob_id': 9, 'position': 7, 'points': 3},
            {'id': 79, 'event_id': 11, 'blob_id': 7, 'position': 4, 'points': 6},
            {'id': 80, 'event_id': 12, 'blob_id': 6, 'position': 1, 'points': 13},
            {'id': 81, 'event_id': 12, 'blob_id': 8, 'position': 2, 'points': 11},
            {'id': 82, 'event_id': 12, 'blob_id': 9, 'position': 3, 'points': 8},
            {'id': 83, 'event_id': 12, 'blob_id': 4, 'position': 4, 'points': 6},
            {'id': 84, 'event_id': 12, 'blob_id': 2, 'position': 5, 'points': 6},
            {'id': 85, 'event_id': 12, 'blob_id': 5, 'position': 6, 'points': 5},
            {'id': 86, 'event_id': 12, 'blob_id': 1, 'position': 7, 'points': 3},
            {'id': 87, 'event_id': 12, 'blob_id': 3, 'position': 8, 'points': 2},
            {'id': 88, 'event_id': 12, 'blob_id': 7, 'position': 9, 'points': 1},
            {'id': 89, 'event_id': 13, 'blob_id': 3, 'position': 1, 'points': 14},
            {'id': 90, 'event_id': 13, 'blob_id': 2, 'position': 2, 'points': 10},
            {'id': 91, 'event_id': 13, 'blob_id': 1, 'position': 3, 'points': 10},
            {'id': 92, 'event_id': 13, 'blob_id': 7, 'position': 4, 'points': 6},
            {'id': 93, 'event_id': 13, 'blob_id': 6, 'position': 5, 'points': 5},
            {'id': 94, 'event_id': 13, 'blob_id': 8, 'position': 6, 'points': 4},
            {'id': 95, 'event_id': 13, 'blob_id': 5, 'position': 7, 'points': 3},
            {'id': 96, 'event_id': 13, 'blob_id': 4, 'position': 8, 'points': 2},
            {'id': 97, 'event_id': 13, 'blob_id': 9, 'position': 9, 'points': 1},
            {'id': 98, 'event_id': 14, 'blob_id': 3, 'position': 1, 'points': 13},
            {'id': 99, 'event_id': 14, 'blob_id': 4, 'position': 2, 'points': 11},
            {'id': 100, 'event_id': 14, 'blob_id': 5, 'position': 3, 'points': 9},
            {'id': 101, 'event_id': 14, 'blob_id': 6, 'position': 4, 'points': 7},
            {'id': 102, 'event_id': 14, 'blob_id': 7, 'position': 5, 'points': 5},
            {'id': 103, 'event_id': 14, 'blob_id': 1, 'position': 6, 'points': 4},
            {'id': 104, 'event_id': 14, 'blob_id': 2, 'position': 7, 'points': 3},
            {'id': 105, 'event_id': 14, 'blob_id': 8, 'position': 8, 'points': 2},
            {'id': 106, 'event_id': 14, 'blob_id': 9, 'position': 9, 'points': 1},
        ]
    )

    op.bulk_insert(
        sa.table('actions',
                 sa.column('id', sa.Integer),
                 sa.column('event_id', sa.Integer),
                 sa.column('tick', sa.Integer),
                 sa.column('blob_id', sa.Integer),
                 sa.column('score', sa.Float)),
        [
            {'id': 1, 'event_id': 12, 'tick': 0, 'blob_id': 6, 'score': 1.002165804567775},
            {'id': 2, 'event_id': 12, 'tick': 1, 'blob_id': 2, 'score': 1.4468579159948627},
            {'id': 3, 'event_id': 12, 'tick': 2, 'blob_id': 3, 'score': 0.5127228538899189},
            {'id': 4, 'event_id': 12, 'tick': 3, 'blob_id': 9, 'score': 0.8125611628156757},
            {'id': 5, 'event_id': 12, 'tick': 4, 'blob_id': 7, 'score': 0.10899404072292464},
            {'id': 6, 'event_id': 12, 'tick': 5, 'blob_id': 1, 'score': 0.9007013510312226},
            {'id': 7, 'event_id': 12, 'tick': 6, 'blob_id': 8, 'score': 1.3268336289248652},
            {'id': 8, 'event_id': 12, 'tick': 7, 'blob_id': 4, 'score': 0.7351932820454287},
            {'id': 9, 'event_id': 12, 'tick': 8, 'blob_id': 5, 'score': 1.7811399868466706},
            {'id': 10, 'event_id': 12, 'tick': 9, 'blob_id': 5, 'score': 0.12915796010707076},
            {'id': 11, 'event_id': 12, 'tick': 10, 'blob_id': 2, 'score': 1.274105256999784},
            {'id': 12, 'event_id': 12, 'tick': 11, 'blob_id': 8, 'score': 0.9741221626199154},
            {'id': 13, 'event_id': 12, 'tick': 12, 'blob_id': 6, 'score': 0.33449750050450944},
            {'id': 14, 'event_id': 12, 'tick': 13, 'blob_id': 1, 'score': 0.04279039624178815},
            {'id': 15, 'event_id': 12, 'tick': 14, 'blob_id': 9, 'score': 0.8497363311537404},
            {'id': 16, 'event_id': 12, 'tick': 15, 'blob_id': 4, 'score': 1.1446957045005568},
            {'id': 17, 'event_id': 12, 'tick': 16, 'blob_id': 2, 'score': 0.3626441526943075},
            {'id': 18, 'event_id': 12, 'tick': 17, 'blob_id': 4, 'score': 0.4002844480210159},
            {'id': 19, 'event_id': 12, 'tick': 18, 'blob_id': 8, 'score': 1.3079511307434},
            {'id': 20, 'event_id': 12, 'tick': 19, 'blob_id': 9, 'score': 0.9212558660963276},
            {'id': 21, 'event_id': 12, 'tick': 20, 'blob_id': 6, 'score': 1.3043587089788116},
            {'id': 22, 'event_id': 12, 'tick': 21, 'blob_id': 8, 'score': 1.3913507350233967},
            {'id': 23, 'event_id': 12, 'tick': 22, 'blob_id': 6, 'score': 1.8878846234360642},
            {'id': 24, 'event_id': 12, 'tick': 23, 'blob_id': 9, 'score': 0.3528983517007876},
            {'id': 25, 'event_id': 13, 'tick': 0, 'blob_id': 4, 'score': 0.782392163816787},
            {'id': 26, 'event_id': 13, 'tick': 1, 'blob_id': 9, 'score': 0.5442814502278482},
            {'id': 27, 'event_id': 13, 'tick': 2, 'blob_id': 6, 'score': 2.174363312832637},
            {'id': 28, 'event_id': 13, 'tick': 3, 'blob_id': 1, 'score': 2.5118436023651416},
            {'id': 29, 'event_id': 13, 'tick': 4, 'blob_id': 2, 'score': 0.6724051797699623},
            {'id': 30, 'event_id': 13, 'tick': 5, 'blob_id': 5, 'score': 0.4132810563695034},
            {'id': 31, 'event_id': 13, 'tick': 6, 'blob_id': 7, 'score': 1.2967383933209526},
            {'id': 32, 'event_id': 13, 'tick': 7, 'blob_id': 3, 'score': 2.001985087140211},
            {'id': 33, 'event_id': 13, 'tick': 8, 'blob_id': 8, 'score': 0.5799633893381972},
            {'id': 34, 'event_id': 13, 'tick': 9, 'blob_id': 1, 'score': 0.018737970288352637},
            {'id': 35, 'event_id': 13, 'tick': 10, 'blob_id': 6, 'score': 1.024276579513783},
            {'id': 36, 'event_id': 13, 'tick': 11, 'blob_id': 3, 'score': 0.22137840493345637},
            {'id': 37, 'event_id': 13, 'tick': 12, 'blob_id': 7, 'score': 1.2823197352847737},
            {'id': 38, 'event_id': 13, 'tick': 13, 'blob_id': 4, 'score': 1.0904305298987051},
            {'id': 39, 'event_id': 13, 'tick': 14, 'blob_id': 2, 'score': 2.1309939192287284},
            {'id': 40, 'event_id': 13, 'tick': 15, 'blob_id': 8, 'score': 1.2922542803785362},
            {'id': 41, 'event_id': 13, 'tick': 16, 'blob_id': 9, 'score': 0.37943129208813176},
            {'id': 42, 'event_id': 13, 'tick': 17, 'blob_id': 5, 'score': 2.2540502931683912},
            {'id': 43, 'event_id': 13, 'tick': 18, 'blob_id': 1, 'score': 1.9367533637965746},
            {'id': 44, 'event_id': 13, 'tick': 19, 'blob_id': 5, 'score': 0.46813322030419535},
            {'id': 45, 'event_id': 13, 'tick': 20, 'blob_id': 6, 'score': 1.6473555718498314},
            {'id': 46, 'event_id': 13, 'tick': 21, 'blob_id': 2, 'score': 1.0382049893632714},
            {'id': 47, 'event_id': 13, 'tick': 22, 'blob_id': 3, 'score': 1.7583725372473924},
            {'id': 48, 'event_id': 13, 'tick': 23, 'blob_id': 7, 'score': 0.6449774081373091},
            {'id': 49, 'event_id': 13, 'tick': 24, 'blob_id': 8, 'score': 0.4745803726107409},
            {'id': 50, 'event_id': 13, 'tick': 25, 'blob_id': 1, 'score': 1.6830454046664833},
            {'id': 51, 'event_id': 13, 'tick': 26, 'blob_id': 3, 'score': 1.3783613378104271},
            {'id': 52, 'event_id': 13, 'tick': 27, 'blob_id': 6, 'score': 0.8158595710177037},
            {'id': 53, 'event_id': 13, 'tick': 28, 'blob_id': 2, 'score': 0.4242059565446894},
            {'id': 54, 'event_id': 13, 'tick': 29, 'blob_id': 7, 'score': 0.6940638931554597},
            {'id': 55, 'event_id': 13, 'tick': 30, 'blob_id': 8, 'score': 0.3578039847115686},
            {'id': 56, 'event_id': 13, 'tick': 31, 'blob_id': 5, 'score': 0.041266340969307834},
            {'id': 57, 'event_id': 13, 'tick': 32, 'blob_id': 1, 'score': 2.604441916053731},
            {'id': 58, 'event_id': 13, 'tick': 33, 'blob_id': 3, 'score': 0.8564028794089404},
            {'id': 59, 'event_id': 13, 'tick': 34, 'blob_id': 6, 'score': 0.7858118884870262},
            {'id': 60, 'event_id': 13, 'tick': 35, 'blob_id': 2, 'score': 1.956151658087452},
            {'id': 61, 'event_id': 13, 'tick': 36, 'blob_id': 7, 'score': 1.425234707743902},
            {'id': 62, 'event_id': 13, 'tick': 37, 'blob_id': 1, 'score': 2.0735274165133495},
            {'id': 63, 'event_id': 13, 'tick': 38, 'blob_id': 2, 'score': 1.8490182382800053},
            {'id': 64, 'event_id': 13, 'tick': 39, 'blob_id': 7, 'score': 0.7547815809533288},
            {'id': 65, 'event_id': 13, 'tick': 40, 'blob_id': 3, 'score': 2.9067298617983077},
            {'id': 66, 'event_id': 13, 'tick': 41, 'blob_id': 6, 'score': 1.0310268251560266},
            {'id': 67, 'event_id': 13, 'tick': 42, 'blob_id': 3, 'score': 2.789291737536149},
            {'id': 68, 'event_id': 13, 'tick': 43, 'blob_id': 1, 'score': 1.2883778482463115},
            {'id': 69, 'event_id': 13, 'tick': 44, 'blob_id': 2, 'score': 1.9137069902952153},
            {'id': 70, 'event_id': 13, 'tick': 45, 'blob_id': 3, 'score': 1.9346321523916588},
            {'id': 71, 'event_id': 13, 'tick': 46, 'blob_id': 2, 'score': 0.11305129588446577},
            {'id': 72, 'event_id': 13, 'tick': 47, 'blob_id': 1, 'score': 1.0086840642521995},
            {'id': 73, 'event_id': 14, 'tick': 0, 'blob_id': 4, 'score': 1.6442596222255683},
            {'id': 74, 'event_id': 14, 'tick': 1, 'blob_id': 9, 'score': 0.20280185387448418},
            {'id': 75, 'event_id': 14, 'tick': 2, 'blob_id': 3, 'score': 0.5570598033713402},
            {'id': 76, 'event_id': 14, 'tick': 3, 'blob_id': 1, 'score': 1.5642825605733477},
            {'id': 77, 'event_id': 14, 'tick': 4, 'blob_id': 6, 'score': 1.7583227781429018},
            {'id': 78, 'event_id': 14, 'tick': 5, 'blob_id': 2, 'score': 0.7289167814103995},
            {'id': 79, 'event_id': 14, 'tick': 6, 'blob_id': 5, 'score': 0.38602045352421666},
            {'id': 80, 'event_id': 14, 'tick': 7, 'blob_id': 8, 'score': 0.2246079426736387},
            {'id': 81, 'event_id': 14, 'tick': 8, 'blob_id': 7, 'score': 0.2818453156925569},
            {'id': 82, 'event_id': 14, 'tick': 9, 'blob_id': 6, 'score': 0.531827306498072},
            {'id': 83, 'event_id': 14, 'tick': 10, 'blob_id': 4, 'score': 1.7798682788737603},
            {'id': 84, 'event_id': 14, 'tick': 11, 'blob_id': 1, 'score': 0.3842278561610046},
            {'id': 85, 'event_id': 14, 'tick': 12, 'blob_id': 2, 'score': 0.06728318098630251},
            {'id': 86, 'event_id': 14, 'tick': 13, 'blob_id': 3, 'score': 0.7835483193496443},
            {'id': 87, 'event_id': 14, 'tick': 14, 'blob_id': 5, 'score': 2.291326486086381},
            {'id': 88, 'event_id': 14, 'tick': 15, 'blob_id': 7, 'score': 1.4739423666519886},
            {'id': 89, 'event_id': 14, 'tick': 16, 'blob_id': 5, 'score': 0.912134789168899},
            {'id': 90, 'event_id': 14, 'tick': 17, 'blob_id': 4, 'score': 1.4221653159227279},
            {'id': 91, 'event_id': 14, 'tick': 18, 'blob_id': 7, 'score': 0.08289492327931648},
            {'id': 92, 'event_id': 14, 'tick': 19, 'blob_id': 3, 'score': 0.8556952229286342},
            {'id': 93, 'event_id': 14, 'tick': 20, 'blob_id': 6, 'score': 0.7040408937293416},
            {'id': 94, 'event_id': 14, 'tick': 21, 'blob_id': 4, 'score': 1.7180353841219382},
            {'id': 95, 'event_id': 14, 'tick': 22, 'blob_id': 5, 'score': 1.579318071126816},
            {'id': 96, 'event_id': 14, 'tick': 23, 'blob_id': 3, 'score': 2.5845564090268334},
        ]
    )

    op.bulk_insert(
        sa.table('sim_data',
                 sa.column('id', sa.Integer),
                 sa.column('sim_time', sa.BigInteger),
                 sa.column('factory_progress', sa.Integer)),
        [
            {'id': 1, 'sim_time': 356, 'factory_progress': 106},
        ]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('results')
    op.drop_table('actions')
    op.drop_table('events')
    op.drop_table('calendar')
    op.drop_table('blobs')
    op.drop_table('users')
    op.drop_table('sim_data')
    op.drop_table('leagues')
    op.drop_table('database_changelog')
    # ### end Alembic commands ###
