"""Add avatar_url to perfiles

Revision ID: 006
Revises: 005
Create Date: 2026-05-09

"""
from alembic import op
import sqlalchemy as sa

revision = "006"
down_revision = "005"
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
    if not _column_exists(conn, "perfiles", "avatar_url"):
        op.add_column("perfiles", sa.Column("avatar_url", sa.String(200), nullable=True, server_default="av1"))


def downgrade():
    conn = op.get_bind()
    if _column_exists(conn, "perfiles", "avatar_url"):
        op.drop_column("perfiles", "avatar_url")
