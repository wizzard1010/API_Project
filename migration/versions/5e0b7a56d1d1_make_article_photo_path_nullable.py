"""make article photo path nullable

Revision ID: 5e0b7a56d1d1
Revises: 2c970a175ecf
Create Date: 2026-06-09 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e0b7a56d1d1'
down_revision: Union[str, Sequence[str], None] = '2c970a175ecf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'articles',
        'photo_path',
        existing_type=sa.String(length=500),
        nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'articles',
        'photo_path',
        existing_type=sa.String(length=500),
        nullable=False,
    )
