import re
import sys
import json

from typing import cast

from loguru import logger
from pathlib import Path

from datetime import datetime
from dateutil.relativedelta import relativedelta

# Инициализация логирования
logger.add('debug.log', format='{time} {level} {message}', level='DEBUG', rotation='100 MB', compression='zip')

# Глобальные переменные
EXT_MODE: str = 'empty'
CONFIRM_BUTTON: bool = True

START_DATE: str | datetime = 'empty'
END_DATE: str | datetime = 'empty'
DATE_FORMAT: str = 'empty'

DAY_SET: list[int | str] = []
MONTH_SET: list[int | str] = []

__all__ = ['init_config',
           'EXT_MODE', 'CONFIRM_BUTTON',
           'START_DATE', 'END_DATE', 'DATE_FORMAT',
           'DAY_SET', 'MONTH_SET'
           ]


def init_config() -> None:
    """
    Initialize config

    """
    global EXT_MODE, CONFIRM_BUTTON
    global START_DATE, END_DATE, DATE_FORMAT
    global DAY_SET, MONTH_SET

    config_list: list[str] = read_config()
    config_dict: dict[str, str] = load_config(config_list)

    EXT_MODE = config_dict.get('ext_mode')
    day_format: str = config_dict.get('day_format')
    month_format: str = config_dict.get('month_format')
    CONFIRM_BUTTON = config_dict.get('confirm_button') == 'True'

    START_DATE = config_dict.get('start_date')
    END_DATE = config_dict.get('end_date')
    DATE_FORMAT = config_dict.get('date_format')

    exterior = CheckExterior(EXT_MODE, day_format, month_format, CONFIRM_BUTTON)
    formator = CheckFormat(DATE_FORMAT)
    bounds = CheckBounds(START_DATE, END_DATE)
    lang_sets = LangData(day_format, month_format)

    if exterior.check:
        DATE_FORMAT = formator.convert_format
        START_DATE, END_DATE = map(lambda some_date: datetime.strftime(some_date, '%d.%m.%Y'), bounds.check_conform)
        DAY_SET = lang_sets.date_set('day')
        MONTH_SET = lang_sets.date_set('month')

        logger.info(f'EXT_MODE: {EXT_MODE}')
        logger.info(f'day_format: {day_format}')
        logger.info(f'month_format: {month_format}')
        logger.info(f'CONFIRM_BUTTON: {CONFIRM_BUTTON}')

        logger.info(f'START_DATE: {START_DATE}')
        logger.info(f'END_DATE: {END_DATE}')
        logger.info(f'DATE_FORMAT: {DATE_FORMAT}')

        logger.info(f'DAY_SET: {DAY_SET}')
        logger.info(f'MONTH_SET: {MONTH_SET}')

    logger.info('Config successfully initialized')


def find_config() -> Path | None:
    """
    Look for 'lite_config.ini' in base_path
    Returns path with config file if found, or None otherwise

    """

    base_path: Path = Path(__file__).parent
    config_file: Path = base_path / 'lite_config.ini'

    if config_file.is_file():
        return config_file

    return None


def read_config() -> list[str] | None:
    """
    Read config file('lite_config.ini')
    Returns prepared config file content

    """
    config_path = find_config()

    if config_path:
        file_content: list[str] = config_path.read_text(encoding='utf-8').split('\n')
        config_content: list[str] = [one_line for one_line in file_content if '[' not in one_line]

        return config_content

    logger.error('Error: Config file (lite_config.ini) not found')
    sys.exit(1)


def load_config(content: list[str] = None) -> dict[str, str]:
    """
    Get config file content if exist
    Returns dictionary with config items

    """
    config_data: dict[str, str] = {}

    for item in content:

        try:
            config_key, config_value = map(str.strip, item.split('=', 1))
            config_data[config_key] = config_value

        except (IndexError, ValueError):
            continue

    if config_data:
        return config_data

    logger.error('Error: Config file (lite_config.ini) is empty')
    sys.exit(1)


class CheckExterior:

    def __init__(self, ext_mode: str, day_format: str, month_format: str, confirm_button: str) -> None:
        self.__values: dict[str, str] = {'mode': ext_mode, 'day': day_format, 'month': month_format,
                                         'button': confirm_button}
        self.__correct: list[set[str]] = [
            {'full', 'mini'},
            {'number', 'ru_full', 'ru_short', 'en_full', 'en_short'},
            {'number', 'ru_full', 'ru_short', 'en_full', 'en_short'},
            {'True', 'False'}
        ]

    @property
    def check(self) -> bool | None:
        """
        Get values of parameters from exterior section
        Returns True if all values are correct or exit otherwise

        """
        index: int = 0

        for name, value in self.__values.items():
            if value not in self.__correct[index]:
                if value == '':
                    value: str = '?'
                logger.error(f'Error: Value {value} for key {name} is not acceptable')
                sys.exit(1)
            else:
                index += 1

        return True


class CheckFormat:

    def __init__(self, date_format: str) -> None:
        self.__date_format = date_format

    @property
    def __check_format(self) -> bool | None:
        """
        Check pattern for output date

        """
        block: str = r'(DD|MM|YYYY)'
        separator: str = r'(?![DMY])[^\w]'

        part_one: str = f'^{block}$'
        part_two: str = f'^{block}{separator}{block}$'
        part_three: str = f'^{block}(?P<sep>{separator}){block}(?P=sep){block}$'

        pattern = re.compile(f'{part_three}|{part_two}|{part_one}')

        if re.fullmatch(pattern, self.__date_format):
            return True

        return False

    @property
    def convert_format(self) -> str | None:
        """
        Convert date output pattern for strptime

        """
        if self.__check_format:
            mapping: dict[str, str] = {'DD': '%d', 'MM': '%m', 'YYYY': '%Y'}
            pattern: re.Pattern = re.compile(r'YYYY|DD|MM')

            converted: str = pattern.sub(lambda date_pattern: mapping[date_pattern.group(0)], self.__date_format)

            return converted

        logger.error('Error: The date output pattern is not specified, or specified incorrectly.')
        sys.exit(1)


class CheckBounds:

    def __init__(self, start_date: str, end_date: str) -> None:
        self.__start_date = start_date
        self.__end_date = end_date

        self.__today: datetime = datetime.now()

    @property
    def __check_start(self) -> datetime | None:
        """
        Checks the start date is correct.

        """
        if self.__start_date == 'now':
            return self.__today

        try:
            temp_date: datetime = datetime.strptime(self.__start_date, '%d-%m-%Y')
            print(temp_date)
            return temp_date

        except ValueError:
            logger.error('Error: The start date is not specified, or specified incorrectly.')
            sys.exit(1)

    @property
    def __check_end(self) -> datetime | None:
        """
        Checks the end date is correct.

        """
        if re.fullmatch(r'now\+(\d+[YMD])', self.__end_date):
            return self.__today

        if re.fullmatch(r'start_date\+(\d+[YMD])', self.__end_date):
            return None

        try:
            temp_date = datetime.strptime(self.__end_date, '%d-%m-%Y')
            return temp_date

        except ValueError:
            logger.error('Error: The end date is not specified, or specified incorrectly.')
            sys.exit(1)

    @property
    def check_conform(self) -> tuple[datetime, datetime] | None:
        """
        Checks the start and end date are conform.

        """
        temp_start = self.__check_start
        temp_end = self.__check_end

        if self.__end_date.startswith('now'):
            return self.__convert_now(temp_start, temp_end)

        elif self.__end_date.startswith('start_date'):
            return self.__convert_now(temp_start, temp_start)

        else:
            if temp_end > temp_start:
                return temp_start, temp_end

            logger.error('Error: The start date is greater or equal the end date.')
            sys.exit(1)

    def __convert_now(self, start_dt: datetime, end_dt: datetime) -> tuple[datetime, datetime]:
        """
        Convert self.__end_date = 'now+...' to concrete date

        """
        try:
            if self.__end_date.startswith('now'):
                time_shift: int = int(self.__end_date[4:-1])
            else:
                time_shift: int = int(self.__end_date[11:-1])

        except ValueError:
            logger.error('Error: The end date is not specified, or specified incorrectly.')
            sys.exit(1)

        match self.__end_date[-1:]:
            case 'Y':
                span = {'years': time_shift}
            case 'M':
                span = {'months': time_shift}
            case 'D':
                span = {'days': time_shift}
            case _:
                logger.error('Error: The the time delta is not specified, or specified incorrectly.')
                sys.exit(1)

        end_dt = end_dt + relativedelta(**span)

        return start_dt, end_dt


class LangData:

    def __init__(self, day_str: str, month_atr: str) -> None:
        self.__day = day_str
        self.__month = month_atr

    @property
    def __read_lang(self) -> dict[str, dict[str, int | str]]:
        """
        Read language file

        """
        lang_path: Path = Path(__file__).parent / 'misc' / 'lang.json'

        with open(lang_path, 'r', encoding='utf-8') as lang_file:
            return json.load(lang_file)

    @classmethod
    def __get_lang(cls, lang_str: str) -> str:
        """
        Get language

        """
        if lang_str == 'number':
            return 'num'
        elif lang_str.startswith('ru'):
            return 'ru'
        elif lang_str.startswith('en'):
            return 'en'
        else:
            logger.error('Error: The language is not specified, or specified incorrectly.')
            sys.exit(1)

    @classmethod
    def __get_grid(cls, grid_str: str, date: str) -> str:
        """
        Get grid

        """
        if grid_str == 'number':
            return '{span}_num'
        elif grid_str.endswith('full'):
            return f'{date}_name'
        elif grid_str.endswith('short'):
            return f'{date}_abbr'
        else:
            logger.error('Error: The grid is not specified, or specified incorrectly.')
            sys.exit(1)

    def date_set(self, option: str) -> list[int | str]:
        """
        Get list of day or month in specified format

        """
        __date_param: str | None = None

        if option == 'day':
            __date_param: str = self.__day
        elif option == 'month':
            __date_param: str = self.__month

        lang_data = self.__read_lang

        lang: str = self.__get_lang(__date_param)
        grid: str = self.__get_grid(__date_param, option)

        return cast(list[int | str], lang_data[lang][grid])


if __name__ == '__main__':
    pass