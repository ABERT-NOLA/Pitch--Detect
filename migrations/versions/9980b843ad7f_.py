"""empty message

Revision ID: 9980b843ad7f
Revises: e02158933783
Create Date: 2020-07-13 11:38:43.206526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9980b843ad7f'
down_revision = 'e02158933783'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('category')
    # ### end Alembic commands ###