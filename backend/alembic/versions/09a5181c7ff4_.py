"""empty message

Revision ID: 09a5181c7ff4
Revises: 60f46ddb8f98
Create Date: 2022-06-22 11:22:22.098057

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '09a5181c7ff4'
down_revision = '60f46ddb8f98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'order_table_num',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('orders', 'order_num',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('orders', 'price_rub',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('orders', 'price_usd',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('orders', 'delivery_date',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'delivery_date',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('orders', 'price_usd',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('orders', 'price_rub',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('orders', 'order_num',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('orders', 'order_table_num',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
