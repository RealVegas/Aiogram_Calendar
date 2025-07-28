import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class AioBaseDate:

    def __init__(self, year: int, month: int, day: int) -> None:
        self.current_year = year
        self.currenr_month = year
        self.current_day = day

        self.