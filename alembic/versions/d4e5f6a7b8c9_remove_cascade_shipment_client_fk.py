"""remove cascade shipment client fk

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-03-15 03:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('shipment_client_id_fkey', 'shipment', type_='foreignkey')
    op.create_foreign_key(
        'shipment_client_id_fkey',
        'shipment', 'client',
        ['client_id'], ['id'],
    )


def downgrade() -> None:
    op.drop_constraint('shipment_client_id_fkey', 'shipment', type_='foreignkey')
    op.create_foreign_key(
        'shipment_client_id_fkey',
        'shipment', 'client',
        ['client_id'], ['id'],
        ondelete='CASCADE',
    )
