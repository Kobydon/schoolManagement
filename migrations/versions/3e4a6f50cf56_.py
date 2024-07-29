"""empty message

Revision ID: 3e4a6f50cf56
Revises: ce7a0fcc0bd9
Create Date: 2024-07-29 07:10:18.934145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e4a6f50cf56'
down_revision = 'ce7a0fcc0bd9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('broad_sheet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('numeracy', sa.String(length=400), nullable=True))
        batch_op.add_column(sa.Column('writing', sa.String(length=400), nullable=True))
        batch_op.add_column(sa.Column('literacy', sa.String(length=400), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('broad_sheet', schema=None) as batch_op:
        batch_op.drop_column('literacy')
        batch_op.drop_column('writing')
        batch_op.drop_column('numeracy')

    # ### end Alembic commands ###
