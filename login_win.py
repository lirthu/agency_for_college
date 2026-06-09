import sys

from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt6.uic import loadUi

from database import cur
from hashed_passwds import hash_passwd
from main_win import MainWin
from reg_win import RegWin


class LoginWin(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("ui/login.ui", self)
        self.loginbtn.clicked.connect(self.login)
        self.regbtn.clicked.connect(self.open_reg)


    def login(self):
        self.line_login_field.setFocus()
        login = self.line_login_field.text()
        password = self.line_passwd_field.text()

        if not login:
            return QMessageBox.warning(self, "Ошибка", "Введите логин!")

        if not password:
            return QMessageBox.warning(self, "Ошибка", "Введите пароль!")

        hashpassword = hash_passwd(password)

        cur.execute("SELECT * FROM user WHERE login = %s AND password = %s", (login, hashpassword))

        res = cur.fetchall()

        if res:
            self.open_main()
            self.line_login_field.clear()
            self.line_passwd_field.clear()
        else:
            return QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")


    def open_main(self):
        self.close()
        self.win = MainWin(self)
        self.win.show()

    def open_reg(self):
        self.close()
        self.win = RegWin(self)
        self.win.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWin()
    window.show()
    sys.exit(app.exec())