"""empty message

Revision ID: 5a0ec28c5114
Revises: 75d148214081
Create Date: 2020-01-07 13:55:08.043137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a0ec28c5114'
down_revision = '75d148214081'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('favoritor_assoc_favoriter_fkey', 'favoritor_assoc', type_='foreignkey')
    op.create_foreign_key(None, 'favoritor_assoc', 'users', ['favoriter'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'favoritor_assoc', type_='foreignkey')
    op.create_foreign_key('favoritor_assoc_favoriter_fkey', 'favoritor_assoc', 'userprofile', ['favoriter'], ['user_id'])
    # ### end Alembic commands ###
