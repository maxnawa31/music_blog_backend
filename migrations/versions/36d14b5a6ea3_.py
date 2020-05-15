"""empty message

Revision ID: 36d14b5a6ea3
Revises: 795b9589761f
Create Date: 2019-11-27 10:03:28.224295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36d14b5a6ea3'
down_revision = '795b9589761f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userprofile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('followers_assoc',
    sa.Column('follower', sa.Integer(), nullable=True),
    sa.Column('followed_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_by'], ['userprofile.user_id'], ),
    sa.ForeignKeyConstraint(['follower'], ['userprofile.user_id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers_assoc')
    op.drop_table('userprofile')
    # ### end Alembic commands ###
