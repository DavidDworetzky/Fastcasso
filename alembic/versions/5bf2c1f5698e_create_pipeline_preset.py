"""create_pipeline_preset

Revision ID: 5bf2c1f5698e
Revises: 
Create Date: 2022-12-21 15:33:38.444034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bf2c1f5698e'
down_revision = None
branch_labels = None
depends_on = None



def upgrade() -> None:
    op.create_table(
        'pipeline_preset',
        sa.Column('pipeline_preset_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('model_id', sa.String(), nullable=False),
        sa.Column('inference_steps', sa.Integer, nullable=False),
        sa.Column('default_width', sa.Integer, nullable=False),
        sa.Column('default_height', sa.Integer, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('pipeline_preset')
