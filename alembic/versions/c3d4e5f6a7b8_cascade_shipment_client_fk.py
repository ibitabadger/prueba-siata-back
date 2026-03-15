"""cascade shipment client fk

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-03-15 02:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, Sequence[str], None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('shipment_client_id_fkey', 'shipment', type_='foreignkey')
    op.create_foreign_key(
        'shipment_client_id_fkey',
        'shipment', 'client',
        ['client_id'], ['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    op.drop_constraint('shipment_client_id_fkey', 'shipment', type_='foreignkey')
    op.create_foreign_key(
        'shipment_client_id_fkey',
        'shipment', 'client',
        ['client_id'], ['id'],
    )
