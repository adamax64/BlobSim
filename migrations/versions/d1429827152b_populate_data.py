"""populate data

Revision ID: d1429827152b
Revises: a0f5588ea845
Create Date: 2025-06-29 11:46:03.625744

"""
from typing import Sequence, Union
import csv
import os
from sqlalchemy.sql import table, column
from sqlalchemy import Integer, String, Float, BigInteger, Boolean

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'd1429827152b'
down_revision: Union[str, None] = 'd63686c84980'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    data_dir = os.path.join(os.path.dirname(__file__), '../../data_migration')

    # Leagues
    with open(os.path.join(data_dir, 'leagues_202506272255.csv'), encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [dict(id=int(r['id']), name=r['name'], level=int(r['level'])) for r in reader if r['id']]
        op.bulk_insert(
            table('leagues',
                  column('id', Integer), column('name', String), column('level', Integer),
                  schema='BCS'),
            rows,
            multiinsert=False
        )

    # Blobs
    with open(os.path.join(data_dir, 'blobs_202506272255.csv'), encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = []
        for r in reader:
            if not r['id']:
                continue
            rows.append({
                'id': int(r['id']),
                'first_name': r['first_name'],
                'last_name': r['last_name'],
                'strength': float(r['strength']) if r['strength'] else None,
                'learning': float(r['learning']) if r['learning'] else None,
                'integrity': int(r['integrity']) if r['integrity'] else None,
                'born': int(r['born']) if r['born'] else None,
                'terminated': int(r['terminated']) if r['terminated'] else None,
                'debut': int(r['debut']) if r['debut'] else None,
                'contract': int(r['contract']) if r['contract'] else None,
                'money': int(r['money']) if r['money'] else None,
                'points': int(r['points']) if r['points'] else None,
                'bronze_medals': int(r['bronze_medals']) if r['bronze_medals'] else None,
                'silver_medals': int(r['silver_medals']) if r['silver_medals'] else None,
                'gold_medals': int(r['gold_medals']) if r['gold_medals'] else None,
                'season_victories': int(r['season_victories']) if r['season_victories'] else None,
                'bronze_trophies': int(r['bronze_trophies']) if r['bronze_trophies'] else None,
                'silver_trophies': int(r['silver_trophies']) if r['silver_trophies'] else None,
                'gold_trophies': int(r['gold_trophies']) if r['gold_trophies'] else None,
                'championships': int(r['championships']) if r['championships'] else None,
                'grandmasters': int(r['grandmasters']) if r['grandmasters'] else None,
                'league_id': int(r['league_id']) if r['league_id'] else None,
                'parent_id': int(r['parent_id']) if r['parent_id'] else None,
                'color': r['color']
            })
        op.bulk_insert(
            table('blobs',
                  column('id', Integer), column('first_name', String), column('last_name', String),
                  column('strength', Float), column('learning', Float), column('integrity', Integer),
                  column('born', BigInteger), column('terminated', BigInteger), column('debut', Integer),
                  column('contract', Integer), column('money', Integer), column('points', Integer),
                  column('bronze_medals', Integer), column('silver_medals', Integer), column('gold_medals', Integer),
                  column('season_victories', Integer), column('bronze_trophies', Integer), column('silver_trophies', Integer),
                  column('gold_trophies', Integer), column('championships', Integer), column('grandmasters', Integer),
                  column('league_id', Integer), column('parent_id', Integer), column('color', String),
                  schema='BCS'),
            rows,
            multiinsert=False
        )

    # Calendar
    with open(os.path.join(data_dir, 'calendar_202506272255.csv'), encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [
            dict(date=int(r['date']), league_id=int(r['league_id']), concluded=bool(int(r['concluded'])), event_type=r['event_type'])
            for r in reader if r['date']
        ]
        op.bulk_insert(
            table('calendar',
                  column('date', BigInteger), column('league_id', Integer), column('concluded', Boolean), column('event_type', String),
                  schema='BCS'),
            rows,
            multiinsert=False
        )

    # Events
    with open(os.path.join(data_dir, 'events_202506272255.csv'), encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [
            dict(
                id=int(r['id']),
                league_id=int(r['league_id']),
                date=int(r['date']) if r['date'] else None,
                season=int(r['season']),
                round=int(r['round']),
                type=r['type']
            )
            for r in reader if r['id']
        ]
        op.bulk_insert(
            table('events',
                  column('id', Integer), column('league_id', Integer), column('date', BigInteger),
                  column('season', Integer), column('round', Integer), column('type', String),
                  schema='BCS'),
            rows,
            multiinsert=False
        )

    # Actions
    with open(os.path.join(data_dir, 'actions_202506272254.csv'), encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [
            dict(
                id=int(r['id']),
                event_id=int(r['event_id']),
                tick=int(r['tick']),
                blob_id=int(r['blob_id']),
                score=float(r['score'])
            )
            for r in reader if r['id']
        ]
        op.bulk_insert(
            table('actions',
                  column('id', Integer), column('event_id', Integer), column('tick', Integer),
                  column('blob_id', Integer), column('score', Float),
                  schema='BCS'),
            rows,
            multiinsert=False
        )

    # Results
    with open(os.path.join(data_dir, 'results_202506272256.csv'), encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [
            dict(
                id=int(r['id']),
                event_id=int(r['event_id']),
                blob_id=int(r['blob_id']),
                position=int(r['position']),
                points=int(r['points'])
            )
            for r in reader if r['id']
        ]
        op.bulk_insert(
            table('results',
                  column('id', Integer), column('event_id', Integer), column('blob_id', Integer),
                  column('position', Integer), column('points', Integer),
                  schema='BCS'),
            rows,
            multiinsert=False
        )

    # Sim Data
    with open(os.path.join(data_dir, 'sim_data_202506272256.csv'), encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [dict(id=int(r['id']), sim_time=int(r['sim_time']), factory_progress=int(r['factory_progress'])) for r in reader if r['id']]
        op.bulk_insert(
            table('sim_data',
                  column('id', Integer), column('sim_time', BigInteger), column('factory_progress', Integer),
                  schema='BCS'),
            rows,
            multiinsert=False
        )

    # Name Suggestions
    with open(os.path.join(data_dir, 'name_suggestions_202506272256.csv'), encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [
            dict(
                id=int(r['id']),
                first_name=r['first_name'],
                last_name=r['last_name'],
                parent_id=int(r['parent_id']) if r['parent_id'] else None,
                created=r['created']
            )
            for r in reader if r['id']
        ]
        op.bulk_insert(
            table('name_suggestions',
                  column('id', Integer), column('first_name', String), column('last_name', String),
                  column('parent_id', Integer), column('created', String),
                  schema='BCS'),
            rows,
            multiinsert=False
        )

    # Users (not in BCS schema)
    with open(os.path.join(data_dir, 'users_202506272256.csv'), encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [dict(id=int(r['id']), name=r['name'], email=r['email'], password=r['password']) for r in reader if r['id']]
        op.bulk_insert(
            table('users',
                  column('id', Integer), column('name', String), column('email', String), column('password', String), schema='BCS'),
            rows,
            multiinsert=False
        )


def downgrade() -> None:
    # Remove inserted data by primary key
    conn = op.get_bind()
    conn.execute("DELETE FROM users")
    for tbl in [
            'name_suggestions', 'sim_data', 'results', 'actions', 'events', 'calendar', 'blobs', 'leagues'
    ]:
        conn.execute(f"DELETE FROM \"BCS\".\"{tbl}\"")
