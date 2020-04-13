import logging
import os
from typing import Union

# import sentry_sdk
# from sentry_sdk.integrations.logging import LoggingIntegration

from handlers.borderlands2 import bo2_handler
from handlers.overcooked import overcooked_handler
from handlers.overcooked2 import overcooked2_handler
from settings import LOG_LEVEL, LOG_DIR, LOG_FILE, SENTRY_DSN, ENVIRONMENT

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
fh = logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE))
formatter = logging.Formatter('[%(filename)s] %(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
# sentry_logging = LoggingIntegration(
#     level=logging.INFO,  # capture info and above as breadcrumbs
#     event_level=logging.WARNING  # but only send warnings and errors as events
# )
# sentry_sdk.init(
#     dsn=SENTRY_DSN,
#     environment=ENVIRONMENT,
#     integrations=[sentry_logging]
# )


def resolve_handler(game_name: str) -> Union[None, object]:
    handlers_mapping = {
        'borderlands2': bo2_handler,
        'overcooked': overcooked_handler,
        'overcooked2': overcooked2_handler,
    }
    handler = handlers_mapping.get(game_name, None)
    if handler:
        return handler
    else:
        logger.error(f'No handler found for \'{game_name}\' game.', exc_info=True)
