"""Hotfix

Revision ID: 97d847025f7c
Revises: f6e2a9028f2e
Create Date: 2022-06-30 02:05:52.585411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97d847025f7c'
down_revision = 'f6e2a9028f2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('comment', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'comment')
    # ### end Alembic commands ###
