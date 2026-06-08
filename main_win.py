
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.uic import loadUi



class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("ui/main.ui", self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWin()
    window.show()
    sys.exit(app.exec())