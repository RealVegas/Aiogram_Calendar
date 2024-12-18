from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import datetime

# Кнопка старт
start_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/start')]], resize_keyboard=True)


# Формирование клавиатуры для выбора года и месяца
# async def combo_keyboard(some_dict: dict[str, str]) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
#     keyboard = InlineKeyboardBuilder()
#     for key, value in some_dict.items():
#         keyboard.add(InlineKeyboardButton(text=value, callback_data=key))
#     return keyboard.adjust(3).as_markup()

now_year = str(datetime.now().year)
now_month = str(datetime.now().month)

#  Кнопки для выбора года
combo_keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text='<', callback_data='prev_year'),
                InlineKeyboardButton(text=now_year, callback_data='Y_none'),
                InlineKeyboardButton(text='>', callback_data='next_year')
                ], [
                InlineKeyboardButton(text='<', callback_data='prev_month'),
                InlineKeyboardButton(text=now_month, callback_data='M_none'),
                InlineKeyboardButton(text='>', callback_data='prev_month')
                ], [
                InlineKeyboardButton(text='пн', callback_data='none'),
                InlineKeyboardButton(text='вт', callback_data='none'),
                InlineKeyboardButton(text='ср', callback_data='none'),
                InlineKeyboardButton(text='чт', callback_data='none'),
                InlineKeyboardButton(text='пт', callback_data='none'),
                InlineKeyboardButton(text='сб', callback_data='none'),
                InlineKeyboardButton(text='вс', callback_data='none')
                ]],
                row_width=3,
                resize_keyboard=True)