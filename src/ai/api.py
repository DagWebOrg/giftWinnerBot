import logging
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Optional
from requests.exceptions import RequestException

from dotenv import load_dotenv

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

from settings import GPT_API_AUTH_KEY


load_dotenv()


class TokenManager:
    """Класс для управления токенами."""

    def __init__(self, engine, token_lifetime_buffer=60):
        """
        Инициализация TokenManager.

        :param engine: Объект для взаимодействия с внешним API (например, для получения токена).
        :param token_lifetime_buffer: Время в секундах для буфера перед истечением срока действия токена,
                                      когда он будет считаться недействительным.
        """
        self.engine = engine
        self.token_data = None
        self.token_lifetime_buffer = token_lifetime_buffer  # Буфер времени для проверки истечения срока действия токена
        self.logger = logging.getLogger(__name__)  # Логгер для отслеживания ошибок и событий

    def _get_new_token(self):
        """Получение нового токена."""
        try:
            token_info = self.engine.get_token()  # Предполагаем, что это объект AccessToken
            if not token_info:
                raise ValueError("Не удалось получить токен. Ответ пустой.")

            expires_at_timestamp = token_info.expires_at
            if expires_at_timestamp is None:
                raise ValueError("Токен не содержит информации о времени истечения срока действия.")

            expires_at_seconds = expires_at_timestamp / 1000  # Преобразуем миллисекунды в секунды
            expiration_time = datetime.now() + timedelta(seconds=expires_at_seconds)

            self.token_data = {
                'access_token': token_info.access_token,
                'expiration_time': expiration_time,
            }
            self.logger.info("Токен успешно получен и обновлен.")

        except Exception as e:
            self.logger.error(f"Ошибка при получении нового токена: {e}")
            raise

    def is_token_valid(self):
        """Проверка действительности токена."""
        if not self.token_data:
            self.logger.warning("Токен не найден.")
            return False

        current_time = datetime.now()
        expiration_time = self.token_data['expiration_time']

        if current_time + timedelta(seconds=self.token_lifetime_buffer) > expiration_time:
            self.logger.info(f"Токен истечет через менее чем {self.token_lifetime_buffer} секунд.")
            return False

        return True

    def ensure_valid_token(self):
        """Обеспечение наличия валидного токена."""
        if not self.is_token_valid():
            self.logger.info("Токен устарел или отсутствует. Запрашиваю новый.")
            self._get_new_token()

    @property
    def token(self):
        """Возвращает текущий токен."""
        self.ensure_valid_token()
        return self.token_data['access_token']


class AIDispatcher:
    def __init__(self, gpt_api_key: Optional[str] = GPT_API_AUTH_KEY, scope: str = "GIGACHAT_API_PERS",
                 verify_ssl: bool = False) -> None:
        """
        Инициализация диспетчера для работы с GPT с системным промптом.

        :param gpt_api_key: API ключ для доступа к GPT.
        :param scope: Область доступа для API.
        :param verify_ssl: Флаг для проверки SSL сертификатов.
        """
        self.logger = logging.getLogger(__name__)
        self.engine = GigaChat(
            credentials=gpt_api_key,
            scope=scope,
            verify_ssl_certs=verify_ssl
        )

        # Системный промпт устанавливаем один раз при инициализации
        self.chat_template = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content='ты — эксперт по анализу розыгрышей. на вход тебе подаётся текст, содержащий описание поста из социальной сети. этот текст может быть как настоящим розыгрышем, так и обычной публикацией (например, реклама или описание товара). твоя задача — извлечь из текста структурированную информацию строго в формате json.    вот поля, которые нужно вернуть:    - **is_valid**: булевое значение. `true`, если текст действительно похож на розыгрыш (например, есть фразы типа "разыгрываем", "прими участие", "победитель", "конкурс" и т.п.), иначе `false`.  - **comments**: список строк. каждая строка — пример комментария, который должен быть оставлен под постом согласно условиям. если комментарий не требуется — вернуть пустой список.  - **like**: булевое значение. `true`, если в тексте указано, что нужно поставить лайк, иначе `false`.  - **reposts**: булевое значение. `true`, если в тексте указано, что нужно сделать репост (или "поделиться", "рассказать друзьям"), иначе `false`.  - **subscription**: булевое значение. `true`, если в тексте указано, что нужно подписаться на группу или сообщество, иначе `false`.  - **message**: строка. сообщение, которое необходимо отправить в личные сообщения сообщества или группы для участия. если это не требуется — вернуть `null`.  - **friends**: целое число или `null`. сколько друзей нужно отметить. если написано "отметьте друга/друзей", но не указано сколько — вернуть случайное число от 1 до 3. если не требуется — вернуть `null`.    ⚠️ ответ должен быть **строго** в формате **валидного json**, без пояснений, комментариев и текста вокруг. только json.    пример валидного json-ответа:    ```json  {  "is_valid": true,  "comments": ["хочу участвовать!", "участвую!"],  "like": true,  "reposts": true,  "message": null,  "friends": 2  }  ```    текст розыгрыша будет подаваться тебе сразу после этого промпта.'
                ).dict(),
            ],
            temperature=0.7,
            max_tokens=100,
        )

        # Создаём менеджер токенов
        self.token_manager = TokenManager(self.engine)

    def chat(self, text: str) -> str:
        """
        Отправка сообщения в GPT и получение ответа, используя системный промпт.

        :param text: Сообщение для отправки в GPT.
        :return: Ответ от GPT.
        """
        try:
            # Обновляем токен перед выполнением запроса
            self.token_manager.ensure_valid_token()

            # Получаем текущий чат с добавленным системным промптом
            payload = deepcopy(self.chat_template)
            payload.messages.append(Messages(role=MessagesRole.USER, content=text).dict())

            # Отправляем запрос
            response = self.engine.chat(payload)

            # Логируем ответ
            self.logger.info(f"Ответ от GPT: {response.choices[0].message.content}")

            return response.choices[0].message.content

        except RequestException as e:
            self.logger.error(f"Ошибка при отправке запроса в GPT: {e}")
            raise  # Повторно выбрасываем исключение для обработки выше
        except Exception as e:
            self.logger.error(f"Неизвестная ошибка: {e}")
            raise  # Повторно выбрасываем исключение для обработки выше

# Пример использования
gpt = AIDispatcher()