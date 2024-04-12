"""empty message

Revision ID: ca7fb4991ab3
Revises: e95c80303fe9
Create Date: 2024-04-09 16:59:13.480507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca7fb4991ab3'
down_revision = 'e95c80303fe9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.add_column(sa.Column('job_grade', sa.String(length=400), nullable=True))
        batch_op.add_column(sa.Column('current_management_unit', sa.String(length=400), nullable=True))
        batch_op.add_column(sa.Column('payroll_status', sa.String(length=400), nullable=True))
        batch_op.add_column(sa.Column('at_post', sa.String(length=400), nullable=True))
        batch_op.add_column(sa.Column('onleave_type', sa.String(length=400), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.drop_column('onleave_type')
        batch_op.drop_column('at_post')
        batch_op.drop_column('payroll_status')
        batch_op.drop_column('current_management_unit')
        batch_op.drop_column('job_grade')

    # ### end Alembic commands ###