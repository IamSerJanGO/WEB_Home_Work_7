"""Init

Revision ID: 29ce8e75ec0b
Revises: d69232d83cea
Create Date: 2023-12-09 00:34:43.320938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29ce8e75ec0b'
down_revision: Union[str, None] = 'd69232d83cea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teacher_subject_association')
    op.add_column('subjects', sa.Column('teacher_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'subjects', 'teachers', ['teacher_id'], ['teacher_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'subjects', type_='foreignkey')
    op.drop_column('subjects', 'teacher_id')
    op.create_table('teacher_subject_association',
    sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('subject_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], name='teacher_subject_association_subject_id_fkey'),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.teacher_id'], name='teacher_subject_association_teacher_id_fkey')
    )
    # ### end Alembic commands ###
