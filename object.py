import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QApplication, QLineEdit, QMessageBox
from PyQt6.uic import loadUi
from datetime import datetime
from database import cur, connection


class ObjectWin(QDialog):
    def __init__(self, object_id, user_id):
        super().__init__()
        loadUi("ui/object.ui", self)
        self.object_id = object_id
        self.user_id = user_id

        if hasattr(self, 'btnClose'):
            self.btnClose.clicked.connect(self.buy_object)
        elif hasattr(self, 'pushButton'):
            self.pushButton.clicked.connect(self.buy_object)

        self.load_data()

    def load_data(self):
        cur.execute(
            "SELECT o.type, concat(u.surname,' ', u.name, ' ', COALESCE(u.third_name, '')), u.phone, o.address, o.status, o.square, o.price, o.photo_path "
            "FROM object o "
            "JOIN client c ON o.client_id = c.client_id "
            "JOIN user u ON c.client_id = u.id_user "
            "WHERE o.id_object = %s", (self.object_id,))
        res = cur.fetchone()

        if not res:
            QMessageBox.warning(self, "Ошибка", "Объект не найден")
            self.close()
            return

        if hasattr(self, 'labelTypeValue'):
            self.labelTypeValue.setText(str(res[0]))
        if hasattr(self, 'labelOwnerValue'):
            self.labelOwnerValue.setText(str(res[1]))
        if hasattr(self, 'labelPhoneValue'):
            self.labelPhoneValue.setText(str(res[2]))
        if hasattr(self, 'labelAddressValue'):
            self.labelAddressValue.setText(str(res[3]))
        if hasattr(self, 'labelStatusValue'):
            self.labelStatusValue.setText(str(res[4]))
        if hasattr(self, 'labelSquareValue'):
            self.labelSquareValue.setText(str(res[5]))
        if hasattr(self, 'labelPriceValue'):
            self.labelPriceValue.setText(f"{res[6]:,.0f} руб")

        photo_blob = res[7]
        if photo_blob and hasattr(self, 'photo_label'):
            pixmap = QPixmap()
            pixmap.loadFromData(photo_blob)
            self.photo_label.setPixmap(pixmap)
        elif hasattr(self, 'photo_label'):
            self.photo_label.setText("Нет фото")

    def buy_object(self):
        try:
            cur.execute("SELECT status, client_id, price FROM object WHERE id_object = %s", (self.object_id,))
            obj = cur.fetchone()

            if not obj:
                QMessageBox.warning(self, "Ошибка", "Объект не найден")
                return

            if obj[0] != 'active':
                QMessageBox.warning(self, "Ошибка", "Этот объект уже продан или неактивен")
                return

            if obj[1] == self.user_id:
                QMessageBox.warning(self, "Ошибка", "Нельзя купить свой собственный объект")
                return

            cur.execute("SELECT employee_id FROM employee LIMIT 1")
            emp = cur.fetchone()
            employee_id = emp[0] if emp else None

            today = datetime.now().strftime("%Y-%m-%d")

            cur.execute("""
                INSERT INTO contract (client_id, employee_id, object_id, type_contract, date, price, status)
                VALUES (%s, %s, %s, 'купля-продажа', %s, %s, 'pending')
            """, (self.user_id, employee_id, self.object_id, today, obj[2]))
            connection.commit()

            cur.execute("UPDATE object SET status = 'sold' WHERE id_object = %s", (self.object_id,))
            connection.commit()

            QMessageBox.information(self, "Успех", "Договор купли-продажи создан!\nОбъект помечен как проданный.")
            self.accept()

        except Exception as e:
            connection.rollback()
            QMessageBox.warning(self, "Ошибка", f"Не удалось создать договор: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ObjectWin(1, 1)
    win.show()
    sys.exit(app.exec())