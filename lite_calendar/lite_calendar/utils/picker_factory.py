import sys
from ..config.picker_config import logger

from ..core.base_calendar import AioBaseCalendar
from ..core.build_full import AioFullPicker
from ..core.build_mini import AioMiniPicker


def lite_calendar() -> AioBaseCalendar:
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