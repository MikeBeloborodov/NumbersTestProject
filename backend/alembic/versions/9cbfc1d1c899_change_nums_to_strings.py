"""change nums to strings

Revision ID: 9cbfc1d1c899
Revises: 09a5181c7ff4
Create Date: 2022-06-23 10:02:22.531788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cbfc1d1c899'
down_revision = '09a5181c7ff4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'order_table_num', type_=sa.String())
    op.alter_column('orders', 'order_num', type_=sa.String())
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'order_table_num', type_=sa.Integer())
    op.alter_column('orders', 'order_num', type_=sa.Integer())
    pass
    # ### end Alembic commands ###
