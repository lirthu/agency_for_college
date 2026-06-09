import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.uic import loadUi

class TestWin(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui/edit_object.ui", self)
        print("UI загружен")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TestWin()
    win.show()
    sys.exit(app.exec())