"""empty message

Revision ID: d6aad50a2789
Revises: 19397a7efd71
Create Date: 2022-03-16 10:48:51.236070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6aad50a2789'
down_revision = '19397a7efd71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('property', sa.Column('image', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('property', 'image')
    # ### end Alembic commands ###
