from typing import Optional

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from sqlalchemy import String, ForeignKey, DateTime, TIMESTAMP
import datetime

from .tools import DatabaseManager 


class Base(DeclarativeBase):
    pass


class TrackingAccount(Base):
    __tablename__ = "tracking_account"
    __table_args__ = {'extend_existing': True}

    account_id: Mapped[str] = mapped_column(primary_key=True)
    alias: Mapped[str] = mapped_column(String(100), unique=True)
    last_scan_data: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())

    # def __repr__(self) -> str:
    #     return f"{self.name}"


class WorkAccount(Base):
    __tablename__ = "work_account"
    __table_args__ = {'extend_existing': True}

    # Служебный id.
    id: Mapped[int] = mapped_column(primary_key=True)
    alias: Mapped[str] = mapped_column(String(100), unique=True)
    login: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(100), unique=True)

    # def __repr__(self) -> str:
    #     return f"{self.alias}"


class ServiceToken(Base):
    __tablename__ = "service_token"
    __table_args__ = {'extend_existing': True}

    # Служебный id.
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(500), unique=True)

    # def __repr__(self) -> str:
    #     return f"{self.alias}"

class BotUser(Base):
    __tablename__ = "bot_user"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)

    # def __repr__(self) -> str:
    #     return f"{self.id}"


class GiftPost(Base):
    __tablename__ = "gift_post"
    __table_args__ = {'extend_existing': True}

    post_id: Mapped[str] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(100), nullable=True)

    
def apply_models():
    Base.metadata.create_all(DatabaseManager().engine)
