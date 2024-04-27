"""empty message

Revision ID: 2668e49e5fff
Revises: e4f73713a435
Create Date: 2024-04-27 15:40:30.102807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2668e49e5fff'
down_revision = 'e4f73713a435'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favoritos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favoritos', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
