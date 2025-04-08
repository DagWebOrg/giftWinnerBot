from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, DateTime
import datetime

from .tools import DatabaseManager 


class Base(DeclarativeBase):
    pass


class TrackingAccount(Base):
    __tablename__ = "tracking_account"
    __table_args__ = {'extend_existing': True}

    account_id: Mapped[str] = mapped_column(primary_key=True)
    alias: Mapped[str] = mapped_column(String(100), unique=True)
    last_scan_data: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.datetime.now(tz=datetime.timezone.utc))


class WorkAccount(Base):
    __tablename__ = "work_account"
    __table_args__ = {'extend_existing': True}

    # Служебный id.
    id: Mapped[int] = mapped_column(primary_key=True)
    alias: Mapped[str] = mapped_column(String(100), unique=True)
    login: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    account_id: Mapped[str] = mapped_column(String(100), nullable=False)


class ServiceToken(Base):
    __tablename__ = "service_token"
    __table_args__ = {'extend_existing': True}

    # Служебный id.
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(500), unique=True)


class BotUser(Base):
    __tablename__ = "bot_user"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)


class GiftPost(Base):
    __tablename__ = "gift_post"
    __table_args__ = {'extend_existing': True}

    post_id: Mapped[str] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(), nullable=True)

    
def apply_models():
    Base.metadata.create_all(DatabaseManager().engine)
