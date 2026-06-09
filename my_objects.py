from PyQt6.QtWidgets import QDialog, QMessageBox, QListWidgetItem
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from database import cur
from edit_object import EditObjectWin


class MyObjects(QDialog):
    def __init__(self, user_id):
        super().__init__()
        loadUi("ui/my_objects.ui", self)
        self.user_id = user_id
        self.btnAdd.clicked.connect(self.add_object)
        self.btnEdit.clicked.connect(self.edit_object)
        self.btnDelete.clicked.connect(self.delete_object)
        self.pushButton_4.clicked.connect(self.close)
        self.load_objects()

    def load_objects(self):
        self.listWidget.clear()
        cur.execute("SELECT id_object, name, address, price FROM object WHERE client_id = %s", (self.user_id,))
        objects = cur.fetchall()

        for obj in objects:
            text = f"{obj[1]} | {obj[2]} | {obj[3]:,.0f} руб"
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, obj[0])
            self.listWidget.addItem(item)

    def add_object(self):
        win = EditObjectWin(self.user_id)
        if win.exec():
            self.load_objects()

    def edit_object(self):
        current = self.listWidget.currentRow()
        if current < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите объект")
            return

        item = self.listWidget.currentItem()
        object_id = item.data(Qt.ItemDataRole.UserRole)

        win = EditObjectWin(self.user_id, object_id)
        if win.exec():
            self.load_objects()

    def delete_object(self):
        current = self.listWidget.currentRow()
        if current < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите объект")
            return

        item = self.listWidget.currentItem()
        object_id = item.data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(self, "Подтверждение", "Удалить объект?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            cur.execute("DELETE FROM object WHERE id_object = %s AND client_id = %s", (object_id, self.user_id))
            cur.connection.commit()
            self.load_objects()
