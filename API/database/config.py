import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if not DATABASE_URL:
    raise ValueError("Se requiere DATABASE_URL en las variables de entorno")

# psycopg2 no soporta channel_binding — se elimina del URL si está presente
if "channel_binding" in DATABASE_URL:
    from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
    parsed = urlparse(DATABASE_URL)
    params = {k: v for k, v in parse_qs(parsed.query).items() if k != "channel_binding"}
    DATABASE_URL = urlunparse(parsed._replace(query=urlencode({k: v[0] for k, v in params.items()})))

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"sslmode": os.getenv("DB_SSLMODE", "require")},
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
