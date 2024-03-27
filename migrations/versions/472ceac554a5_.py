"""empty message

Revision ID: 472ceac554a5
Revises: 9c340c8851fd
Create Date: 2024-02-27 14:02:36.033019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '472ceac554a5'
down_revision = '9c340c8851fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.String(length=400), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.drop_column('created_date')

    # ### end Alembic commands ###
