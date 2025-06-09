import sys
from PyQt5.QtWidgets import (
    QWidget,  QLabel, QLineEdit, QPushButton, QTextEdit,
    QRadioButton, QButtonGroup, QVBoxLayout, QHBoxLayout, QApplication
)

class UnitermApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Uniterm Transformer")

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

        # Output obu operacji będzie później wyświetlany na canvas
        self.output_seq_label = QLabel("Sekwencjowanie:")
        self.output_seq_field = QTextEdit()
        self.output_seq_field.setReadOnly(True)
        self.output_paral_label = QLabel("Zrównoleglenie:")
        self.output_paral_field = QTextEdit()
        self.output_paral_field.setReadOnly(True)

        # Ustawienia zamiany
        self.radio_label = QLabel("Wybierz uniterm do zamiany:")
        self.radiobutton1 = QRadioButton("Pierwszy")
        self.radiobutton2 = QRadioButton("Drugi")
        radio_group = QButtonGroup()
        radio_group.addButton(self.radiobutton1)
        radio_group.addButton(self.radiobutton2)
        self.transform_button = QPushButton("Zamień")
        self.transform_button.clicked.connect(self.show_transform)

        # Output będzie później wyświetlany na canvas
        self.output_transform_label = QLabel("Wynik zamiany:")
        self.output_transform_field = QTextEdit()
        self.output_transform_field.setReadOnly(True)

        # Widok okna
        window_layout = QVBoxLayout()
        settings_layout = QHBoxLayout()
        seq_layout = QVBoxLayout()
        paral_layout = QVBoxLayout()
        transform_layout = QVBoxLayout()

        window_layout.addLayout(settings_layout)
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
        # Tymczasowe
        window_layout.addWidget(self.output_seq_label)
        window_layout.addWidget(self.output_seq_field)
        window_layout.addWidget(self.output_paral_label)
        window_layout.addWidget(self.output_paral_field)
        window_layout.addWidget(self.output_transform_label)
        window_layout.addWidget(self.output_transform_field)

        self.setLayout(window_layout)

    def show_seq(self):
        a = self.seq_field1.text()
        b = self.seq_field2.text()
        if a and b:
            seq = f"{a} ; {b}"
        else:
            seq = "Wprowadź unitermy i spróbuj ponownie."
        self.output_seq_field.setText(seq)

    def show_paral(self):
        a = self.paral_field1.text().strip()
        b = self.paral_field2.text().strip()
        if a and b:
            paral = f"{a} , {b}"
        else:
            paral = "Wprowadź unitermy i spróbuj ponownie."
        self.output_paral_field.setText(paral)

    def show_transform(self):
        seq = self.output_seq_field.toPlainText()
        paral = self.output_paral_field.toPlainText()

        if not seq or not paral or ';' not in seq or ',' not in paral:
            self.output_transform_field.setText("Dodaj operacje i spróbuj ponownie.")
            return
        
        seq_parts = [s.strip() for s in seq.split(';')]
        paral_wrapped = f"( {paral} )"

        if self.radiobutton1.isChecked():
            if len(seq_parts) >= 1:
                seq_parts[0] = paral_wrapped
        elif self.radiobutton2.isChecked():
            if len(seq_parts) >= 2:
                seq_parts[1] = paral_wrapped
        
        transformed = ' ; '.join(seq_parts)
        self.output_transform_field.setText(transformed)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UnitermApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())