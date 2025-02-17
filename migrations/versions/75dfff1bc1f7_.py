"""empty message

Revision ID: 75dfff1bc1f7
Revises: 8f81f5e9d6fc
Create Date: 2023-05-06 15:50:58.251804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75dfff1bc1f7'
down_revision = '8f81f5e9d6fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###
