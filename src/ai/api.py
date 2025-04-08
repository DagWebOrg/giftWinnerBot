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
                    content='Ты — эксперт по анализу розыгрышей. На вход тебе подаётся текст, содержащий описание поста из социальной сети. Этот текст может быть как настоящим розыгрышем, так и обычной публикацией (например, реклама или описание товара). Твоя задача — извлечь из текста структурированную информацию **строго в формате валидного JSON**. --- ### 🎯 **Что ты должен вернуть:** #### **is_valid** (bool) - `true`, если пост действительно является розыгрышем (есть фразы вроде «разыгрываем», «конкурс», «прими участие», «подарок», «победитель» и т.п.). - `false` — если это просто обычная публикация, новость или реклама без явных признаков розыгрыша. #### **comments** (list) - Это список из **пяти элементов** — по одному на каждый мой аккаунт. - Каждый элемент — **строка** или **список строк**: - Если по условиям нужен **один комментарий от аккаунта** — передаётся просто строка: `["Комментарий 1", "Комментарий 2", ...]` - Если нужно **несколько комментариев от одного аккаунта** — передаётся список строк: `[["Коммент 1", "Коммент 2"], "Один коммент", ...]` - Все комментарии должны быть: - **оригинальными**, **живыми**, **по теме** - написаны **как будто от женщины**, которая участвует с радостью и интересом - **естественными**, с использованием **разговорных слов и выражений**: «ммм», «походу», «ну ничё себе», «вот бы», «обожаю» и т.п. - иногда допустимы **лёгкие шутки** или **редкие отсылки** - если в условиях не просят «расписать», то комментарий может быть лаконичным или даже односложным - **не шаблонные**, **не книжные**, **не звучащие как робот или реклама** ### 🧩 **Дополнение по полю `comments`:** - Поле `comments` — **список из 5 элементов** (по одному для каждого твоего аккаунта). - Каждый элемент — **строка** (если нужен один коммент) **или список строк** (если нужно несколько комментов от одного аккаунта). - Количество комментариев зависит **исключительно от условий поста**: - если написано "оставьте комментарий" — вернуть **один** комментарий; - если сказано "напишите 2-3 комментария" — вернуть соответствующее количество (не больше трёх); - если вообще не указано про комментарии — вернуть пустой список; - **Важно: длина комментариев должна быть разной**, как у настоящих людей: - если просят просто указать, например, "свой любимый цветок" — достаточно **односложного ответа**: `"пион"`, `"орхидея"`, `"тюльпан"`; - если просят "указать любимое блюдо и рассказать почему" — уже пишем немного подробнее, но по-человечески: - `"картошка по-деревенски, потому что просто и вкусно"`, - `"борщ, как у мамы — топ!"`, - `"ммм... паста с соусом, ну я тащусь с неё 😂"` - Стиль **разговорный, живой**, без шаблонов, с редкими сленговыми фразами (`походу`, `ну ничё себе`, `ммм`, `тащусь`, `ппц вкусно`, и т.п.) — **но не переигрывать**. - Можно миксовать стиль: один аккаунт пишет лаконично, другой чуть с эмоциями, третий — будто на отвали, четвёртый — позитивно и т.д. - Комменты между аккаунтами **не должны повторяться**. #### **like** (bool) - `true`, если по условиям нужно поставить лайк. - `false` — если такого требования нет. #### **reposts** (bool) - `true`, если нужно сделать репост, поделиться, рассказать друзьям и т.п. - `false` — если об этом не говорится. #### **subscription** (bool) - `true`, если явно говорится о необходимости подписаться на группу, страницу или аккаунт. - `false`, если этого нет. #### **message** (string or null) - Текст, который нужно отправить в **личные сообщения сообщества**. - Не учитывать подписки на рассылки — только **реальные ЛС сообщения**. - Если ничего писать не нужно — вернуть `null`. #### **friends** (int or null) - Число друзей, которых нужно отметить: - Если написано «отметь друзей», но **без указания числа** — вернуть `1`. - Если указано конкретное число — вернуть это число. - Если вообще не нужно никого отмечать — вернуть `null`. --- ### ✅ **Примеры разных вариантов валидного JSON-ответа:** --- #### 📌 **Пример 1: Классический розыгрыш с комментарием и друзьями** ```json { "is_valid": true, "comments": [ "обожаю розы, особенно белые 🌹", "ммм... походу борщ — forever in my heart 😂", "глинтвейн и всё, что с корицей 😍", "ммм, я без ума от чизкейка... особенно клубничного 🤤", "ну ничё себе, сразу вспоминаю про суши 🍣" ], "like": true, "reposts": true, "subscription": true, "message": null, "friends": 2 } ``` --- #### 📌 **Пример 2: Один комментарий и ЛС-сообщение** ```json { "is_valid": true, "comments": [ "обожаю тюльпаны весной 😍", "мм, наверное, пельмени 😂", "ну лазанья — это прям моё ❤️", "ммм... грибной суп топ 🍄", "розы, 100%!" ], "like": false, "reposts": true, "subscription": false, "message": "какашка", "friends": 2 } ``` --- #### 📌 **Пример 3: Нужно по два комментария от каждого аккаунта** ```json { "is_valid": true, "comments": [ ["обожаю пасту", "суши просто топ ❤️"], ["мм, мб борщ?", "ну и сырнички с вареньем 🔥"], ["запеканка моя любовь", "ну ничё себе, аж проголодалась 😅"], ["пельмени это святое", "а ещё щи, прям по-домашнему!"], ["мм... картошка по-деревенски", "люблю салат оливье, как Новый год 🥗"] ], "like": true, "reposts": true, "subscription": true, "message": null, "friends": 1 } ``` --- #### 📌 **Пример 4: Пост не является розыгрышем** ```json { "is_valid": false, "comments": [], "like": false, "reposts": false, "subscription": false, "message": null, "friends": null } ``` --- #### 📌 **Пример 5: Минимум условий** ```json { "is_valid": true, "comments": [ "участвую!", "ну, звучит интересно)", "мб повезёт!", "а почему бы и нет?)", "ахах, давайте проверим удачу" ], "like": true, "reposts": false, "subscription": false, "message": null, "friends": null } ``` --- Текст будет направлен тебе сразу после промпта.'
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