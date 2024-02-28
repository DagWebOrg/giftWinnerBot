from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from .models import ObservedAccount
from .tools import DatabaseManager
from settings import ALLOWED_USERS
from .models import BotUser


class CRUD():
    
    @staticmethod
    def loginfo():
        with DatabaseManager() as session:
            result = session.query(ObservedAccount)
            print(result)
    
    @staticmethod
    def get_users():
        with DatabaseManager() as session:
            try:
                users = session.query(BotUser).all()
                session.expunge_all()
                users = [item.id for item in users]
                return users
            except Exception as e:
                raise ValueError('Не удалось получить элемент. Что-то пошло не так.')
    
    @staticmethod
    def create_user(id):
        with DatabaseManager() as session:
            try:
                new_bot_user = BotUser(id = id)
                session.add(new_bot_user)
                session.commit()
            except Exception as e:
                print(e)
                raise ValueError('Что-то не так с БД.')

