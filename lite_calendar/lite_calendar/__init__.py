__author__ = 'Vadim Golov'
__title__ = 'Lite Calendar'
__version__ = '1.0.0'

import picker_config

from .factory import create_calendar
from .base_calendar import AioBaseCalendar

__all__ = ['create_calendar', 'AioBaseCalendar']
__all__.extend(getattr(picker_config, '__all__', []))