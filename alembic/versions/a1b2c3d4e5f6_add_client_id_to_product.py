"""add client_id to product

Revision ID: a1b2c3d4e5f6
Revises: 5e52c80dcb68
Create Date: 2026-03-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '5e52c80dcb68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'product',
        sa.Column('client_id', sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        'fk_product_client_id',
        'product', 'client',
        ['client_id'], ['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    op.drop_constraint('fk_product_client_id', 'product', type_='foreignkey')
    op.drop_column('product', 'client_id')
