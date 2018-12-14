"""empty message

Revision ID: 5a20064c47d9
Revises: d27d86884906
Create Date: 2018-12-14 19:22:53.836381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a20064c47d9'
down_revision = 'd27d86884906'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('user', 'open_id',
                    existing_type=sa.String(length=64),
                    type_=sa.String(length=128),
                    existing_nullable=True,
                    nullable_=False)

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('title', sa.String(length=140), nullable=False))
    op.add_column('user', sa.Column('avatar', sa.String(length=200), nullable=True))
    op.add_column('user', sa.Column('nickname', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    op.alter_column('user', 'open_id',
                    existing_type=sa.String(length=128),
                    type_=sa.String(length=64),
                    existing_nullable=False,
                    nullable_=True)

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'nickname')
    op.drop_column('user', 'avatar')
    op.drop_column('question', 'title')
    # ### end Alembic commands ###
