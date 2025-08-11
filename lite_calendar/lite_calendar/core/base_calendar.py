import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..config import *


class AioBaseCalendar:
    """
    Base class for calendar builders

    """
    def __init__(self) -> None:
        # Инициализация
        init_config()
        now_date: datetime = datetime.now()

        # Параметры конфига
        self.ext_mode: str = EXT_MODE
        self.confirm_button: bool = CONFIRM_BUTTON
        self.start_date: datetime = START_DATE
        self.end_date: datetime = END_DATE
        self.date_format: str = DATE_FORMAT
        self.day_set: list[str] = DAY_SET
        self.month_set: list[str] = MONTH_SET

        # Параметры календаря
        self.key_builder = InlineKeyboardBuilder()

        # Параметры текущей даты
        self.now_day: int = now_date.day
        self.now_month: int = now_date.month
        self.now_year: int = now_date.year

        # Параметры выбранной даты
        self.current_day: int = self.start_date.day
        self.current_year: int = self.start_date.year
        self.current_month: int = self.start_date.month

        self.selected_date: datetime | None = None

        self.rebuild_grid: bool = True
        self.close_picker: bool = False

    def _nav_bounds(self, period: str, direction: str) -> datetime | bool:
        """
        Проверяет, можно ли сдвинуть календарь в заданном направлении и периоде.

        :param period: 'day', 'month' или 'year'
        :param direction: 'next' или 'prev'
        :return: новая дата, если сдвиг возможен, иначе False

        """
        date_offset = 1 if direction == 'next' else -1

        period_map: dict[str, dict[str, int]] = {
            'day': {'days': date_offset},
            'month': {'months': date_offset},
            'year': {'years': date_offset}
        }

        shift = period_map.get(period)

        if shift is None:
            return False

        new_date: datetime = datetime(self.current_year, self.current_month, self.current_day) + relativedelta(**shift)

        if self.start_date <= new_date <= self.end_date:
            return new_date

        return False

    def navigate(self, period: str, direction: str) -> bool:
        """
        Публичный метод: сдвигает отображаемый период календаря на 1 шаг.

        :param period: 'day','month' или 'year'
        :param direction: 'next' или 'prev'
        :return: True, если навигация выполнена (self.rebuild_grid установлен в True),
                 False, если движение запрещено (nav_bounds вернул False).
        """
        # Проверяем что новая дата получена
        nav_date = self._nav_bounds(period, direction)

        if not nav_date:
            return False

        # Обновляем данные календаря
        self.current_year = nav_date.year
        self.current_month = nav_date.month
        self.current_day = nav_date.day

        # Параметр, перестроения сетки
        self.rebuild_grid = True

        return True

    def confirm_selection(self) -> None:
        """
        Подтверждает выбор даты, фиксируя selected_date.
        """
        self.selected_date = datetime(self.current_year, self.current_month, self.current_day)
        self.close_picker = True

    def formatted_selection(self) -> str:
        """
        Возвращает выбранную дату в виде отформатированной строки.

        """
        return self.selected_date.strftime(self.date_format)