from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from database import cur
from payments import PaymentsWin


class MyContracts(QDialog):
    def __init__(self, user_id):
        super().__init__()
        loadUi("ui/my_contracts.ui", self)
        self.user_id = user_id

        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.open_payments)

        self.load_contracts()

    def load_contracts(self):
        cur.execute("""
            SELECT c.id_contract, c.type_contract, o.name, o.address, c.price, c.date, c.status
            FROM contract c
            JOIN object o ON c.object_id = o.id_object
            WHERE c.client_id = %s
            ORDER BY c.date DESC
        """, (self.user_id,))
        contracts = cur.fetchall()

        table = self.tableWidget
        table.setRowCount(len(contracts))
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(["ID", "Тип договора", "Объект", "Адрес", "Сумма", "Дата", "Статус"])

        for row, contract in enumerate(contracts):
            table.setItem(row, 0, self.create_item(str(contract[0])))
            table.setItem(row, 1, self.create_item(contract[1] or ''))
            table.setItem(row, 2, self.create_item(contract[2] or ''))
            table.setItem(row, 3, self.create_item(contract[3] or ''))
            table.setItem(row, 4, self.create_item(f"{contract[4]:,.0f} руб"))
            table.setItem(row, 5, self.create_item(str(contract[5])))
            table.setItem(row, 6, self.create_item(contract[6] or ''))

        table.resizeColumnsToContents()

    def open_payments(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите договор для просмотра платежей")
            return

        contract_id = int(self.tableWidget.item(row, 0).text())
        window = PaymentsWin(self.user_id, contract_id, self)
        window.exec()

    def create_item(self, text):
        item = QTableWidgetItem(str(text))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        return item