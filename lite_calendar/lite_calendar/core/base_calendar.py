import calendar
from datetime import datetime

from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..config import *


class AioBaseCalendar:
    """
    Base class for calendar builders

    """
    def __init__(self) -> None:
        init_config()
        now_date: datetime = datetime.now()

        self.ext_mode: str = EXT_MODE
        self.confirm_button: bool = CONFIRM_BUTTON
        self.start_date: datetime = START_DATE
        self.end_date: datetime = END_DATE
        self.date_format: str = DATE_FORMAT
        self.day_set: list[str] = DAY_SET
        self.month_set: list[str] = MONTH_SET

        self.key_builder = InlineKeyboardBuilder()

        self.now_day: int = now_date.day
        self.now_month: int = now_date.month
        self.now_year: int = now_date.year

        self.current_day: int = self.start_date.day
        self.current_year: int = self.start_date.year
        self.current_month: int = self.start_date.month

        self.selected_date: datetime | None = None

        self.rebuild_grid: bool = True
        self.callback_prefix: str = 'litepick'