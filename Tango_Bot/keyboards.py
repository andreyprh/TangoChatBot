from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_service_keyboard():
    keyboard = [
        [KeyboardButton(text="Групповые занятия"), KeyboardButton(text="Индивидуальные занятия")],
        [KeyboardButton(text="Постановочный танец"), KeyboardButton(text="Подарочный сертификат")],
        [KeyboardButton(text="Случайное танго-фото")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_level_keyboard():
    keyboard = [
        [KeyboardButton(text="Начинающий"), KeyboardButton(text="Продвинутый")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_confirmation_keyboard():
    keyboard = [
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)