import logging
import os
import sys
from functools import partial

# import sentry_sdk
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QSizePolicy, QLabel
# from sentry_sdk.integrations.logging import LoggingIntegration

from settings import SENTRY_DSN, ENVIRONMENT, LOG_LEVEL, LOG_DIR, LOG_FILE
from src import config
from src.core import resolve_handler
# from src.metadata import get_metadata

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

MAIN_COLOR = '#d5d927'
METADATA_PATH = 'metadata'


class MainScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.showFullScreen()
        self.setStyleSheet(f'background-color: {MAIN_COLOR}')

        self.games_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.games_layout)
        if not os.path.exists(METADATA_PATH):
            os.mkdir(METADATA_PATH)
        for game_name in config.games:
            self.game = QtWidgets.QPushButton(game_name)
            image_path = os.path.join(METADATA_PATH, game_name) + '.jpg'
            # todo cache properly inside metadata.py
            # urllib.request.urlretrieve(get_metadata(game_name)['image'], image_path)
            self.label = QLabel(self)
            self.image = QImage(image_path)
            pixmap = QPixmap(self.image)
            # todo maximize image, get rid of button text
            self.label.setPixmap(pixmap.scaled(self.label.size()*10, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.game.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.games_layout.addWidget(self.game)
            self.games_layout.addWidget(self.label)
            self.game.clicked.connect(partial(self.launch, game_name))

    def launch(self, game_name):
        self.hide()
        handler = resolve_handler(game_name)
        handler()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    main_screen = MainScreen()
    main_screen.show()

    sys.exit(app.exec_())
