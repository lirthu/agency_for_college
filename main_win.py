
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.uic import loadUi

from profile_win import ProfileWin


class MainWin(QWidget):
    def __init__(self, login_window = None):
        super().__init__()
        loadUi("ui/main.ui", self)
        self.login_window = login_window
        self.comboBox.currentIndexChanged.connect(self.change_index)
        self.comboBox.setCurrentIndex(0)

    def change_index(self, index):
        if index == 1:
            self.open_profile_menu()
        elif index == 2:
            self.logout()

    def open_profile_menu(self):
        window = ProfileWin()
        window.show()

    def logout(self):
        self.close()
        if self.login_window:
            self.login_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWin()
    window.show()
    sys.exit(app.exec())