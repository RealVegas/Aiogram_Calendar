import re
import sys

from loguru import logger
from pathlib import Path

from datetime import datetime
from dateutil.relativedelta import relativedelta

# Инициализация логирования
logger.add('debug.log', format='{time} {level} {message}', level='DEBUG', rotation='100 MB', compression='zip')


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
        temp: list[str] = item.split('=')

        try:
            config_key: str = temp[0].strip()
            config_value: str = temp[1].strip()

            config_data[config_key] = config_value

        except IndexError:
            continue

    if config_data:
        return config_data

    logger.error('Error: Config file (lite_config.ini) is empty')
    sys.exit(1)


class CheckExterior:
    """
    Get values of parameters from exterior section
    Returns True if all values are correct or exit otherwise

    """

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


class CheckBounds:

    def __init__(self, start_date: str, end_date: str, date_format: str) -> None:
        self.__start_date = start_date
        self.__end_date = end_date
        self.__date_format = date_format

        self.__temp_start: datetime | None = None
        self.__temp_end: datetime | None = None
        self.__today: datetime = datetime.now()

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

    @property
    def __check_start(self) -> dict[str, datetime | bool] | None:
        """
        Checks the start date is correct and a conform check necessity.

        """
        if self.__start_date == 'now':
            return {'check_start': self.__today, 'check_conform': False}

        try:
            self.__temp_start = datetime.strptime(self.__start_date, '%d-%m-%Y')
            return {'check_start': self.__temp_start, 'check_conform': True}

        except ValueError:
            logger.error('Error: The start date is not specified, or specified incorrectly.')
            sys.exit(1)

    @property
    def __check_end(self) -> dict[str, datetime | bool] | None:
        """
        Checks the end date is correct and a conform check necessity.

        """
        if re.fullmatch(r'now\+(\d+[YMD])', self.__end_date):
            return {'check_end': True, 'check_conform': False}

        try:
            self.__temp_end = datetime.strptime(self.__end_date, '%d-%m-%Y')
            return {'check_end': self.__temp_end, 'check_conform': True}

        except ValueError:
            logger.error('Error: The end date is not specified, or specified incorrectly.')
            sys.exit(1)

    def check_conform(self) -> bool | None:
        """
        Checks the start and end date are conform.

        """
        start_conform = self.__check_start['check_conform']
        end_conform = self.__check_end['check_conform']

        if not start_conform and not end_conform:
            return True

        if 'now+' in self.__end_date:
            check_result = self.check_now()

            if not check_result:
                logger.error('Error: The start date is greater than or equal the end date.')
                sys.exit(1)

            return True

        else:
            if self.__temp_end >= self.__temp_start:
                return True

            logger.error('Error: The start date is greater than or equal the end date.')
            sys.exit(1)

    def check_now(self) -> bool:
        """
        Checks for conformity if self.__end_date = 'now+...'

        """
        try:
            time_shift: int = int(self.__end_date[4:-1])

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

        finish_date: datetime = self.__today + relativedelta(**span)

        if finish_date >= self.__temp_start:
            return True

        return False


# Основное
if find_config():
    con_data: list[str] = read_config()
    config: dict[str, str] = load_config(con_data)

else:
    sys.exit('Параметры календаря не загружены: файл lite_config.ini отсутствует')

# Exterior
EXT_MODE: str = config.get('ext_mode')
DAY_FORMAT: str = config.get('day_format')
MONTH_FORMAT: str = config.get('month_format')
CONFIRM_BUTTON: str = config.get('confirm_button')

# Date Bounds
START_DATE: str = config.get('start_date')
END_DATE: str = config.get('end_date')
DATE_FORMAT: str = config.get('date_format')

exterior = CheckExterior(EXT_MODE, DAY_FORMAT, MONTH_FORMAT, CONFIRM_BUTTON)
bounds = CheckBounds(START_DATE, END_DATE, DATE_FORMAT)

print(exterior.check)
print(bounds.convert_format())