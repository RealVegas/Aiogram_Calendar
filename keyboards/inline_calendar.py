import calendar
from datetime import datetime

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from . import lang
import unittest

# Кнопка старт
start_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/start')]], resize_keyboard=True)


# Формирование календаря

# Кнопки для выбора года и месяца
def header_keyboard(h_year: int, h_month: int, month_list: list[str]) -> list[list[InlineKeyboardButton]]:

    month_desc: str = month_list[h_month - 1]
    header_section: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Кнопки для лет
    header_section.add(InlineKeyboardButton(text='<', callback_data=f'year-prev_{h_year}_{h_month}'),
                       InlineKeyboardButton(text=f'{h_year}', callback_data='ignore'),
                       InlineKeyboardButton(text='>', callback_data=f'year-next_{h_year}_{h_month}'))
    # Кнопки для месяцев
    header_section.add(InlineKeyboardButton(text='<', callback_data=f'month-prev_{h_month}_{h_year}'),
                       InlineKeyboardButton(text=f'{month_desc}', callback_data='ignore'),
                       InlineKeyboardButton(text='>', callback_data=f'month-next_{h_month}_{h_year}'))

    header_section: list[list[InlineKeyboardButton]] = header_section.adjust(3).as_markup().inline_keyboard

    return header_section


# Cетка для чисел месяца c названием дней
def month_keyboard(m_year: int, m_month: int, day_list: list[str]) -> list[list[InlineKeyboardButton]]:

    today = datetime.now()
    now_year = today.year
    now_month = today.month
    now_day = today.day

    month_calendar: list[list[str | int]] = [day_list] + calendar.monthcalendar(m_year, m_month)
    weeks_section: InlineKeyboardBuilder = InlineKeyboardBuilder()

    this_day = now_day if now_year == m_year and now_month == m_month else -1

    for one_week in month_calendar:

        for one_day in one_week:

            if isinstance(one_day, str):
                attr: dict[str, str] = {'text': f'{one_day}', 'data': 'ignore'}
            elif one_day == 0:
                attr: dict[str, str] = {'text': ' ', 'data': 'ignore'}
            elif one_day == this_day:
                attr: dict[str, str] = {'text': f'[ {one_day} ]', 'data': f'day_{one_day}'}
            else:
                attr: dict[str, str] = {'text': f'{one_day}', 'data': f'day_{one_day}'}

            weeks_section.add(InlineKeyboardButton(text=attr['text'], callback_data=attr['data']))

    weeks_section: list[list[InlineKeyboardButton]] = weeks_section.adjust(7).as_markup().inline_keyboard

    return weeks_section


# Формирование клавиатуры по параметрам
async def generate_calendar(get_year: int, get_month: int, option=None) -> InlineKeyboardMarkup:

    # Настройки нотации и языка (если что-то пойдёт не так)
    day_set: list[str] = lang.ru_day_abbr
    month_set: list[str] = lang.ru_month_name

    # Настройки нотации и языка для формирования клавиатур
    match option:
        case 'rus_full':
            day_set: list[str] = lang.ru_day_name
            month_set: list[str] = lang.ru_month_name
        case 'rus_short':
            day_set: list[str] = lang.ru_day_abbr
            month_set: list[str] = lang.ru_month_name
        case 'eng_full':
            day_set: list[str] = lang.eng_day_name
            month_set: list[str] = lang.eng_month_name
        case 'eng_short':
            day_set: list[str] = lang.eng_day_abbr
            month_set: list[str] = lang.eng_month_name

    # Формирование клавиатур
    header: list[list[InlineKeyboardButton]] = header_keyboard(get_year, get_month, month_list=month_set)
    month: list[list[InlineKeyboardButton]] = month_keyboard(get_year, get_month, day_list=day_set)

    # Сборка клавиатуры
    rows: int = int(len(month)) + 2
    assembled_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=header + month, row_width=rows, resize_keyboard=True)

    return assembled_keyboard


# Тесты функций
class TestCalendar(unittest.TestCase):
    def test_month_keyboard(self):
        month_keyboard(2023, 4, lang.ru_day_abbr)

    def test_header_keyboard(self):
        header_keyboard(2023, 4, lang.ru_month_name)

    def test_generate_calendar(self):  # когда функция была синхронной
        generate_calendar(2023, 4, 'rus_short')
        generate_calendar(2024, 10, 'rus_full')
        generate_calendar(2024, 12, 'eng_short')
        generate_calendar(2023, 8, 'eng_full')


if __name__ == '__main__':
    unittest.main()