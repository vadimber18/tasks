"""init

Revision ID: fc83e82b887f
Revises: 
Create Date: 2022-03-03 15:48:42.050745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc83e82b887f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('processing_time', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('new', 'processing', 'completed', 'error', name='taskstatus'), nullable=False),
    sa.Column('cpu_bound', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    # ### end Alembic commands ###
