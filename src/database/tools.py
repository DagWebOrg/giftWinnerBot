import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings


class DatabaseManager:
    def __init__(self):
        self.db_name = settings.CONFIG['db']['info']['name']
        self.db_url = settings.CONFIG['db']['info']['url']
        self.db_username = settings.CONFIG['db']['user']['username']
        self.db_password = settings.CONFIG['db']['user']['password']

        self.engine = create_engine(f"postgresql+psycopg2://{self.db_username}:{self.db_password}@{self.db_url}/{self.db_name}")
        self.Session = sessionmaker(bind=self.engine)

    def __enter__(self):
        self.session = self.Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

