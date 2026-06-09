import sys

from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt6.uic import loadUi

from database import cur
from hashed_passwds import hash_passwd


class ProfileWin(QDialog):
    def __init__(self, user_id):
        super().__init__()
        loadUi("ui/profile_menu.ui", self)
        self.user_id = user_id
        self.load_data()
        self.pushButton.clicked.connect(self.save_new_password)

    def load_data(self):
        cur.execute("SELECT concat(u.surname,' ', u.name, ' ', COALESCE(u.third_name, '')), c.type, u.phone, u.email "
                    "FROM user u "
                    "JOIN client c on c.client_id = u.id_user "
                    "WHERE u.id_user = %s", (self.user_id,))
        res = cur.fetchone()
        self.label_4.setText(str(res[0]))
        self.label_9.setText(str(res[1]))
        self.label_10.setText(str(res[2]))
        self.label_11.setText(str(res[3]))

    def save_new_password(self):
        f_password = self.lineEdit_2.text()
        sec_password = self.lineEdit.text()
        if not f_password or not sec_password:
            return QMessageBox.warning(self, "Error!", "Enter all fields")
        if f_password != sec_password:
            return QMessageBox.warning(self, "Error!", "Password must be the same")
        hashpasword = hash_passwd(f_password)
        cur.execute("UPDATE user SET password = %s WHERE id_user = %s", (hashpasword, self.user_id,))
        cur.connection.commit()
        self.lineEdit_2.clear()
        self.lineEdit.clear()
        QMessageBox.information(self, "Success", "Password changed")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileWin(1)
    window.show()
    sys.exit(app.exec())
