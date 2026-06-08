import sys

from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt6.uic import loadUi

from database import cur
from hashed_passwds import hash_passwd
from main_win import MainWin


class RegWin(QWidget):
    def __init__(self, login_window = None):
        super().__init__()
        loadUi("ui/reg.ui", self)
        self.login_window = login_window
        self.regbtn.clicked.connect(self.registration)
        self.cancel.clicked.connect(self.cancel_login)

    def registration(self):
        surename = self.lineEdit.text()
        name = self.lineEdit_2.text()
        thirdname = self.lineEdit_3.text()
        phone = self.lineEdit_7.text()
        email = self.lineEdit_8.text()
        login = self.lineEdit_4.text()
        password = self.lineEdit_5.text()
        return_password = self.lineEdit_6.text()

        if not surename or not name or not thirdname or not login or not password or not return_password:
            return QMessageBox.warning(self, "Error", "fill all fields")

        if password != return_password:
            return QMessageBox.warning(self, "Error", "Passwords must be the same")

        hashpassword = hash_passwd(password)
        cur.execute("SELECT 1 FROM user WHERE login = %s", (login,))
        res = cur.fetchall()

        if res:
            return QMessageBox.warning(self, "Error", "User with this login already exists")

        cur.execute("INSERT INTO user (role, surname, name, third_name, phone, email, login, password) VALUES ('client', %s, %s, %s, %s, %s, %s, %s)", (surename, name, thirdname, phone, email, login, hashpassword))
        cur.connection.commit()
        self.reg_open_main()


    def reg_open_main(self):
        self.close()
        self.win = MainWin()
        self.win.show()

    def cancel_login(self):
        self.close()
        if self.login_window:
            self.login_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegWin()
    window.show()
    sys.exit(app.exec())