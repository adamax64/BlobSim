"""reset autoincrement for tables

Revision ID: 7f710ea02f24
Revises: d1429827152b
Create Date: 2025-07-02 22:14:27.621500

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7f710ea02f24'
down_revision: Union[str, None] = 'd1429827152b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("SELECT setval('\"BCS\".actions_id_seq', COALESCE((SELECT MAX(id) FROM \"BCS\".actions), 1), true);")
    op.execute("SELECT setval('\"BCS\".blobs_id_seq', COALESCE((SELECT MAX(id) FROM \"BCS\".blobs), 1), true);")
    op.execute("SELECT setval('\"BCS\".events_id_seq', COALESCE((SELECT MAX(id) FROM \"BCS\".events), 1), true);")
    op.execute("SELECT setval('\"BCS\".leagues_id_seq', COALESCE((SELECT MAX(id) FROM \"BCS\".leagues), 1), true);")
    op.execute("SELECT setval('\"BCS\".results_id_seq', COALESCE((SELECT MAX(id) FROM \"BCS\".results), 1), true);")
    op.execute("SELECT setval('\"BCS\".name_suggestions_id_seq', COALESCE((SELECT MAX(id) FROM \"BCS\".name_suggestions), 1), true);")


def downgrade() -> None:
    pass
