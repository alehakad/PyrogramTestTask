from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Column, String, DateTime
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, unique=True, primary_key=True)
    username = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
