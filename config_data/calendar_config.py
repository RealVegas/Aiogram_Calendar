import os
import sys
import re

from datetime import datetime
from dateutil.relativedelta import relativedelta


def parent_dir(path: str) -> str:
    """
    Return parent directory of the given directory

    """
    return os.path.abspath(os.path.join(path, os.pardir))


def find_config() -> str | None:
    """
    Look for config_name('lite_config.ini') in path tree
    Returns path with config_name if found, or None otherwise

    """
    config_name: str = 'lite_config.ini'

    curr_path: str = os.getcwd()
    curr_content: list[str] = os.listdir(curr_path)

    last_path: str = curr_path

    while config_name not in curr_content:
        curr_path: str = parent_dir(last_path)
        curr_content: list[str] = os.listdir(curr_path)

        if curr_path == last_path:
            return None
        else:
            last_path: str = curr_path

    return os.path.join(curr_path, config_name)


def read_config(config_path: str = None) -> list[str]:
    """
    Read config file('lite_config.ini')
    Returns prepared config file content

    """
    if config_path is None:
        config_path: str = find_config()

    if config_path is None:
        sys.exit('Error: Config file not found')

    else:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            file_content: list[str] = config_file.read().split('\n')
            config_content: list[str] = [one_line for one_line in file_content if '[' not in one_line]

        return config_content


def load_config(content: list[str] = None) -> dict[str, str]:
    """
    Get config file content if exist
    Returns dictionary with config items

    """
    config_data: dict[str, str] = {}

    for item in content:
        temp: list[str] = item.split('=')

        try:
            con_key: str = temp[0].strip()
            con_val: str = temp[1].strip()

            config_data[con_key] = con_val

        except IndexError:
            continue

    return config_data


class CheckExterior:
    """
    Get values of parameters from exterior section
    Returns True if all values are correct or exit otherwise

    """
    def __init__(self, day_format: str, month_format: str, confirm_button: str) -> None:
        self.__values: dict[str, str] = {'day': day_format, 'month': month_format, 'button': confirm_button}

        self.__correct: list[set[str]] = [{'number', 'ru_full', 'ru_short', 'en_full', 'en_short'},
                                          {'number', 'ru_full', 'ru_short', 'en_full', 'en_short'},
                                          {'True', 'False'}]

    @property
    def check(self) -> bool | None:
        num: int = 0

        for name, value in self.__values.items():
            if value not in self.__correct[num]:
                if value == '':
                    value: str = '?'
                sys.exit(f' {name} - Ошибка! Значение: {value} не является допустимым')
            else:
                num += 1

        return True


class CheckBounds:

    def __init__(self, start_date: str, end_date: str, date_format: str) -> None:
        self.__start_date: str = start_date
        self.__end_date: str = end_date
        self.__date_format: str = date_format

        self.__today: str = datetime.now().strftime('%d-%m-%Y')

    @property
    def check_format(self) -> bool | None:
        format_decision: bool = False

        if 'DD' in self.__date_format:
            format_decision: bool = True
        if 'MM' in self.__date_format:
            format_decision: bool = True
        if 'YYYY' in self.__date_format:
            format_decision: bool = True

        if not format_decision:
            sys.exit('Формат вывода даты не указан, либо указан неверно')

        return True

    @property
    def check_start(self) -> tuple[bool, bool] | None:

        start_decision: bool = False
        conform_check: bool = False

        if 'now' in self.__start_date:
            start_decision: bool = True

        else:
            try:
                datetime.strptime(self.__start_date, '%d-%m-%Y')
                conform_check: bool = True
                start_decision: bool = True

            except ValueError:
                start_decision: bool = False

        if not start_decision:
            sys.exit('Начальная дата не указана, либо указана неверно')

        return conform_check, True

    @property
    def check_end(self) -> tuple[bool, bool] | None:

        end_decision: bool = False
        conform_check: bool = False

        if 'now+' in self.__end_date:
            match: Match = re.match(r'^now\+(\d+[YMD])$', self.__end_date)
            if not match:
                end_decision: bool = False

        else:
            try:
                datetime.strptime(self.__end_date, '%d-%m-%Y')
                conform_check: bool = True
                end_decision: bool = True

            except ValueError:
                end_decision: bool = False

        if not end_decision:
            sys.exit('Конечная дата не указана, либо указана неверно')

        return conform_check, True

    def check_conform(self):

        start_conform = self.check_start[0]
        end_conform = self.check_end[0]

        if not start_conform and not end_conform:
            return True

        conform_decision = False

        delta = None
        start_span = None
        end_span = None

        if 'now+' in self.__end_date:
            match: Match = re.match(r'^now\+(\d+[YMD])$', self.__end_date)

            if match[-1::] == 'Y':
                span = {'years': int(match[:-1])}
                delta = relativedelta(**span)
            elif match[-1::] == 'M':
                span = {'months': int(match[:-1])}
                delta = relativedelta(**span)
            elif match [-1::] == 'D':
                span = {'days': int(match[:-1])}
                delta = relativedelta(**span)

        if start_conform:
            if not end_conform:
                end_span = datetime.strptime(self.__today, 'd%-m%-%Y') + delta
            start_span = datetime.strptime(self.__start_date, 'd%-m%-%Y')

        if end_conform:
            if not start_conform:
                start_span = datetime.strptime(self.__today, 'd%-m%-%Y')
            end_span = datetime.strptime(self.__end_date, 'd%-m%-%Y')

        if start_span > end_span:
            sys.exit(f'Несоответствие дат: {start_span} больше {end_span}')
        elif start_span == end_span:
            sys.exit(f'Несоответствие дат: {start_span} и {end_span} одинаковые')
        else:
            return True


# Основное
if find_config():
    con_data: list[str] = read_config()
    config: dict[str, str] = load_config(con_data)

else:
    sys.exit('Параметры календаря не загружены: файл lite_config.ini отсутствует')

# Exterior
DAY_FORMAT: str = config.get('day_format')
MONTH_FORMAT: str = config.get('month_format')
CONFIRM_BUTTON: str = config.get('confirm_button')

# Date Bounds
START_DATE: str = config.get('start_date')
END_DATE: str = config.get('end_date')
DATE_FORMAT: str = config.get('date_format')

exterior = CheckExterior(DAY_FORMAT, MONTH_FORMAT, CONFIRM_BUTTON)
bounds = CheckBounds(START_DATE, END_DATE, DATE_FORMAT)

print(exterior.check)
print(bounds.check_format)