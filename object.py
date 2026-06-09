import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QApplication, QLineEdit
from PyQt6.uic import loadUi

from database import cur


class ObjectWin(QDialog):
    label_11: QLineEdit
    def __init__(self, object_id):
        super().__init__()
        loadUi("ui/object.ui", self)
        self.object_id = object_id
        self.load_data()

    def load_data(self):
        cur.execute("SELECT o.type, concat(u.surname,' ', u.name, ' ', COALESCE(u.third_name, '')), u.phone, o.address, o.status, o.square, o.price, o.photo_path "
                    "FROM object o "
                    "JOIN client c ON o.client_id = c.client_id "
                    "JOIN user u ON c.client_id = u.id_user "
                    "WHERE o.id_object = %s", (self.object_id,))
        res = cur.fetchone()
        self.labelTypeValue.setText(str(res[0]))
        self.labelOwnerValue.setText(str(res[1]))
        self.labelPhoneValue.setText(str(res[2]))
        self.labelAddressValue.setText(str(res[3]))
        self.labelStatusValue.setText(str(res[4]))
        self.labelSquareValue.setText(str(res[5]))
        self.labelPriceValue.setText(f"{res[6]:,.0f} руб")

        photo_blob = res[7]
        if photo_blob:
            pixmap = QPixmap()
            pixmap.loadFromData(photo_blob)
            self.photo_label.setPixmap(pixmap)
        else:
            self.photo_label.setText("Нет фото")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ObjectWin(1)
    win.show()
    sys.exit(app.exec())