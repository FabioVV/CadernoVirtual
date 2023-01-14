"""change foreing key

Revision ID: bae2a233a4e8
Revises: bd544c293b94
Create Date: 2023-01-14 13:47:35.646274

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bae2a233a4e8'
down_revision = 'bd544c293b94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('posts_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])
        batch_op.drop_column('poster_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('poster_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('posts_ibfk_1', 'users', ['poster_id'], ['id'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
