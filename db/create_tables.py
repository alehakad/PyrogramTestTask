from sqlalchemy.ext.declarative import declarative_base
from .connection import engine
from .models import Base
from loguru import logger

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created")
    except:
        logger.debug("Error creating tables, maybe they already exist")