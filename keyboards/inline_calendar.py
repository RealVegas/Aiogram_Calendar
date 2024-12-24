import calendar
from datetime import datetime

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import lang

import unittest

# Кнопка старт
start_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/start')]], resize_keyboard=True)

# Формирование календаря

# Текущий шод и месяц
today = datetime.now()

now_year = today.year
now_month = today.month


def month_keyboard(get_year: int, get_month: int) -> list[list[InlineKeyboardButton]]:

    month_calendar = calendar.monthcalendar(get_year, get_month)
    weeks_section = InlineKeyboardBuilder()

    for one_week in month_calendar:

        for one_day in one_week:
            if one_day == 0:
                weeks_section.add(InlineKeyboardButton(text=' ', callback_data='ignore'))
            else:
                weeks_section.add(InlineKeyboardButton(text=f'{one_day} ', callback_data=f'day_{one_day}'))

    weeks_section = weeks_section.adjust(7).as_markup().inline_keyboard

    return weeks_section











# async def generate_calendar(year, month, option=None):
#     match option:
#         case 'rus_full':
#             day_set = lang.ru_day_name
#             month_set = lang.ru_month_name
#         case 'rus_short':
#             day_set = lang.ru_day_abbr
#             month_set = lang.ru_month_abbr
#         case 'eng_full':
#             day_set = lang.eng_day_name
#             month_set = lang.eng_month_name
#         case 'eng_short':
#             day_set = lang.eng_day_abbr
#             month_set = lang.eng_month_abbr
#
#
# # Кнопки для выбора года
# year_section = [InlineKeyboardButton(text='<', callback_data='prev_year'),
#                 InlineKeyboardButton(text=f'{now_year}', callback_data='ignore'),
#                 InlineKeyboardButton(text='>', callback_data='next_year')]
#
# # Кнопки для выбора месяца
# month_section = [InlineKeyboardButton(text='<', callback_data='prev_month'),
#                  InlineKeyboardButton(text=f'{now_month}', callback_data='ignore'),
#                  InlineKeyboardButton(text='>', callback_data='prev_month')]
#
# # Дни недели
# weekday_section = [InlineKeyboardButton(text='пн', callback_data='ignore'),
#                    InlineKeyboardButton(text='вт', callback_data='ignore'),
#                    InlineKeyboardButton(text='ср', callback_data='ignore'),
#                    InlineKeyboardButton(text='чт', callback_data='ignore'),
#                    InlineKeyboardButton(text='пт', callback_data='ignore'),
#                    InlineKeyboardButton(text='сб', callback_data='ignore'),
#                    InlineKeyboardButton(text='вс', callback_data='ignore')]
#
# contro_keyboard = InlineKeyboardMarkup(inline_keyboard=[year_section, month_section, weekday_section], row_width=3,
#                                        resize_keyboard=True)
#
#
# def new_keyboard() -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
#     month_cal = calendar.monthcalendar(now_year, now_month)
#     one_week_section = InlineKeyboardBuilder()
#
#     for curr_week in month_cal:
#
#         for day_number in curr_week:
#             if day_number == 0:
#                 one_week_section.add(InlineKeyboardButton(text=' ', callback_data='none'))
#
#             else:
#                 one_week_section.add(InlineKeyboardButton(text=f'{day_number} ', callback_data=f'day_{day_number}'))
#
#     return one_week_section.adjust(7).as_markup()
#
#
# days_keyboard = new_keyboard()
#
# combo_keyboard = contro_keyboard.inline_keyboard + days_keyboard.inline_keyboard
#
# rows = int(len(combo_keyboard))
#
# combo_keyboard = InlineKeyboardMarkup(inline_keyboard=combo_keyboard, row_width=rows, resize_keyboard=True)

# Формирование клавиатуры для выбора года и месяца
# async def combo_keyboard(some_dict: dict[str, str]) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
#     keyboard = InlineKeyboardBuilder()
#     for key, value in some_dict.items():
#         keyboard.add(InlineKeyboardButton(text=value, callback_data=key))
#     return keyboard.adjust(3).as_markup()


class TestCalendar(unittest.TestCase):
    def test_month_keyboard(self):
        month_keyboard(2023, 4)

        # month_keyboard(2023, 2)
        # month_keyboard(2023, 3)

if __name__ == '__main__':
    unittest.main()