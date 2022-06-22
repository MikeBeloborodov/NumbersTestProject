"""empty message

Revision ID: 3a5e27ed83d4
Revises: fd066ff70050
Create Date: 2022-06-22 04:01:15.087714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a5e27ed83d4'
down_revision = 'fd066ff70050'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('orders', 'price_rub', type_=sa.Float())
    op.alter_column('orders', 'price_usd', type_=sa.Float())
    pass


def downgrade():
    op.alter_column('orders', 'price_rub', type_=sa.Integer())
    op.alter_column('orders', 'price_usd', type_=sa.Integer())
    pass
