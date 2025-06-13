from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
)
from database import get_all_authors, get_all_entries, delete_entry

class SaveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Zapisz dane")
        self.setMinimumWidth(300)

        self.title_label = QLabel("Nazwa (wymagana):")
        self.title_field = QLineEdit()

        self.author_label = QLabel("Autor (opcjonalnie):")
        self.author_input = QComboBox()
        self.author_input.setEditable(True)
        self.author_input.addItems(sorted(get_all_authors()))

        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.clicked.connect(self.reject)
        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.handle_save)

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        layout.addWidget(self.title_label)
        layout.addWidget(self.title_field)
        layout.addWidget(self.author_label)
        layout.addWidget(self.author_input)
        layout.addLayout(button_layout)

        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)

        self.setLayout(layout)

    def get_values(self):
        return self.title_field.text().strip(), self.author_input.currentText().strip()
    
    def handle_save(self):
        title = self.title_field.text().strip()
        if not title:
            QMessageBox.warning(self, "Błąd", "Tytuł nie może być pusty.")
            return
        self.accept()

class LoadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Wybierz zapis")
        self.setMinimumSize(500, 300)

        self.selected_entry = None

        entries = list(reversed(get_all_entries()))

        self.table = QTableWidget(len(entries), 3)
        self.table.setHorizontalHeaderLabels(["Tytuł", "Autor", "Data i czas zapisu"])

        for i, entry in enumerate(entries):
            self.table.setItem(i, 0, QTableWidgetItem(entry["title"]))
            self.table.setItem(i, 1, QTableWidgetItem(entry["author"]))
            self.table.setItem(i, 2, QTableWidgetItem(entry["datetime"]))

        self.table.cellDoubleClicked.connect(self.choose_entry)

        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.clicked.connect(self.reject)
        self.delete_button = QPushButton("Usuń zaznaczone")
        self.delete_button.clicked.connect(self.handle_delete)
        self.open_button = QPushButton("Otwórz")
        self.open_button.clicked.connect(self.handle_open)

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.open_button)

        self.setLayout(layout)

    def choose_entry(self, row, _column):
        all_entries = list(reversed(get_all_entries()))
        self.selected_entry = all_entries[row]
        self.accept()

    def handle_open(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Błąd", "Nie wybrano rekordu do otwarcia.")
            return

        self.choose_entry(row, 0)

    def handle_delete(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Błąd", "Nie wybrano rekordu do usunięcia.")
            return
        
        title = self.table.item(row, 0).text()
        confirm = QMessageBox.question(
            self, "Potwierdź usunięcie", f"Czy na pewno chcesz usunąć zapis: \"{title}\"?",
            QMessageBox.No | QMessageBox.Yes
        )
        if confirm == QMessageBox.Yes:
            author = self.table.item(row, 1).text()
            datetime = self.table.item(row, 2).text()
            delete_entry(title, author, datetime)
            QMessageBox.information(self, "Usunięto", f"Zapis \"{title}\" został usunięty.")
            self.refresh_table()

    def refresh_table(self):
        entries = list(reversed(get_all_entries()))
        self.table.setRowCount(len(entries))
        for i, entry in enumerate(entries):
            self.table.setItem(i, 0, QTableWidgetItem(entry["title"]))
            self.table.setItem(i, 1, QTableWidgetItem(entry.get("author", "")))
            self.table.setItem(i, 2, QTableWidgetItem(entry["datetime"]))

    def get_selected(self):
        return self.selected_entry