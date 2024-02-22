from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from .models import ObservedAccount

from .tools import DatabaseManager


class CRUD():
    @staticmethod
    def loginfo():
        with DatabaseManager() as session:
            result = session.query(ObservedAccount)
            print(result)

    
