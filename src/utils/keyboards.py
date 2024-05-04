from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class KeyboardStorage():
    @staticmethod
    def initial():
        return ReplyKeyboardMarkup(keyboard=[[
            KeyboardButton(text='Список рабочих аккаунтов 📝'),
            KeyboardButton(text='Список отслеживаемых аккаунтов 👁'),
        ],[
            KeyboardButton(text='Информация о розыгрышах 🛍'),
        ],[
            KeyboardButton(text='Добавить/обновить токен 🎛'),
        ],[
            KeyboardButton(text='Новые сообщения 📩'),
        ]])
    def work_accounts_list():
        return ReplyKeyboardMarkup(keyboard=[[
            KeyboardButton(text='Добавить новый аккаунт ✍🏻'),
            KeyboardButton(text='Удалить аккаунт ❌'),
        ],[
            KeyboardButton(text='Вернуться на главную 🏚'),
        ]])
    def tracking_accounts_list():
        return ReplyKeyboardMarkup(keyboard=[[
            KeyboardButton(text='Добавить новый аккаунт 🖌'),
            KeyboardButton(text='Удалить аккаунт 🚫'),
        ],[
            KeyboardButton(text='Вернуться на главную 🏚'),
        ]])
    def post_list():
        return ReplyKeyboardMarkup(keyboard=[[
            KeyboardButton(text='Искать новые посты 🔍'),
            KeyboardButton(text='Удалить пост 🚫'),
        ],[
            KeyboardButton(text='Репост постов на рабочие аккаунты 📋'),
        ],[
            KeyboardButton(text='Вернуться на главную 🏚'),
        ]])
    def kb_for_return():
        return ReplyKeyboardMarkup(keyboard=[[
            KeyboardButton(text='Вернуться на главную 🏚'),
        ]])