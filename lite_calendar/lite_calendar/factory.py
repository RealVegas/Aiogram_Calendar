import sys
from .picker_config import logger

from .base_calendar import AioBaseCalendar
from .full_picker import AioFullPicker
from .mini_picker import AioMiniPicker


def create_calendar() -> AioBaseCalendar:
    """
    Создаёт календарь в зависимости от режима.

    :return: экземпляр календаря
    """
    mode = AioBaseCalendar().ext_mode

    if mode == 'full':
        return AioFullPicker()
    elif mode == 'mini':
        return AioMiniPicker()
    else:
        logger.error(f'Error: Unknown ext_mode: {ext_mode}')
        sys.exit(1)