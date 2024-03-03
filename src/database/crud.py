from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from .models import ObservedAccount
from .tools import DatabaseManager
from settings import ALLOWED_USERS
from .models import BotUser, WorkAccount


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
                raise ValueError(f'Ошибка БД.\n{e}')
    
    @staticmethod
    def create_user(id):
        with DatabaseManager() as session:
            try:
                new_bot_user = BotUser(id = id)
                session.add(new_bot_user)
                session.commit()
            except Exception as e:
                raise ValueError(f'Ошибка БД.\n{e}')
            
    
    @staticmethod
    def get_work_accounts():
        with DatabaseManager() as session:
            try:
                work_accounts = session.query(WorkAccount).all()
                session.expunge_all()
                work_accounts = [{'alias': item.alias,
                                'access_token': item.access_token}
                                  for item in work_accounts]
                return work_accounts
            except Exception as e:
                raise ValueError(f'Ошибка БД.\n{e}')


    @staticmethod
    def create_work_account(alias: str, access_token: str):
        with DatabaseManager() as session:
            try:
                new_work_account = WorkAccount(
                    alias = alias,
                    access_token = access_token
                )
                session.add(new_work_account)
                session.commit()
            except Exception as e:
                raise ValueError(f'Ошибка БД.\n{e}')
            
    
    @staticmethod
    def delete_work_account(alias: str):
        with DatabaseManager() as session:
            try:
                work_account = session.query(WorkAccount).filter(WorkAccount.alias == alias).one()
                session.delete(work_account)
                session.commit()
            except Exception as e:
                raise ValueError(f'Ошибка БД.\n{e}')
