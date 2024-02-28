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
            'name': os.getenv('DB_NAME'),
            'url': os.getenv('DB_URL'), 
        },
        'user': {
            'username': os.getenv('DB_USERNAME'),
            'password': os.getenv('DB_PASSWORD'),
        }
    }
}