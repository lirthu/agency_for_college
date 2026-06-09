from PyQt6.QtWidgets import QDialog, QTableWidgetItem
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from database import cur


class PaymentsWin(QDialog):
    def __init__(self, user_id, contract_id, parent=None):
        super().__init__(parent)
        loadUi("ui/payments.ui", self)
        self.user_id = user_id
        self.contract_id = contract_id
        self.parent_window = parent

        self.pushButton.clicked.connect(self.back_to_contracts)
        self.pushButton_2.clicked.connect(self.exit_to_menu)

        self.load_payments()

    def load_payments(self):
        cur.execute("""
            SELECT p.id_payment, p.type_payment, p.price, p.date, p.status
            FROM payment p
            WHERE p.contract_id = %s
            ORDER BY p.date DESC
        """, (self.contract_id,))
        payments = cur.fetchall()

        table = self.tableWidget
        table.setRowCount(len(payments))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Тип платежа", "Сумма", "Дата", "Статус"])

        for row, payment in enumerate(payments):
            table.setItem(row, 0, self.create_item(str(payment[0])))
            table.setItem(row, 1, self.create_item(payment[1] or ''))
            table.setItem(row, 2, self.create_item(f"{payment[2]:,.0f} руб"))
            table.setItem(row, 3, self.create_item(str(payment[3])))
            table.setItem(row, 4, self.create_item(payment[4] or ''))

        table.resizeColumnsToContents()

    def back_to_contracts(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()

    def exit_to_menu(self):
        self.close()
        if self.parent_window:
            self.parent_window.close()

    def create_item(self, text):
        item = QTableWidgetItem(str(text))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        return item