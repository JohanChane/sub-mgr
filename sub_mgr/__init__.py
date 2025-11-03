"""SubMgr - Subscription Manager"""

__version__ = "0.1.0"
__author__ = "SubMgr Developer"

from .sub_mgr import list_subscriptions, convert_subscriptions, quick_convert
from .core.sub_mgr import SubscriptionConverter, load_config_from_toml, save_config_to_toml

__all__ = [
    'list_subscriptions',
    'convert_subscriptions',
    'quick_convert',
    'SubscriptionConverter',
    'load_config_from_toml',
    'save_config_to_toml',
    '__version__',
    '__author__',
]
