"""Add indexing to purchase date

Revision ID: 532aebcce76b
Revises: d5e40b49c6dc
Create Date: 2019-07-11 20:38:00.539548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '532aebcce76b'
down_revision = 'd5e40b49c6dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_purchase_date'), 'purchase', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_purchase_date'), table_name='purchase')
    # ### end Alembic commands ###
