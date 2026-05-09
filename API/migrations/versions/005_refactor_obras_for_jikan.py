"""Refactor obras table for Jikan catalog import

Revision ID: 005
Revises: 004
Create Date: 2026-05-09

"""
from alembic import op
import sqlalchemy as sa

revision = "005"
down_revision = "004"
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


def _index_exists(conn, index_name):
    result = conn.execute(
        sa.text(
            "SELECT 1 FROM pg_indexes WHERE indexname=:i"
        ),
        {"i": index_name},
    ).fetchone()
    return result is not None


def upgrade():
    conn = op.get_bind()

    # Columnas nuevas
    new_columns = [
        ("mal_id",           "INTEGER"),
        ("nombre_japones",   "VARCHAR(200)"),
        ("temporada",        "VARCHAR(20)"),
        ("rango",            "INTEGER"),
        ("duracion",         "VARCHAR(50)"),
        ("estudios",         "VARCHAR(300)"),
        ("generos_externos", "TEXT"),
    ]
    for col, col_type in new_columns:
        if not _column_exists(conn, "obras", col):
            op.add_column("obras", sa.Column(col, sa.Text() if col_type == "TEXT" else sa.String(
                int(col_type.split("(")[1].rstrip(")")) if "(" in col_type else None
            ) if col_type.startswith("VARCHAR") else sa.Integer(), nullable=True))

    # Hacer opcionales las FKs internas y campos que antes eran NOT NULL
    nullable_columns = ["episodios", "anio", "id_categoria", "id_genero"]
    for col in nullable_columns:
        if _column_exists(conn, "obras", col):
            op.alter_column("obras", col, nullable=True)

    # Ampliar nombre de 150 a 200 chars
    if _column_exists(conn, "obras", "nombre"):
        op.alter_column("obras", "nombre", type_=sa.String(200), existing_nullable=False)

    # Índice único en mal_id (solo donde no es null)
    if not _index_exists(conn, "uq_obras_mal_id"):
        op.execute("CREATE UNIQUE INDEX uq_obras_mal_id ON obras(mal_id) WHERE mal_id IS NOT NULL")


def downgrade():
    conn = op.get_bind()

    if _index_exists(conn, "uq_obras_mal_id"):
        op.execute("DROP INDEX IF EXISTS uq_obras_mal_id")

    drop_columns = ["mal_id", "nombre_japones", "temporada", "rango", "duracion", "estudios", "generos_externos"]
    for col in drop_columns:
        if _column_exists(conn, "obras", col):
            op.drop_column("obras", col)

    # Revertir nullable — solo si hay datos consistentes
    for col in ["episodios", "anio"]:
        if _column_exists(conn, "obras", col):
            op.alter_column("obras", col, nullable=False)
