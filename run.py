import sys

from PySide2 import QtWidgets

from handlers.borderlands2 import handler

MAIN_COLOR = '#d5d927'


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.showFullScreen()
        self.setStyleSheet(f'background-color: {MAIN_COLOR}')

        self.game1 = QtWidgets.QPushButton('borderlands2')

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.game1)
        self.setLayout(self.layout)

        self.game1.clicked.connect(self.launch_game1)

    def launch_game1(self):
        handler()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())
