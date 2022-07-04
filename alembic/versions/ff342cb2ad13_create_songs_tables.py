"""create_songs_tables

Revision ID: ff342cb2ad13
Revises: 75f6e8e987fa
Create Date: 2022-07-04 23:33:00.251578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff342cb2ad13'
down_revision = '75f6e8e987fa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "songs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("duration", sa.Integer, nullable=False),
        sa.Column("url", sa.String, nullable=False)
    )
    op.create_table(
        "genres",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False)
    )
    op.create_table(
        "artists",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False)
    )
    op.create_table(
        "song_has_genre",
        sa.Column("song_id", sa.Integer, sa.ForeignKey("songs.id")),
        sa.Column("genre_id", sa.Integer, sa.ForeignKey("genres.id")),
        sa.PrimaryKeyConstraint("song_id", "genre_id")
    )
    op.create_table(
        "song_has_artist",
        sa.Column("song_id", sa.Integer, sa.ForeignKey("songs.id")),
        sa.Column("artist_id", sa.Integer, sa.ForeignKey("artists.id")),
        sa.PrimaryKeyConstraint("song_id", "artist_id")
    )

def downgrade() -> None:
    op.drop_table("song_has_artist")
    op.drop_table("song_has_genre")
    op.drop_table("artists")
    op.drop_table("genres")
    op.drop_table("songs")
