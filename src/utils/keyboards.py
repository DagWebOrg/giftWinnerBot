from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

class KeyboardStorage():
    @staticmethod
    def initial():
        return ReplyKeyboardMarkup(keyboard=[[
            KeyboardButton(text='Список рабочих аккаунтов 📝'),
            KeyboardButton(text='Список отслеживаемых аккаунтов 👁'),
        ],[
            KeyboardButton(text='Информация о розыгрышах 🛍'),
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
    def kb_for_return():
        return ReplyKeyboardMarkup(keyboard=[[
            KeyboardButton(text='Вернуться на главную 🏚'),
        ]])