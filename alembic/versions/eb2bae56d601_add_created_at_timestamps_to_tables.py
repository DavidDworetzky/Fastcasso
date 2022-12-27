"""add created_at timestamps to tables.

Revision ID: eb2bae56d601
Revises: 5bf2c1f5698e
Create Date: 2022-12-26 23:50:43.940310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb2bae56d601'
down_revision = '5bf2c1f5698e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('image_input', sa.Column('created_at', sa.DateTime(), nullable=True, default=sa.func.now()))
    op.add_column('image_output', sa.Column('created_at', sa.DateTime(), nullable=True, default=sa.func.now()))
    op.add_column('pipeline_preset', sa.Column('created_at', sa.DateTime(), nullable=True, default=sa.func.now()))
    # update existing rows 
    op.execute("UPDATE image_input SET created_at = NOW()")
    op.execute("UPDATE image_output SET created_at = NOW()")
    op.execute("UPDATE pipeline_preset SET created_at = NOW()")
    #alter columns to be non nullable
    op.alter_column('image_input', 'created_at', nullable=False)
    op.alter_column('image_output', 'created_at', nullable=False)
    op.alter_column('pipeline_preset', 'created_at', nullable=False)

def downgrade() -> None:
    op.drop_column('pipeline_preset', 'created_at')
    op.drop_column('image_output', 'created_at')
    op.drop_column('image_input', 'created_at')
