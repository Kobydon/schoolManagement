"""empty message

Revision ID: ce49e2cfd0bd
Revises: 
Create Date: 2024-04-08 09:16:06.382758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce49e2cfd0bd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('department')
    op.drop_table('subjectb')
    op.drop_table('subjectr')
    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.add_column(sa.Column('other_name', sa.String(length=400), nullable=True))
        batch_op.drop_constraint('staff_email_key', type_='unique')
        batch_op.drop_constraint('staff_national_id_key', type_='unique')

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('other_name', sa.String(length=400), nullable=True))
        batch_op.drop_constraint('student_email_key', type_='unique')
        batch_op.drop_constraint('student_student_number_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.create_unique_constraint('student_student_number_key', ['student_number'])
        batch_op.create_unique_constraint('student_email_key', ['email'])
        batch_op.drop_column('other_name')

    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.create_unique_constraint('staff_national_id_key', ['national_id'])
        batch_op.create_unique_constraint('staff_email_key', ['email'])
        batch_op.drop_column('other_name')

    op.create_table('subjectr',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('subject_name', sa.VARCHAR(length=5000), autoincrement=False, nullable=True),
    sa.Column('department_name', sa.VARCHAR(length=5000), autoincrement=False, nullable=True),
    sa.Column('created_by_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='subjectr_created_by_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='subjectr_pkey'),
    sa.UniqueConstraint('subject_name', name='subjectr_subject_name_key')
    )
    op.create_table('subjectb',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('subject_name', sa.VARCHAR(length=5000), autoincrement=False, nullable=True),
    sa.Column('department_name', sa.VARCHAR(length=5000), autoincrement=False, nullable=True),
    sa.Column('school_name', sa.VARCHAR(length=5000), autoincrement=False, nullable=True),
    sa.Column('created_by_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='subjectb_created_by_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='subjectb_pkey'),
    sa.UniqueConstraint('subject_name', name='subjectb_subject_name_key')
    )
    op.create_table('department',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('department_name', sa.VARCHAR(length=400), autoincrement=False, nullable=True),
    sa.Column('department_head', sa.VARCHAR(length=400), autoincrement=False, nullable=True),
    sa.Column('total_teachers', sa.VARCHAR(length=400), autoincrement=False, nullable=True),
    sa.Column('total_subjects', sa.VARCHAR(length=400), autoincrement=False, nullable=True),
    sa.Column('created_by_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_date', sa.VARCHAR(length=400), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='department_created_by_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='department_pkey'),
    sa.UniqueConstraint('department_head', name='department_department_head_key'),
    sa.UniqueConstraint('department_name', name='department_department_name_key')
    )
    # ### end Alembic commands ###