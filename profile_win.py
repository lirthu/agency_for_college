import sys

from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.uic import loadUi


class ProfileWin(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui/profile_menu.ui", self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileWin()
    window.show()
    sys.exit(app.exec())
