"""empty message

Revision ID: 4f3b1997a33b
Revises: 57e0d42d0cde
Create Date: 2024-04-16 14:15:55.789481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f3b1997a33b'
down_revision = '57e0d42d0cde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('grading', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=400), nullable=True))

    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.add_column(sa.Column('district', sa.String(length=400), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.drop_column('district')

    with op.batch_alter_table('grading', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###
