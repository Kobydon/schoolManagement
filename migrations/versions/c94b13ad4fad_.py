"""empty message

Revision ID: c94b13ad4fad
Revises: 812199f9206c
Create Date: 2024-04-22 10:35:59.299722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c94b13ad4fad'
down_revision = '812199f9206c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.add_column(sa.Column('circuit', sa.String(length=400), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.drop_column('circuit')

    # ### end Alembic commands ###
