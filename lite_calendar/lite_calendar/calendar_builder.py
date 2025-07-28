import calendar
from datetime import datetime
from typing import Any

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from picker_config import *


class AioBaseCalendar:
    """
    Base class for calendar builders

    """
    def __init__(self, current: datetime = datetime.now()) -> None:
        init_config()

        self.builder = InlineKeyboardBuilder()

        self.active_day: int = current.day
        self.active_month: int = current.month
        self.active_year: int = current.year

        self.current_year: int
        self.current_month: int

        self.ext_mode: str = EXT_MODE
        self.confirm_button: bool = CONFIRM_BUTTON.lower() == 'true'
        self.start_date: str = START_DATE
        self.end_date: str = END_DATE
        self.date_format: str = DATE_FORMAT
        self.day_set: list[str] = DAY_SET
        self.month_set: list[str] = MONTH_SET

        self.callback_prefix: str


class AioFullPicker(AioBaseCalendar):
    pass


class AioMiniPicker(AioBaseCalendar):
    pass