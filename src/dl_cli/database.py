# dl_cli/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dl_cli.models import Base
from dl_cli.config import DB_PATH
from contextlib import contextmanager

# Create the engine
engine = create_engine(f"sqlite:///{DB_PATH}")

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize the database connection and create tables if they do not exist."""
    print(f"Initializing database at: sqlite:///{DB_PATH}")  # Debugging
    Base.metadata.create_all(engine)


@contextmanager
def get_db_session():
    """Provide a transactional scope for a database session."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# This will ensure tables are created when the module is imported (e.g., by your CLI)
# If you prefer to explicitly call it, remove this line and make sure your CLI calls init_db()
init_db()

# It's better to manage sessions via get_db_session() context manager rather than a global db_instance for operations.
# The original _db: Engine | None = db line in RootDbManager used a global engine, which is fine for table creation,
# but actual CRUD operations need a session.
