"""remove client_id from product

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-03-15 01:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('fk_product_client_id', 'product', type_='foreignkey')
    op.drop_column('product', 'client_id')


def downgrade() -> None:
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
