"""empty message

Revision ID: 4073d0cef881
Revises: 472ceac554a5
Create Date: 2024-02-27 17:20:33.792366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4073d0cef881'
down_revision = '472ceac554a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('class', schema=None) as batch_op:
        batch_op.alter_column('staff_id',
               existing_type=sa.VARCHAR(length=400),
               type_=sa.Integer(),
               existing_nullable=True)

    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.alter_column('department_name',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=400),
               existing_nullable=True)

    with op.batch_alter_table('grading', schema=None) as batch_op:
        batch_op.alter_column('subject_name',
               existing_type=sa.VARCHAR(length=5000),
               type_=sa.String(length=400),
               existing_nullable=True)
        batch_op.alter_column('exams_score',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=400),
               existing_nullable=True)
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.alter_column('subject_name',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=400),
               existing_nullable=True)

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('school_name', sa.String(length=400), nullable=True))
        batch_op.create_foreign_key(None, 'school', ['school_name'], ['school_name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('school_name')

    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.alter_column('subject_name',
               existing_type=sa.String(length=400),
               type_=sa.INTEGER(),
               existing_nullable=True)

    with op.batch_alter_table('grading', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'payment', ['exams_score'], ['id'])
        batch_op.alter_column('exams_score',
               existing_type=sa.String(length=400),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('subject_name',
               existing_type=sa.String(length=400),
               type_=sa.VARCHAR(length=5000),
               existing_nullable=True)

    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.alter_column('department_name',
               existing_type=sa.String(length=400),
               type_=sa.INTEGER(),
               existing_nullable=True)

    with op.batch_alter_table('class', schema=None) as batch_op:
        batch_op.alter_column('staff_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=400),
               existing_nullable=True)

    # ### end Alembic commands ###
