import os
import sys
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(BASE_DIR)

ALLOWED_USERS = []
BOT_PASSWORD = os.getenv('BOT_PASSWORD')
CONFIG = {
    'db':{
        'info': {
            'name': os.getenv('POSTGRES_DB'),
            'url': os.getenv('POSTGRES_URL'), 
        },
        'user': {
            'username': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD'),
        }
    },
    'redis':{
        'url': 'localhost:6479',
    }
}
