import sys
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QInputDialog
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from database import cur, connection


class AdminWin(QWidget):
    def __init__(self, user_id, surname, name, login_window=None):
        super().__init__()
        loadUi("ui/admin.ui", self)
        self.user_id = user_id
        self.login_window = login_window

        self.label.setText(f"Добро пожаловать, {surname} {name}")

        self.pushButton_2.clicked.connect(self.edit_item)
        self.pushButton_3.clicked.connect(self.delete_item)
        self.pushButton_4.clicked.connect(self.logout)

        self.tabWidget.currentChanged.connect(self.on_tab_changed)

        self.load_users()
        self.load_objects()
        self.load_contracts()

    def get_current_tab(self):
        return self.tabWidget.currentIndex()

    def on_tab_changed(self, index):
        if index == 0:
            self.load_users()
        elif index == 1:
            self.load_objects()
        elif index == 2:
            self.load_contracts()

    def load_users(self):
        cur.execute("""
            SELECT u.id_user, u.surname, u.name, u.phone, u.login, u.role,
                   CASE WHEN c.client_id IS NOT NULL THEN 'client' ELSE 'employee' END as user_type
            FROM user u
            LEFT JOIN client c ON u.id_user = c.client_id
            ORDER BY u.id_user
        """)
        users = cur.fetchall()

        table = self.tableWidget
        table.setRowCount(len(users))
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["ID", "Фамилия", "Имя", "Телефон", "Логин", "Роль"])

        for row, user in enumerate(users):
            table.setItem(row, 0, self.create_item(str(user[0])))
            table.setItem(row, 1, self.create_item(user[1] or ''))
            table.setItem(row, 2, self.create_item(user[2] or ''))
            table.setItem(row, 3, self.create_item(user[3] or ''))
            table.setItem(row, 4, self.create_item(user[4] or ''))
            table.setItem(row, 5, self.create_item(user[5] or ''))

        table.resizeColumnsToContents()

    def load_objects(self):
        cur.execute("""
            SELECT o.id_object, o.name, o.type, o.address, o.square, o.price, o.status,
                   u.surname, u.name
            FROM object o
            JOIN client c ON o.client_id = c.client_id
            JOIN user u ON c.client_id = u.id_user
            ORDER BY o.id_object
        """)
        objects = cur.fetchall()

        table = self.tableWidget_2
        table.setRowCount(len(objects))
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(["ID", "Название", "Тип", "Адрес", "Площадь", "Цена", "Статус", "Владелец"])

        for row, obj in enumerate(objects):
            table.setItem(row, 0, self.create_item(str(obj[0])))
            table.setItem(row, 1, self.create_item(obj[1] or ''))
            table.setItem(row, 2, self.create_item(obj[2] or ''))
            table.setItem(row, 3, self.create_item(obj[3] or ''))
            table.setItem(row, 4, self.create_item(str(obj[4])))
            table.setItem(row, 5, self.create_item(f"{obj[5]:,.0f}"))
            table.setItem(row, 6, self.create_item(obj[6] or ''))
            table.setItem(row, 7, self.create_item(f"{obj[7]} {obj[8]}"))

        table.resizeColumnsToContents()

    def load_contracts(self):
        cur.execute("""
            SELECT c.id_contract, u.surname, u.name, c.type_contract, o.address, c.price, c.date, c.status
            FROM contract c
            JOIN client cl ON c.client_id = cl.client_id
            JOIN user u ON cl.client_id = u.id_user
            JOIN object o ON c.object_id = o.id_object
            ORDER BY c.id_contract
        """)
        contracts = cur.fetchall()

        table = self.tableWidget_3
        table.setRowCount(len(contracts))
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(["ID", "Клиент", "Тип", "Объект", "Сумма", "Дата", "Статус"])

        for row, contract in enumerate(contracts):
            table.setItem(row, 0, self.create_item(str(contract[0])))
            table.setItem(row, 1, self.create_item(f"{contract[1]} {contract[2]}"))
            table.setItem(row, 2, self.create_item(contract[3] or ''))
            table.setItem(row, 3, self.create_item(contract[4] or ''))
            table.setItem(row, 4, self.create_item(f"{contract[5]:,.0f}"))
            table.setItem(row, 5, self.create_item(str(contract[6])))
            table.setItem(row, 6, self.create_item(contract[7] or ''))

        table.resizeColumnsToContents()

    def create_item(self, text):
        item = QTableWidgetItem(str(text))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        return item

    def get_selected_id(self):
        tab = self.get_current_tab()
        if tab == 0:
            row = self.tableWidget.currentRow()
            if row >= 0:
                return int(self.tableWidget.item(row, 0).text())
        elif tab == 1:
            row = self.tableWidget_2.currentRow()
            if row >= 0:
                return int(self.tableWidget_2.item(row, 0).text())
        elif tab == 2:
            row = self.tableWidget_3.currentRow()
            if row >= 0:
                return int(self.tableWidget_3.item(row, 0).text())
        return None

    def edit_item(self):
        item_id = self.get_selected_id()
        if item_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите запись")
            return

        tab = self.get_current_tab()
        if tab == 0:
            self.edit_user(item_id)
        elif tab == 1:
            self.edit_object(item_id)
        elif tab == 2:
            self.edit_contract(item_id)

    def edit_user(self, user_id):
        new_role, ok = QInputDialog.getItem(self, "Смена роли", "Выберите новую роль:", ["client", "employee"], 0,
                                            False)
        if ok and new_role:
            cur.execute("UPDATE user SET role = %s WHERE id_user = %s", (new_role, user_id))
            if new_role == 'client':
                cur.execute("DELETE FROM employee WHERE employee_id = %s", (user_id,))
                cur.execute("INSERT INTO client (client_id, type) VALUES (%s, 'физ лицо')", (user_id,))
            else:
                cur.execute("DELETE FROM client WHERE client_id = %s", (user_id,))
                cur.execute("INSERT INTO employee (employee_id) VALUES (%s)", (user_id,))
            connection.commit()
            QMessageBox.information(self, "Успех", "Роль изменена")
            self.load_users()

    def edit_object(self, obj_id):
        statuses = ["active", "sold", "inactive"]
        new_status, ok = QInputDialog.getItem(self, "Смена статуса", "Выберите статус:", statuses, 0, False)
        if ok and new_status:
            cur.execute("UPDATE object SET status = %s WHERE id_object = %s", (new_status, obj_id))
            connection.commit()
            QMessageBox.information(self, "Успех", "Статус изменен")
            self.load_objects()

    def edit_contract(self, contract_id):
        statuses = ["pending", "active", "completed", "cancelled"]
        new_status, ok = QInputDialog.getItem(self, "Смена статуса договора", "Выберите статус:", statuses, 0, False)
        if ok and new_status:
            cur.execute("UPDATE contract SET status = %s WHERE id_contract = %s", (new_status, contract_id))
            connection.commit()
            QMessageBox.information(self, "Успех", "Статус договора изменен")
            self.load_contracts()

    def delete_item(self):
        item_id = self.get_selected_id()
        if item_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите запись")
            return

        tab = self.get_current_tab()
        reply = QMessageBox.question(self, "Подтверждение", "Удалить запись?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply != QMessageBox.StandardButton.Yes:
            return

        if tab == 0:
            if item_id == self.user_id:
                QMessageBox.warning(self, "Ошибка", "Нельзя удалить себя")
                return
            cur.execute("DELETE FROM user WHERE id_user = %s", (item_id,))
            connection.commit()
            self.load_users()
        elif tab == 1:
            cur.execute("DELETE FROM object WHERE id_object = %s", (item_id,))
            connection.commit()
            self.load_objects()
        elif tab == 2:
            cur.execute("DELETE FROM contract WHERE id_contract = %s", (item_id,))
            connection.commit()
            self.load_contracts()

        QMessageBox.information(self, "Успех", "Запись удалена")

    def logout(self):
        self.close()
        if self.login_window:
            self.login_window.show()
        else:
            from login_win import LoginWin
            self.login = LoginWin()
            self.login.show()