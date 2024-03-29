"""new tables

Revision ID: 0c414d1e3338
Revises: bae2a233a4e8
Create Date: 2023-01-14 18:26:29.277790

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0c414d1e3338'
down_revision = 'bae2a233a4e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('poster_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('posts_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['poster_id'], ['id'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('posts_ibfk_1', 'users', ['user_id'], ['id'])
        batch_op.drop_column('poster_id')

    # ### end Alembic commands ###
