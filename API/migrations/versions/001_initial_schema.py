"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-03-27

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "usuarios",
        sa.Column("id_usuario", UUID(as_uuid=True), primary_key=True),
        sa.Column("nombre", sa.String(50), nullable=False),
        sa.Column("apellido", sa.String(50), nullable=False),
        sa.Column("email", sa.String(100), nullable=False, unique=True),
        sa.Column("telefono", sa.String(20), nullable=True),
        sa.Column("edad", sa.Integer(), nullable=True),
        sa.Column("contrasena_hash", sa.String(255), nullable=False),
        sa.Column("fecha_registro", sa.DateTime(), nullable=True),
        sa.Column("fecha_actualizacion", sa.DateTime(), nullable=True),
        sa.Column("admin", sa.Boolean(), default=False),
        sa.Column("pais", sa.String(50), nullable=True),
        sa.Column("activo", sa.Boolean(), default=True),
    )

    op.create_table(
        "categorias",
        sa.Column("id_categoria", UUID(as_uuid=True), primary_key=True),
        sa.Column("nombre_categoria", sa.String(50), nullable=False, unique=True),
    )

    op.create_table(
        "generos",
        sa.Column("id_genero", UUID(as_uuid=True), primary_key=True),
        sa.Column("nombre_genero", sa.String(100), nullable=False, unique=True),
    )

    op.create_table(
        "suscripciones",
        sa.Column("id_suscripcion", UUID(as_uuid=True), primary_key=True),
        sa.Column("tipo_suscripcion", sa.String(50), nullable=False),
        sa.Column("fecha_inicio", sa.DateTime(), nullable=True),
        sa.Column("fecha_fin", sa.DateTime(), nullable=True),
        sa.Column("id_usuario", UUID(as_uuid=True), sa.ForeignKey("usuarios.id_usuario"), nullable=False, unique=True),
    )

    op.create_table(
        "obras",
        sa.Column("id_obra", UUID(as_uuid=True), primary_key=True),
        sa.Column("nombre", sa.String(150), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("episodios", sa.Integer(), nullable=False),
        sa.Column("anio", sa.Integer(), nullable=False),
        sa.Column("fecha_registro", sa.DateTime(), nullable=True),
        sa.Column("id_categoria", UUID(as_uuid=True), sa.ForeignKey("categorias.id_categoria"), nullable=False),
        sa.Column("id_genero", UUID(as_uuid=True), sa.ForeignKey("generos.id_genero"), nullable=False),
    )

    op.create_table(
        "perfiles",
        sa.Column("id_perfil", UUID(as_uuid=True), primary_key=True),
        sa.Column("nombre_usuario", sa.String(100), nullable=False),
        sa.Column("idioma", sa.String(50), nullable=False),
        sa.Column("es_infantil", sa.Boolean(), default=False),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=True),
        sa.Column("id_usuario", UUID(as_uuid=True), sa.ForeignKey("usuarios.id_usuario"), nullable=False),
    )

    op.create_table(
        "detalle_suscripcion",
        sa.Column("id_detalle_suscripcion", UUID(as_uuid=True), primary_key=True),
        sa.Column("fecha_suscripcion", sa.DateTime(), nullable=True),
        sa.Column("valor", sa.Numeric(10, 2), nullable=False),
        sa.Column("metodo_pago", sa.String(50), nullable=False),
        sa.Column("id_suscripcion", UUID(as_uuid=True), sa.ForeignKey("suscripciones.id_suscripcion"), nullable=False, unique=True),
    )

    op.create_table(
        "historial_reproduccion",
        sa.Column("id_historial", UUID(as_uuid=True), primary_key=True),
        sa.Column("tiempo_visto", sa.Integer(), nullable=False),
        sa.Column("fecha_visualizacion", sa.DateTime(), nullable=True),
        sa.Column("id_perfil", UUID(as_uuid=True), sa.ForeignKey("perfiles.id_perfil"), nullable=False),
        sa.Column("id_obra", UUID(as_uuid=True), sa.ForeignKey("obras.id_obra"), nullable=False),
    )


def downgrade():
    op.drop_table("historial_reproduccion")
    op.drop_table("detalle_suscripcion")
    op.drop_table("perfiles")
    op.drop_table("obras")
    op.drop_table("suscripciones")
    op.drop_table("generos")
    op.drop_table("categorias")
    op.drop_table("usuarios")
