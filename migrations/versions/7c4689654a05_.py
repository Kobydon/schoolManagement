"""empty message

Revision ID: 7c4689654a05
Revises: 760100d0afb5
Create Date: 2024-05-03 10:40:48.459602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c4689654a05'
down_revision = '760100d0afb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('grading', schema=None) as batch_op:
        batch_op.add_column(sa.Column('original_class_name', sa.String(length=5000), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('grading', schema=None) as batch_op:
        batch_op.drop_column('original_class_name')

    # ### end Alembic commands ###
