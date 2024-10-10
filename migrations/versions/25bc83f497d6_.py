"""empty message

Revision ID: 25bc83f497d6
Revises: 77abc459a351
Create Date: 2024-10-10 10:00:48.308475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25bc83f497d6'
down_revision = '77abc459a351'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('class', schema=None) as batch_op:
        batch_op.add_column(sa.Column('grade', sa.String(length=400), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('class', schema=None) as batch_op:
        batch_op.drop_column('grade')

    # ### end Alembic commands ###