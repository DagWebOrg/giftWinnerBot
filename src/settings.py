import os

from dotenv import load_dotenv
load_dotenv()


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