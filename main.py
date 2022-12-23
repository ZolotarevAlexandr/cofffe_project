import sys

from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

import cgitb
cgitb.enable(format='text')


class CoffeeTableView(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee_db.sqlite')
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable('coffee')
        model.select()
        self.tableView.setModel(model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeTableView()
    ex.show()
    sys.exit(app.exec())
