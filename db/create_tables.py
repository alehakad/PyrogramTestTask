from sqlalchemy.ext.declarative import declarative_base
from .connection import Session, engine


def create_tables():
    Base = declarative_base()
    Base.metadata.create_all(bind=engine)
