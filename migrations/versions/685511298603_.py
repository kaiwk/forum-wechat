"""empty message

Revision ID: 685511298603
Revises: e80fd3303126
Create Date: 2018-12-09 23:46:07.301252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '685511298603'
down_revision = 'e80fd3303126'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('followings', sa.Column('following_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'followings', 'user', ['following_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'followings', type_='foreignkey')
    op.drop_column('followings', 'following_id')
    # ### end Alembic commands ###
