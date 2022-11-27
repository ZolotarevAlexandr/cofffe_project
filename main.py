import sys

from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

import sqlite3

from ui import main_ui, edit_ui

import cgitb
cgitb.enable(format='text')


class CoffeeTableView(QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('data/coffee_db.sqlite')
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable('coffee')
        model.select()
        self.tableView.setModel(model)

        self.edit_btn.clicked.connect(self.open_edit)

    def open_edit(self):
        self.edit_window = EditView()
        self.edit_window.show()
        self.close()


class EditView(QMainWindow, edit_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ok_btn.clicked.connect(self.save_changes)
        self.id_inp.valueChanged.connect(self.set_selected)

    def save_changes(self):
        id_of_element = self.id_inp.value()

        new_sort = self.sort_inp.text()
        new_roast = self.roast_inp.currentText()
        new_grains = self.grains_inp.currentText()
        new_description = self.description_inp.toPlainText()
        new_price = int(self.price_inp.text())
        new_size = int(self.size_inp.text())

        with sqlite3.connect('data/coffee_db.sqlite') as con:
            cur = con.cursor()
            max_id = cur.execute(f"""
            SELECT id FROM coffee
            ORDER BY id DESC
            """).fetchone()

        with sqlite3.connect('data/coffee_db.sqlite') as con:
            cur = con.cursor()
            if id_of_element <= max_id[0]:
                cur.execute(f"""
                UPDATE coffee
                SET sort = '{new_sort}',
                    roast = '{new_roast}',
                    grains = '{new_grains}',
                    description = '{new_description}',
                    price = {new_price},
                    size_in_grams = {new_size}
                WHERE id = {id_of_element}
                """)
            else:
                cur.execute(f"""
                INSERT INTO coffee VALUES (
                    {id_of_element},
                    '{new_sort}',
                    '{new_roast}',
                    '{new_grains}',
                    '{new_description}',
                    {new_price},
                    {new_size})
                """)
            con.commit()

        self.coffee_table = CoffeeTableView()
        self.coffee_table.show()
        self.close()

    def set_selected(self):
        id_of_element = self.id_inp.value()
        with sqlite3.connect('data/coffee_db.sqlite') as con:
            cur = con.cursor()
            result = cur.execute(f"""
            SELECT * FROM coffee
            WHERE id = {id_of_element}
            """).fetchone()
            con.commit()
        try:
            self.sort_inp.setText(result[1])
            self.roast_inp.setCurrentIndex(self.roast_inp.findText(result[2]))
            self.grains_inp.setCurrentIndex(self.grains_inp.findText(result[3]))
            self.description_inp.setPlainText(result[4])
            self.price_inp.setText(str(result[5]))
            self.size_inp.setText(str(result[6]))
            self.error_label.clear()
        except TypeError:
            self.sort_inp.clear()
            self.roast_inp.setCurrentIndex(1)
            self.grains_inp.setCurrentIndex(1)
            self.description_inp.clear()
            self.price_inp.clear()
            self.size_inp.clear()
            self.error_label.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeTableView()
    ex.show()
    sys.exit(app.exec())
