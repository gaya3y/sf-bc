"""create_listening_history_table

Revision ID: d39b66c868c8
Revises: ff342cb2ad13
Create Date: 2022-07-04 23:36:08.487090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd39b66c868c8'
down_revision = 'ff342cb2ad13'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "listening_history",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("song_id", sa.Integer, sa.ForeignKey("songs.id")),
        sa.Column("start_time", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("end_time", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("listening_history")
