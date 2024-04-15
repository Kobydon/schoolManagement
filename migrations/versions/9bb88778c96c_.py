"""empty message

Revision ID: 9bb88778c96c
Revises: 3c9797818f13
Create Date: 2024-04-15 16:27:50.037272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bb88778c96c'
down_revision = '3c9797818f13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fees_payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_number', sa.String(length=400), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fees_payment', schema=None) as batch_op:
        batch_op.drop_column('student_number')

    # ### end Alembic commands ###
