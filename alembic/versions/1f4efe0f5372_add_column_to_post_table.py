"""add column to post table

Revision ID: 1f4efe0f5372
Revises: 489184ba2aaf
Create Date: 2024-05-26 17:29:04.207952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f4efe0f5372'
down_revision: Union[str, None] = '489184ba2aaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'posts', 
        sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
