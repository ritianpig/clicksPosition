"""empty message

Revision ID: eab0af8fc470
Revises: eb36690eca01
Create Date: 2019-03-22 14:54:10.071762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eab0af8fc470'
down_revision = 'eb36690eca01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('down_json', sa.Column('switch', sa.String(length=10), nullable=True, comment='开关'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('down_json', 'switch')
    # ### end Alembic commands ###