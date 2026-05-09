"""Change avatar_url to TEXT to support base64 images

Revision ID: 007
Revises: 006
Create Date: 2026-05-09

"""
from alembic import op
import sqlalchemy as sa

revision = "007"
down_revision = "006"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("perfiles", "avatar_url", type_=sa.Text(), existing_nullable=True)


def downgrade():
    op.alter_column("perfiles", "avatar_url", type_=sa.String(200), existing_nullable=True)
