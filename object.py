import sys

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
        cur.execute("SELECT o.type, concat(u.surname,' ', u.name, ' ', COALESCE(u.third_name, '')), u.phone, o.address, o.status, o.square, o.price "
                    "FROM object o "
                    "JOIN client c ON o.client_id = c.client_id "
                    "JOIN user u ON c.client_id = u.id_user "
                    "WHERE o.id_object = %s", (self.object_id,))
        res = cur.fetchone()
        print(f"Результат: {res}")  # Что выводится?
        print(f"Тип результата: {type(res)}")

        if res:
            print(f"Количество полей: {len(res)}")
            for i, val in enumerate(res):
                print(f"Поле {i}: {val}")
        else:
            print("Результат пустой!")
        self.label_11.setText(str(res[0]))
        self.label_12.setText(str(res[1]))
        self.label_13.setText(str(res[2]))
        self.label_14.setText(str(res[3]))
        self.label_15.setText(str(res[4]))
        self.label_16.setText(str(res[5]))
        self.label_17.setText(str(res[6]))





if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ObjectWin(1)
    win.show()
    sys.exit(app.exec())