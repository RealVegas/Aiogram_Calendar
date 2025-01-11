import os
import sys


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