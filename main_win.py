
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QComboBox, QListWidget
from PyQt6.uic import loadUi

from database import cur
from object import ObjectWin
from profile_win import ProfileWin


class MainWin(QWidget):
    comboBox: QComboBox
    listWidget_2: QListWidget
    listWidget: QListWidget
    def __init__(self, login_window = None):
        super().__init__()
        loadUi("ui/main.ui", self)
        self.login_window = login_window
        self.comboBox.currentIndexChanged.connect(self.change_index)
        self.comboBox.setCurrentIndex(0)

        self.listWidget_2.itemClicked.connect(self.open_object_card)
        self.listWidget.itemClicked.connect(self.filter_objects_category)
        self.show_objects()

    def show_objects(self):
        self.listWidget_2.clear()
        cur.execute("SELECT name FROM object")
        res = cur.fetchall()
        for row in res:
            name = row[0]
            self.listWidget_2.addItem(name)


    def change_index(self, index):
        if index == 1:
            self.open_profile_menu()
        elif index == 2:
            self.logout()

    def open_profile_menu(self):
        window = ProfileWin()
        window.exec()
        self.comboBox.setCurrentIndex(0)

    def open_object_card(self, item):
        name = item.text()
        cur.execute("SELECT id_object FROM object WHERE name = %s", (name,))
        res = cur.fetchall()

        if res:
            object_id = res[0][0]
            self.win = ObjectWin(object_id)
            self.win.exec()

    def logout(self):
        self.close()
        if self.login_window:
            self.login_window.show()
            self.comboBox.setCurrentIndex(0)

    def filter_objects_category(self, item):
        category = item.text()
        self.listWidget_2.clear()
        if category == 'Все':
            cur.execute("SELECT name FROM object")
        else:
            cur.execute("SELECT name FROM object WHERE type = %s", (category,))

        res = cur.fetchall()

        for row in res:
            name = row[0]
            self.listWidget_2.addItem(name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWin()
    window.show()
    sys.exit(app.exec())