"""Added liked_by array column

Revision ID: cbdec367d532
Revises: 1ba1bf5c902d
Create Date: 2022-06-30 22:02:35.287749

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cbdec367d532'
down_revision = '1ba1bf5c902d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column(
        'liked_by', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'liked_by')
    # ### end Alembic commands ###
