"""disapprove_comment column at posts table

Revision ID: 170a05743ad2
Revises: 88a0f788e358
Create Date: 2022-06-30 13:38:42.600207

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '170a05743ad2'
down_revision = '88a0f788e358'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column(
        'disapprove_comment', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'disapprove_comment')
    # ### end Alembic commands ###
