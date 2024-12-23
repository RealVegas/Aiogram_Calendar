import asyncio

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import datetime
import calendar

# Кнопка старт
start_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/start')]], resize_keyboard=True)

# Формирование клавиатуры для выбора года и месяца
# async def combo_keyboard(some_dict: dict[str, str]) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
#     keyboard = InlineKeyboardBuilder()
#     for key, value in some_dict.items():
#         keyboard.add(InlineKeyboardButton(text=value, callback_data=key))
#     return keyboard.adjust(3).as_markup()

today = datetime.today()

now_year = today.year
now_month = today.month

# Кнопки для выбора года
year_section = [InlineKeyboardButton(text='<', callback_data='prev_year'),
                InlineKeyboardButton(text=f'{now_year}', callback_data='Y_none'),
                InlineKeyboardButton(text='>', callback_data='next_year')]

# Кнопки для выбора месяца
month_section = [InlineKeyboardButton(text='<', callback_data='prev_month'),
                 InlineKeyboardButton(text=f'{now_month}', callback_data='M_none'),
                 InlineKeyboardButton(text='>', callback_data='prev_month')]

# Дни недели
weekday_section = [InlineKeyboardButton(text='пн', callback_data='none'),
                   InlineKeyboardButton(text='вт', callback_data='none'),
                   InlineKeyboardButton(text='ср', callback_data='none'),
                   InlineKeyboardButton(text='чт', callback_data='none'),
                   InlineKeyboardButton(text='пт', callback_data='none'),
                   InlineKeyboardButton(text='сб', callback_data='none'),
                   InlineKeyboardButton(text='вс', callback_data='none')]

contro_keyboard = InlineKeyboardMarkup(inline_keyboard=[year_section, month_section, weekday_section], row_width=3, resize_keyboard=True)

async def new_keyboard() -> InlineKeyboardMarkup | ReplyKeyboardMarkup:

    month_cal = calendar.monthcalendar(now_year, now_month)
    one_week_section = InlineKeyboardBuilder()

    for curr_week in month_cal:

        for day_number in curr_week:
            if day_number == 0:
                one_week_section.add(InlineKeyboardButton(text=' ', callback_data='none'))

            else:
                one_week_section.add(InlineKeyboardButton(text=f'{day_number} ', callback_data=f'day_{day_number}'))

    return one_week_section.adjust(7).as_markup()

days_keyboard = asyncio.run(new_keyboard())

combo_keyboard = contro_keyboard.inline_keyboard + days_keyboard.inline_keyboard

rows = int(len(combo_keyboard))

combo_keyboard = InlineKeyboardMarkup(inline_keyboard=combo_keyboard, row_width=rows, resize_keyboard=True)