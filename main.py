import sys
from PyQt6.QtWidgets import QApplication
from login_win import LoginWin

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWin()
    window.show()
    sys.exit(app.exec())