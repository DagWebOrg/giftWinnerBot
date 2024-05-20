import os
import sys
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(BASE_DIR)

# Слова для выборки постов с наблюдаемых аккаунтов. Если хоть одно слово есть - пост подходит.
GIFT_WORDS = ['конкурс', 'розыгрыш', "дари", "репост", "побед", "билет", "абонемент", 'разыгры']

# Списки слов, по которым определяется нужно ли в посте отметить друга. Должно быть каждое слово из любого списка.
WORDS_DEFINING_THAT_POST_WITH_A_FRIENDS_MARK = [
                        ['отмет', 'друг'],
                        ['отмет', 'друз'],
                        ['отмеч', 'друз'],
                        ['отмеч', 'друг'],
                        ['отмет', 'в коммент'],
                        ['отмеч', 'в коммент'],
]

# Комментарии, которые пишутся к постам в обычных постах.
STANDART_COMMENTS = [
                        [
                            ['Участвую', 'участвую'],
                            ['Всем удачи!', 'желаю всем удачи', 'желаю удачи', 'удачи всем!!'],
                            ['Спасибо за розыгрыш', 'Ура, розыгрыш)', 'Хочу, хочу', 'Хочууу'],
                            ['Ждем результатов', 'жду результатов))', 'Жду результатов']
                        ],
                        [
                            ['Участвую', 'участвую'],
                            ['Большое спасибо за розыгрыш)))', 'пасибоо за розыгрыш', 'Ооо, точно хочу победить', 'блин, хочу выиграть..'],
                        ],
                        [
                            ['Участвую', 'участвую']
                        ]
                    ]




NUMBER_OF_SCANNED_POST_FROM_ACCOUNT = 20
FREQUENCY_OF_THE_REPOST = 1800

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
        'url': os.getenv('REDIS_URL'),
    }
}
