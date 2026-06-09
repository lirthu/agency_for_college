import sys

from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt6.uic import loadUi

from database import cur, get_user_role
from hashed_passwds import hash_passwd
from main_win import MainWin
from reg_win import RegWin
# from admin_win import AdminWin

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
        res = cur.fetchone()

        if res:
            user_id = res[0]
            role = get_user_role(user_id)

            if role == 'client':
                self.open_main(user_id)
            else:
                self.open_admin(user_id)

            self.line_login_field.clear()
            self.line_passwd_field.clear()
        else:
            return QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def open_admin(self, user_id):
        from admin_win import AdminWin
        cur.execute("SELECT surname, name FROM user WHERE id_user = %s", (user_id,))
        user = cur.fetchone()
        self.close()
        self.admin_win = AdminWin(user_id, user[0], user[1], login_window=self)
        self.admin_win.show()

    def open_main(self, user_id):
        self.close()
        self.win = MainWin(user_id, login_window=self)
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