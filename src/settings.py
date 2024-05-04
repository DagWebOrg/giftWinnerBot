import os
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()


ALLOWED_USERS = []

BOT_PASSWORD = os.getenv('BOT_PASSWORD')

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(BASE_DIR)

CONFIG = {
    'db':{
        'info': {
            'name': os.getenv('POSTGRES_NAME'),
            'url': os.getenv('POSTGRES_URL'), 
        },
        'user': {
            'username': os.getenv('POSTGRES_USERNAME'),
            'password': os.getenv('POSTGRES_PASSWORD'),
        }
    }
}