import os
import sys
from typing import Optional


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
    config_name = 'lite_config.ini'

    curr_path = os.getcwd()
    curr_content = os.listdir(curr_path)

    last_path = curr_path

    while config_name not in curr_content:
        curr_path = parent_dir(last_path)
        curr_content = os.listdir(curr_path)

        if curr_path == last_path:
            return None
        else:
            last_path = curr_path

    return os.path.join(curr_path, config_name)


def load_config(config_path: Optional[str] = None) -> list[str]:
    """
    Load config file('lite_config.ini')
    Returns prepared config file content

    """
    if config_path is None:
        config_path = find_config()

    if config_path is None:
        sys.exit('Error: Config file not found')

    else:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            file_content = config_file.read().split('\n')
            config_content = [one_line for one_line in file_content if '[' not in one_line]

        return config_content


cs = load_config()
print(cs)

















        # for line in
        # config_file:
        #     config = line.strip().split('=')
        #     try:
        #         new_dict[config[0].strip()] = config[1].strip()
        #     except IndexError:
        #         pass







# def load_config(
#         dotenv_path: Optional[StrPath] = None,
#         stream: Optional[IO[str]] = None,
#         encoding: Optional[str] = "utf-8",
# ) -> bool:
#     """Parse a .env file and then load all the variables found as environment variables.
#
#     Parameters:
#         dotenv_path: Absolute or relative path to .env file.
#         stream: Text stream (such as `io.StringIO`) with .env content, used if
#             `dotenv_path` is `None`.
#         encoding: Encoding to be used to read the file.
#     Returns:
#         Bool: True if at least one environment variable is set else False
#
#     If both `dotenv_path` and `stream` are `None`, `find_dotenv()` is used to find the
#     .env file.
#     """
#     if dotenv_path is None and stream is None:
#         dotenv_path = find_config()
#
#     dotenv = DotEnv(
#             dotenv_path=dotenv_path,
#             stream=stream,
#             encoding=encoding,
#     )
#     return dotenv.set_as_environment_variables()
#
#
# def dotenv_values(
#         dotenv_path: Optional[StrPath] = None,
#         stream: Optional[IO[str]] = None,
#         encoding: Optional[str] = "utf-8",
# ) -> dict[str, Optional[str]]:
#     """
#     Parse a .env file and return its content as a dict.
#
#     The returned dict will have `None` values for keys without values in the .env file.
#     For example, `foo=bar` results in `{"foo": "bar"}` whereas `foo` alone results in
#     `{"foo": None}`
#
#     Parameters:
#         dotenv_path: Absolute or relative path to the .env file.
#         stream: `StringIO` object with .env content, used if `dotenv_path` is `None`.
#         encoding: Encoding to be used to read the file.
#
#     If both `dotenv_path` and `stream` are `None`, `find_dotenv()` is used to find the
#     .env file.
#     """
#     if dotenv_path is None and stream is None:
#         dotenv_path = find_config()
#
#     return DotEnv(
#             dotenv_path=dotenv_path,
#             stream=stream,
#             encoding=encoding,
#     ).dict()




# if find_config():
#     load_config()
# else:
#      sys.exit('Настройки не загружены: файл lite_config.ini отсутствует')

# BOT_TOKEN: str = os.getenv('BOT_TOKEN')
# API_KEY: str = os.getenv('API_KEY')












# from dotenv import load_dotenv, find_dotenv

# if find_dotenv():
#     load_dotenv(find_dotenv())
# else:
#     exit('Переменные окружения не загружены: файл .env отсутствует')
#
# BOT_TOKEN: str = os.getenv('BOT_TOKEN')
# API_KEY: str = os.getenv('API_KEY')