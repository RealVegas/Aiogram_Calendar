from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Кнопка старт
start_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/start')]], resize_keyboard=True)


# Формирование клавиатуры для выбора года и месяца
async def combo_keyboard(some_dict: dict[str, str]) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for key, value in some_dict.items():
        keyboard.add(InlineKeyboardButton(text=value, callback_data=key))
    return keyboard.adjust(3).as_markup()


#  Кнопки для выбора года
# year_keyboard = InlineKeyboardMarkup(inline_keyboard=[[
#                 InlineKeyboardButton(text='<', callback_data='prev_year'),
#                 InlineKeyboardButton(text=now_year, callback_data='None'),
#                 InlineKeyboardButton(text='>', callback_data='next_year')]],
#                 resize_keyboard=True,
#                 row_width=1)