__author__ = 'Vadim Golov'
__title__ = 'Lite Calendar'
__version__ = '1.0.0'

from . import picker_config

__all__ = []
__all__.extend(getattr(picker_config, '__all__', []))