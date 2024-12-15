import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTableView, QMessageBox)
from PyQt5.QtSql import QSqlDatabase, QSqlRelationalTableModel, QSqlQuery
from PyQt5.QtCore import QDateTime

def setup_database():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("mydatabase.db")

    if not db.open():
        print("Ошибка подключения к базе данных.")
        return

    query = QSqlQuery()
    query.exec_("CREATE TABLE IF NOT EXISTS Variants ("
                 "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                 "teacher TEXT NOT NULL, "
                 "variant TEXT NOT NULL, "
                 "created_at DATETIME DEFAULT CURRENT_TIMESTAMP);")

    db.close()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Variants Database')

        self.teacher_label = QLabel('Teacher:')
        self.teacher_edit = QLineEdit()
        self.variant_label = QLabel('Variant Name:')
        self.variant_edit = QLineEdit()

        self.add_button = QPushButton('Add Variant')
        self.add_button.clicked.connect(self.add_variant)

        self.delete_button = QPushButton('Delete Variant')
        self.delete_button.clicked.connect(self.delete_variant)

        self.table = QTableView()
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("Variants")
        self.model.select()
        self.table.setModel(self.model)

        vbox = QVBoxLayout()
        vbox.addWidget(self.teacher_label)
        vbox.addWidget(self.teacher_edit)
        vbox.addWidget(self.variant_label)
        vbox.addWidget(self.variant_edit)
        vbox.addWidget(self.add_button)
        vbox.addWidget(self.delete_button)
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def add_variant(self):
        teacher = self.teacher_edit.text().strip()
        variant = self.variant_edit.text().strip()

        if not teacher or not variant:
            QMessageBox.warning(self, 'Input Error', 'All fields are required!')
            return

        conn = QSqlDatabase.database()
        query = QSqlQuery(conn)
        query.prepare("INSERT INTO Variants (teacher, variant) VALUES (:teacher, :variant)")
        query.bindValue(":teacher", teacher)
        query.bindValue(":variant", variant)

        if not query.exec_():
            QMessageBox.warning(self, 'Database Error', 'Failed to add variant!')
        else:
            self.model.select()

        self.teacher_edit.clear()
        self.variant_edit.clear()

    def delete_variant(self):
        selected_row = self.table.currentIndex().row()
        if selected_row < 0:
            QMessageBox.warning(self, 'Selection Error', 'Please select a variant to delete!')
            return

        variant_id = self.model.index(selected_row, 0).data()

        query = QSqlQuery()
        query.prepare("DELETE FROM Variants WHERE id = :id")
        query.bindValue(":id", variant_id)

        if not query.exec_():
            QMessageBox.warning(self, 'Database Error', 'Failed to delete variant!')
        else:
            self.model.select()

if __name__ == '__main__':
    setup_database()
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
