"""empty message

Revision ID: cc9f8b1a35ad
Revises: c519658d5249
Create Date: 2024-06-11 09:23:08.739490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc9f8b1a35ad'
down_revision = 'c519658d5249'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('broad_sheet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('promotion_status', sa.String(length=400), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('broad_sheet', schema=None) as batch_op:
        batch_op.drop_column('promotion_status')

    # ### end Alembic commands ###
