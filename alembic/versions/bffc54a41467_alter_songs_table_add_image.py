"""alter_songs_table_add_image

Revision ID: bffc54a41467
Revises: d39b66c868c8
Create Date: 2022-07-23 07:59:29.791838

"""
from doctest import FAIL_FAST
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bffc54a41467'
down_revision = 'd39b66c868c8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    default = "https://upload.wikimedia.org/wikipedia/commons/6/6a/Youtube_Music_icon.svg"
    op.add_column("songs", sa.Column("image", sa.String, nullable=True, default=default))
    op.execute("UPDATE songs SET image='%s'" % default)
    op.alter_column("songs", "image", nullable=False)

def downgrade() -> None:
    op.drop_column("songs", "image")
