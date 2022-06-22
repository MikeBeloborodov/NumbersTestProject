"""empty message

Revision ID: 60f46ddb8f98
Revises: 3a5e27ed83d4
Create Date: 2022-06-22 10:39:49.041434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60f46ddb8f98'
down_revision = '3a5e27ed83d4'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('orders', 'delivery_date', type_=sa.String())
    pass


def downgrade():
    op.alter_column('orders', 'delivery_date', type_=sa.Date())
    pass
