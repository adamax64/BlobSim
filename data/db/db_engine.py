from contextlib import contextmanager
from functools import wraps
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import inspect

from dotenv import load_dotenv
load_dotenv()

POSTGRES_USER = os.environ.get("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "bcs_database")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")

DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(DB_URL)

# Create the base class for declarative models
Base = declarative_base()

Session = sessionmaker(bind=engine)


# Define a model for your data
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'BCS'}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)


from data.model import action, blob, calendar, event, event_type, league, result, sim_data, name_suggestion  # noqa: F401, E402


def create_session():
    return Session()


@contextmanager
def transaction_scope():
    session = create_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def transactional(func):
    """ Decorator that creates a new session if one is not provided """

    def is_session_in_args(args):
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        if 'session' in params:
            session_index = params.index('session')
            return len(args) > session_index and args[session_index] is not None

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'session' in kwargs and kwargs['session'] is not None or is_session_in_args(args):
            # Use the existing session
            return func(*args, **kwargs)
        else:
            # Create a new session
            with transaction_scope() as session:
                return func(*args, session=session, **kwargs)
    return wrapper
