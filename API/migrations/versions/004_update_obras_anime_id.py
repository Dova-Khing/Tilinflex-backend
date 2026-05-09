"""Add anime_id field to obras (replaces legacy column)

Revision ID: 004
Revises: 003
Create Date: 2026-05-08

"""
from alembic import op
import sqlalchemy as sa

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def _column_exists(conn, table, column):
    result = conn.execute(
        sa.text(
            "SELECT 1 FROM information_schema.columns "
            "WHERE table_name=:t AND column_name=:c"
        ),
        {"t": table, "c": column},
    ).fetchone()
    return result is not None


def upgrade():
    conn = op.get_bind()
    # Renombra la columna legacy si aún existe con el nombre viejo
    if _column_exists(conn, "obras", "hianime_id") and not _column_exists(conn, "obras", "anime_id"):
        op.alter_column("obras", "hianime_id", new_column_name="anime_id")


def downgrade():
    conn = op.get_bind()
    if _column_exists(conn, "obras", "anime_id") and not _column_exists(conn, "obras", "hianime_id"):
        op.alter_column("obras", "anime_id", new_column_name="hianime_id")
