from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.environ.get("DB_USER")
db_port = os.environ.get("POSTGRES_USER")
db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")


engine = create_engine(
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
async_engine = create_async_engine(
    f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}/{db_name}"
)


Session = sessionmaker(bind=engine)
AsyncSession = async_sessionmaker(bind=async_engine, expire_on_commit=False)
