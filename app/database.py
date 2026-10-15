
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Carrega as variáveis do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "A variável DATABASE_URL não foi configurada no arquivo .env"
    )

# Cria a conexão com o PostgreSQL.
# pool_pre_ping verifica se a conexão ainda está válida.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Cada requisição poderá utilizar sua própria sessão.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Classe base utilizada pelos modelos ORM.
Base = declarative_base()


def get_db():
    """Fornece uma sessão e garante seu fechamento."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
