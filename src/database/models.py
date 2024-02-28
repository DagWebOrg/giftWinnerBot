from typing import List
from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey

from .tools import DatabaseManager 

class Base(DeclarativeBase):
    pass

class ObservedAccount(Base):
    __tablename__ = "observed_account"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    # def __repr__(self) -> str:
    #     return f"{self.name}"
    
class BotUser(Base):
    __tablename__ = "bot_user"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)

    # def __repr__(self) -> str:
    #     return f"{self.id}"
    

def apply_models():
    Base.metadata.create_all(DatabaseManager().engine)