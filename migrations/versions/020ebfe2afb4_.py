"""empty message

Revision ID: 020ebfe2afb4
Revises: d41c65ac3674
Create Date: 2020-07-13 02:18:04.916657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '020ebfe2afb4'
down_revision = 'd41c65ac3674'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('review', sa.Column('pitch_review', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('review', 'pitch_review')
    # ### end Alembic commands ###
