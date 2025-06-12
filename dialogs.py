from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
)
from database import get_all_authors, get_all_entries

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

        self.cancel_button = QPushButton("Cancel")
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