from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Enum, DateTime, Boolean, BigInteger
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True, nullable=False)
    trigger_message = Column(Boolean, default=False)
    registration_time = Column(DateTime(timezone=True), server_default=func.now())
    state = Column(Enum("start", "first", "second", "finished", name="user_state"), default="start")
