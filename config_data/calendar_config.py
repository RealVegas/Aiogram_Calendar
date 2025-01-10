import os

from typing import Optional, Iterator, IO
import sys

from dotenv.main import StrPath, DotEnv

import threading




# from dotenv import load_dotenv, find_dotenv

# if find_dotenv():
#     load_dotenv(find_dotenv())
# else:
#     exit('Переменные окружения не загружены: файл .env отсутствует')
#
# BOT_TOKEN: str = os.getenv('BOT_TOKEN')
# API_KEY: str = os.getenv('API_KEY')


def _walk_to_root(path: str) -> Iterator[str]:
    """
    Yield directories starting from the given directory up to the root
    """
    if not os.path.exists(path):
        raise IOError('Starting path not found')

    if os.path.isfile(path):
        path = os.path.dirname(path)

    last_dir = None
    current_dir = os.path.abspath(path)
    while last_dir != current_dir:
        yield current_dir
        parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
        last_dir, current_dir = current_dir, parent_dir


def find_config(
        filename: str = 'liteconfig.ini',
        raise_error_if_not_found: bool = False,
        usecwd: bool = False,
) -> str:
    """
    Search in increasingly higher folders for the given file

    Returns path to the file if found, or an empty string otherwise
    """

    def _is_interactive():
        """ Decide whether this is running in a REPL or IPython notebook """
        try:
            main = __import__('__main__', None, None, fromlist=['__file__'])
        except ModuleNotFoundError:
            return False
        return not hasattr(main, '__file__')

    if usecwd or _is_interactive() or getattr(sys, 'frozen', False):
        # Should work without __file__, e.g. in REPL or IPython notebook.
        path = os.getcwd()
    else:
        # will work for .py files
        frame = sys._getframe()
        current_file = __file__

        while frame.f_code.co_filename == current_file or not os.path.exists(
                frame.f_code.co_filename
        ):
            assert frame.f_back is not None
            frame = frame.f_back
        frame_filename = frame.f_code.co_filename
        path = os.path.dirname(os.path.abspath(frame_filename))

    for dirname in _walk_to_root(path):
        check_path = os.path.join(dirname, filename)
        if os.path.isfile(check_path):
            return check_path

    if raise_error_if_not_found:
        raise IOError('File not found')

    return ''


def load_config(
        dotenv_path: Optional[StrPath] = None,
        stream: Optional[IO[str]] = None,
        encoding: Optional[str] = "utf-8",
) -> bool:
    """Parse a .env file and then load all the variables found as environment variables.

    Parameters:
        dotenv_path: Absolute or relative path to .env file.
        stream: Text stream (such as `io.StringIO`) with .env content, used if
            `dotenv_path` is `None`.
        encoding: Encoding to be used to read the file.
    Returns:
        Bool: True if at least one environment variable is set else False

    If both `dotenv_path` and `stream` are `None`, `find_dotenv()` is used to find the
    .env file.
    """
    if dotenv_path is None and stream is None:
        dotenv_path = find_config()

    dotenv = DotEnv(
            dotenv_path=dotenv_path,
            stream=stream,
            encoding=encoding,
    )
    return dotenv.set_as_environment_variables()


def dotenv_values(
        dotenv_path: Optional[StrPath] = None,
        stream: Optional[IO[str]] = None,
        encoding: Optional[str] = "utf-8",
) -> dict[str, Optional[str]]:
    """
    Parse a .env file and return its content as a dict.

    The returned dict will have `None` values for keys without values in the .env file.
    For example, `foo=bar` results in `{"foo": "bar"}` whereas `foo` alone results in
    `{"foo": None}`

    Parameters:
        dotenv_path: Absolute or relative path to the .env file.
        stream: `StringIO` object with .env content, used if `dotenv_path` is `None`.
        encoding: Encoding to be used to read the file.

    If both `dotenv_path` and `stream` are `None`, `find_dotenv()` is used to find the
    .env file.
    """
    if dotenv_path is None and stream is None:
        dotenv_path = find_config()

    return DotEnv(
            dotenv_path=dotenv_path,
            stream=stream,
            encoding=encoding,
    ).dict()