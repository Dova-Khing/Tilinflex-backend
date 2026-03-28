from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

load_dotenv()

from API.database.config import Base  # noqa: E402
from API.src.entities import usuarios  # noqa: F401, E402
from API.src.entities import suscripciones  # noqa: F401, E402
from API.src.entities import obras  # noqa: F401, E402
from API.src.entities import categoria  # noqa: F401, E402
from API.src.entities import detalle_suscripcion  # noqa: F401, E402
from API.src.entities import perfil  # noqa: F401, E402
from API.src.entities import generos  # noqa: F401, E402
from API.src.entities import historial_reproduccion  # noqa: F401, E402

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connect_args = {"sslmode": os.getenv("DB_SSLMODE", "require")}
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
