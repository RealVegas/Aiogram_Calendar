import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from picker_config import *


class AioBaseCalendar:
    """
    Base class for calendar builders

    """
    def __init__(self, now_date: datetime = datetime.now()) -> None:
        init_config()

        self.builder = InlineKeyboardBuilder()

        self.now_day: int = now_date.day
        self.now_month: int = now_date.month
        self.now_year: int = now_date.year

        self.ext_mode: str = EXT_MODE
        self.confirm_button: bool = CONFIRM_BUTTON
        self.start_date: datetime = START_DATE
        self.end_date: datetime = END_DATE
        self.date_format: str = DATE_FORMAT
        self.day_set: list[str] = DAY_SET
        self.month_set: list[str] = MONTH_SET

        self.current_year: int = self.start_date.year
        self.current_month: int = self.start_date.month
        self.selected_date: datetime | None = None

        self.callback_prefix: str


class AioFullPicker(AioBaseCalendar):
    pass


class AioMiniPicker(AioBaseCalendar):
    pass