"""create_user_circle_table

Revision ID: 75f6e8e987fa
Revises: dfed0fe40907
Create Date: 2022-07-04 23:29:36.112504

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75f6e8e987fa'
down_revision = 'dfed0fe40907'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_circle",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("following_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("is_compatible", sa.Boolean, nullable=False, default=False),
    )
    op.create_primary_key("user_circle_pkey", "user_circle", ["user_id", "following_id"])


def downgrade() -> None:
    op.drop_table("user_circle")
