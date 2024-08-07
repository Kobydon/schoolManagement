"""empty message

Revision ID: 04c79f60cc51
Revises: 09c08ca0df10
Create Date: 2024-06-23 21:15:06.755169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04c79f60cc51'
down_revision = '09c08ca0df10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.add_column(sa.Column('church_logo', sa.String(length=400), nullable=True))
        batch_op.add_column(sa.Column('report_type', sa.String(length=400), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.drop_column('report_type')
        batch_op.drop_column('church_logo')

    # ### end Alembic commands ###
