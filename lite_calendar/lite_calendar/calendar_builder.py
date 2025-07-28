import calendar
from typing import Any
from datetime import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from picker_config import *

# 'EXT_MODE': EXT_MODE,
# 'CONFIRM_BUTTON': CONFIRM_BUTTON,
# 'START_DATE': START_DATE,
# 'END_DATE': END_DATE,
# 'DATE_FORMAT': DATE_FORMAT,
# 'DAY_SET': DAY_SET,
# 'MONTH_SET': MONTH_SET


class AioBaseСalendar:
    """
    Base class for calendar builders

    """
    def __init__(self, current: datetime | None = None) -> None:
        init_config()

        self.builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        self.active_day: int
        self.active_month: int
        self.active_year: int

        self.current_year: int
        self.current_month: int

        self.start_date: date
        self.end_date: date
        self.date_format: str
        self.day_set: list[str]
        self.month_set: list[str]
        self.ext_mode: bool
        self.confirm_button: bool

        self.callback_prefix: str














        self.today: datetime = datetime.today()
        self.current: datetime = current or self.today


        # Подтягиваем конфиг (можно сделать через init_config() -> CalendarConfig)
        self.ext_mode: str = EXT_MODE
        self.confirm_button: bool = True if CONFIRM_BUTTON == 'True' else False
        self.start_date: datetime = START_DATE
        self.end_date: datetime = END_DATE
        self.date_format: str = DATE_FORMAT
        self.day_set: list[str | int] = DAY_SET
        self.month_set: list[str | int] = MONTH_SET


class AioFullPicker(AioBaseСalendar):
    pass

class AioMiniPicker(AioBaseСalendar):
    pass