"""create_users_table

Revision ID: dfed0fe40907
Revises: 
Create Date: 2022-06-08 14:06:04.445908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfed0fe40907'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
        sa.Column("username", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String,nullable = False),
        sa.Column("id", sa.Integer, nullable = False, primary_key = True),
        sa.Column("name",sa.String,nullable = False) 
    )


def downgrade() -> None:
    op.drop_table("users")
