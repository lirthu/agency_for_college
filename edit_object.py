from PyQt6.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from database import cur


class EditObjectWin(QDialog):
    def __init__(self, user_id, object_id=None):
        super().__init__()
        loadUi("ui/edit_object.ui", self)
        self.user_id = user_id
        self.object_id = object_id
        self.photo_data = None

        self.btnSave.clicked.connect(self.save)
        self.btnCancel.clicked.connect(self.reject)

        self.photo_label.mousePressEvent = self.choose_photo

        if object_id:
            self.load_object_data()

    def choose_photo(self, event):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите фото", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            with open(file_path, 'rb') as f:
                self.photo_data = f.read()
            pixmap = QPixmap()
            pixmap.loadFromData(self.photo_data)
            self.photo_label.setPixmap(pixmap.scaled(
                300, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            ))

    def load_object_data(self):
        cur.execute("SELECT type, name, address, square, price, photo_path FROM object WHERE id_object = %s",
                    (self.object_id,))
        res = cur.fetchone()

        if res:
            index = self.comboType.findText(res[0])
            if index >= 0:
                self.comboType.setCurrentIndex(index)
            self.lineName.setText(str(res[1]))
            self.lineAddress.setText(str(res[2]))
            self.lineSquare.setText(str(res[3]))
            self.linePrice.setText(str(res[4]))

            photo_blob = res[5]
            if photo_blob:
                pixmap = QPixmap()
                pixmap.loadFromData(photo_blob)
                self.photo_label.setPixmap(pixmap.scaled(
                    300, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))
                self.photo_data = photo_blob

    def save(self):
        obj_type = self.comboType.currentText()
        name = self.lineName.text()
        address = self.lineAddress.text()
        square = self.lineSquare.text()
        price = self.linePrice.text()

        if not all([name, address, square, price]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        if self.object_id:
            if self.photo_data:
                cur.execute("""
                    UPDATE object SET type=%s, name=%s, address=%s, square=%s, price=%s, photo_path=%s
                    WHERE id_object=%s AND client_id=%s
                """, (obj_type, name, address, float(square), float(price), self.photo_data, self.object_id,
                      self.user_id))
            else:
                cur.execute("""
                    UPDATE object SET type=%s, name=%s, address=%s, square=%s, price=%s
                    WHERE id_object=%s AND client_id=%s
                """, (obj_type, name, address, float(square), float(price), self.object_id, self.user_id))
        else:
            cur.execute("""
                INSERT INTO object (client_id, type, name, address, square, price, status, photo_path)
                VALUES (%s, %s, %s, %s, %s, %s, 'active', %s)
            """, (self.user_id, obj_type, name, address, float(square), float(price), self.photo_data))

        cur.connection.commit()
        self.accept()