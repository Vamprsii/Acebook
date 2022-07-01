"""Drafts table

Revision ID: 88a0f788e358
Revises: 97d847025f7c
Create Date: 2022-06-30 02:43:31.224212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88a0f788e358'
down_revision = '97d847025f7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('drafts',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('users_ids', sa.ARRAY(
                        sa.Integer), nullable=True),
                    sa.Column('title', sa.String(length=100), nullable=True),
                    sa.Column('content', sa.TEXT(), nullable=True),
                    sa.Column('status', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('drafts')
    # ### end Alembic commands ###
