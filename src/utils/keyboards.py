from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

class KeyboardStorage():
    @staticmethod
    def initial():
        return ReplyKeyboardMarkup(keyboard=[[
            KeyboardButton(text='Список рабочих аккаунтов 📝'),
            KeyboardButton(text='Список наблюдаемых аккаунтов 👁'),
        ],[
            KeyboardButton(text='Информация о розыгрышах 🛍'),
        ],[
            KeyboardButton(text='Новые сообщения 📩'),
        ]])