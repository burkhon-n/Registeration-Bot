from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# PostgreSQL database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://username:password@localhost:5432/registration_bot"
)

# Convert postgresql:// to postgresql+psycopg:// for psycopg3 compatibility
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
    logger.info("Converted postgresql:// to postgresql+psycopg:// for psycopg3 driver")
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
    logger.info("Converted postgres:// to postgresql+psycopg:// for psycopg3 driver")

# Create SQLAlchemy engine
logger.info(f"Creating database engine with pool_size=5, max_overflow=10")
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10
)
logger.info("Database engine created successfully")

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Usage:
        db = next(get_db())
        try:
            # Your database operations
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database - create all tables
    """
    logger.info("Initializing database - creating all tables")
    try:
        from models.User import User  # Import your models here
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}", exc_info=True)
        raise