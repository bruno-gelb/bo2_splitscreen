import logging
import os
import sys
from functools import partial

import sentry_sdk
from PySide2 import QtWidgets
from sentry_sdk.integrations.logging import LoggingIntegration

from settings import SENTRY_DSN, ENVIRONMENT, LOG_LEVEL, LOG_DIR, LOG_FILE
from src import config
from src.core import resolve_handler

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
fh = logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE))
formatter = logging.Formatter('[%(filename)s] %(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # capture info and above as breadcrumbs
    event_level=logging.WARNING  # but only send warnings and errors as events
)
sentry_sdk.init(
    dsn=SENTRY_DSN,
    environment=ENVIRONMENT,
    integrations=[sentry_logging]
)

MAIN_COLOR = '#d5d927'


class MainScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.showFullScreen()
        self.setStyleSheet(f'background-color: {MAIN_COLOR}')

        self.games_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.games_layout)
        for game_name in config.games:
            self.game = QtWidgets.QPushButton(game_name)
            self.games_layout.addWidget(self.game)
            self.game.clicked.connect(partial(self.launch, game_name))

    def launch(self, game_name):
        self.hide()
        handler = resolve_handler(game_name)
        if handler:
            handler()
        else:
            logger.error(f'No handler found for \'{game_name}\' game.', exc_info=True)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    main_screen = MainScreen()
    main_screen.show()

    sys.exit(app.exec_())
