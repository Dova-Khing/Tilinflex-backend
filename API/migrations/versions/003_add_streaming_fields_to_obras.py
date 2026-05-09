"""Add streaming fields to obras

Revision ID: 003
Revises: 002
Create Date: 2026-05-09

"""
from alembic import op
import sqlalchemy as sa

revision = "003"
down_revision = "002"
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
    new_columns = [
        ("tipo",          sa.String(20),  True,  None),
        ("hianime_id",    sa.String(150), True,  None),
        ("thumbnail_url", sa.Text(),      True,  None),
        ("banner_url",    sa.Text(),      True,  None),
        ("trailer_url",   sa.Text(),      True,  None),
        ("estado",        sa.String(30),  True,  None),
        ("puntuacion",    sa.Float(),     True,  None),
    ]
    for col_name, col_type, nullable, default in new_columns:
        if not _column_exists(conn, "obras", col_name):
            op.add_column("obras", sa.Column(col_name, col_type, nullable=nullable, server_default=default))


def downgrade():
    for col in ["tipo", "hianime_id", "thumbnail_url", "banner_url", "trailer_url", "estado", "puntuacion"]:
        op.drop_column("obras", col)
