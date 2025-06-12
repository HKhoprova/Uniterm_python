import sys
from PyQt5.QtWidgets import (
    QWidget,  QLabel, QLineEdit, QPushButton, QApplication,
    QRadioButton, QButtonGroup, QVBoxLayout, QHBoxLayout, QMessageBox
)
from canvas import UnitermCanvas

class UnitermApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Uniterm Transformer")
        self.canvas = UnitermCanvas()
        self.canvas.setMinimumHeight(300)

        # Input sekwencjonowanie
        self.seq_label = QLabel("Pozioma operacja sekwencjowania:")
        self.seq_field1 = QLineEdit()
        self.seq_field2 = QLineEdit()
        self.seq_button = QPushButton("Dodaj")
        self.seq_button.clicked.connect(self.show_seq)

        # Input zrównoleglenie
        self.paral_label = QLabel("Pozioma operacja zrównoleglenia:")
        self.paral_field1 = QLineEdit()
        self.paral_field2 = QLineEdit()
        self.paral_button = QPushButton("Dodaj")
        self.paral_button.clicked.connect(self.show_paral)

        # Ustawienia zamiany
        self.radio_label = QLabel("Wybierz uniterm do zamiany:")
        self.radiobutton1 = QRadioButton("Pierwszy")
        self.radiobutton2 = QRadioButton("Drugi")
        radio_group = QButtonGroup()
        radio_group.addButton(self.radiobutton1)
        radio_group.addButton(self.radiobutton2)
        self.radiobutton1.setChecked(True)
        self.transform_button = QPushButton("Zamień")
        self.transform_button.clicked.connect(self.show_transform)

        # Widok okna
        window_layout = QVBoxLayout()
        settings_layout = QHBoxLayout()
        seq_layout = QVBoxLayout()
        paral_layout = QVBoxLayout()
        transform_layout = QVBoxLayout()

        window_layout.addLayout(settings_layout)
        window_layout.addWidget(self.canvas)
        settings_layout.addLayout(seq_layout)
        settings_layout.addLayout(paral_layout)
        settings_layout.addLayout(transform_layout)
        seq_layout.addWidget(self.seq_label)
        seq_layout.addWidget(self.seq_field1)
        seq_layout.addWidget(self.seq_field2)
        seq_layout.addWidget(self.seq_button)
        paral_layout.addWidget(self.paral_label)
        paral_layout.addWidget(self.paral_field1)
        paral_layout.addWidget(self.paral_field2)
        paral_layout.addWidget(self.paral_button)
        transform_layout.addWidget(self.radio_label)
        transform_layout.addWidget(self.radiobutton1)
        transform_layout.addWidget(self.radiobutton2)
        transform_layout.addWidget(self.transform_button)

        self.setLayout(window_layout)

    def show_seq(self):
        a = self.seq_field1.text()
        b = self.seq_field2.text()
        if a and b:
            self.canvas.draw_seq(a, b)
        else:
            self.handle_error("Wprowadź unitermy i spróbuj ponownie.")

    def show_paral(self):
        a = self.paral_field1.text().strip()
        b = self.paral_field2.text().strip()
        if a and b:
            self.canvas.draw_paral(a, b)
        else:
            self.handle_error("Wprowadź unitermy i spróbuj ponownie.")

    def show_transform(self):
        sa = self.seq_field1.text().strip()
        sb = self.seq_field2.text().strip()
        pa = self.paral_field1.text().strip()
        pb = self.paral_field2.text().strip()

        if not sa or not sb or not pa or not pb:
            self.handle_error("Dodaj operacje i spróbuj ponownie.")
            return
        
        replace_first = self.radiobutton1.isChecked()
        self.canvas.draw_transformed(sa, sb, pa, pb, replace_first)

    def handle_error(self, message):
        QMessageBox.critical(self, "Błąd", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UnitermApp()
    window.resize(800, 500)
    window.show()
    sys.exit(app.exec_())