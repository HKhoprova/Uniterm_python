import sys
import re
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,  QLabel, QLineEdit, QPushButton, QApplication, QMessageBox,
    QRadioButton, QButtonGroup, QVBoxLayout, QHBoxLayout, QFileDialog
)

from canvas import UnitermCanvas
from database import save_entry, get_all_entries
from dialogs import SaveDialog, LoadDialog

class UnitermApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Uniterm Transformer")
        self.canvas = UnitermCanvas()
        self.canvas.setMinimumHeight(400)
        self.saved_seq = None
        self.saved_paral = None
        self.saved_transformed = None

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

        # Przyciski pod canvasem
        self.save_to_db_button = QPushButton("Zapisz do bazy")
        self.save_to_db_button.clicked.connect(self.save_to_db)
        self.save_to_db_button.setEnabled(False)
        self.save_to_db_button.setToolTip("Wykonaj zamianę, aby aktywować zapis.")
        self.read_from_db_button = QPushButton("Odczytaj z bazy")
        self.read_from_db_button.clicked.connect(self.read_from_db)
        self.save_as_png_button = QPushButton("Zapisz obraz")
        self.save_as_png_button.clicked.connect(self.save_as_png)
        self.save_as_png_button.setEnabled(False)
        self.save_as_png_button.setToolTip("Wykonaj zamianę, aby zapisać obraz.")

        # Widok okna
        window_layout = QVBoxLayout()
        settings_layout = QHBoxLayout()
        seq_layout = QVBoxLayout()
        paral_layout = QVBoxLayout()
        transform_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()

        window_layout.addLayout(settings_layout)
        window_layout.addWidget(self.canvas)
        window_layout.addLayout(buttons_layout)

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

        buttons_layout.addWidget(self.save_to_db_button)
        buttons_layout.addWidget(self.read_from_db_button)
        buttons_layout.addWidget(self.save_as_png_button)

        self.setLayout(window_layout)

    def show_seq(self):
        a = self.seq_field1.text()
        b = self.seq_field2.text()
        if not self.is_valid_uniterm(a) or not self.is_valid_uniterm(b):
            self.handle_error("Uniterm nie może zawierać znaków ; ani , oraz nie może być pusty.")
            return
        self.saved_seq = (a, b)
        self.canvas.draw_seq(a, b)
        self.save_to_db_button.setEnabled(False)
        self.save_as_png_button.setEnabled(False)

    def show_paral(self):
        a = self.paral_field1.text().strip()
        b = self.paral_field2.text().strip()
        if not self.is_valid_uniterm(a) or not self.is_valid_uniterm(b):
            self.handle_error("Uniterm nie może zawierać znaków ; ani , oraz nie może być pusty.")
            return
        self.saved_paral = (a, b)
        self.canvas.draw_paral(a, b)
        self.save_to_db_button.setEnabled(False)
        self.save_as_png_button.setEnabled(False)

    def show_transform(self):
        if not self.saved_seq:
            self.handle_error("Najpierw dodaj operację sekwencjonowania.")
            return
        if not self.saved_paral:
            self.handle_error("Najpierw dodaj operację zrównoleglenia.")
            return

        sa, sb = self.saved_seq
        pa, pb = self.saved_paral
        replace_first = self.radiobutton1.isChecked()
        self.saved_transformed = (sa, sb, pa, pb, replace_first)
        self.canvas.draw_transformed(sa, sb, pa, pb, replace_first)
        self.save_to_db_button.setEnabled(True)
        self.save_as_png_button.setEnabled(True)

    def save_to_db(self):
        if not self.canvas.transformed:
            self.handle_error("Najpierw wykonaj zamianę unitermów.")
            return
        
        dialog = SaveDialog(self)

        existing_titles = [e["title"] for e in get_all_entries()]
        i = 1
        while f"Untitled{i}" in existing_titles:
            i += 1
        dialog.title_field.setText(f"Untitled{i}")

        if dialog.exec_():
            title, author = dialog.get_values()
            if not title:
                self.handle_error("Tytuł jest wymagany.")
                return
            
            sa, sb, pa, pb, replace_first = self.saved_transformed
            save_entry(title, author, sa, sb, pa, pb, replace_first)
            self.saved_title = title
            QMessageBox.information(self, "Sukces", "Zapisano do bazy.")

    def read_from_db(self):
        dialog = LoadDialog(self)
        if dialog.exec_():
            entry = dialog.get_selected()
            if not entry:
                return
            sa, sb, pa, pb, replace_first = entry["sa"], entry["sb"], entry["pa"], entry["pb"], entry["replace_first"]
            self.saved_transformed = (sa, sb, pa, pb, replace_first)
            self.canvas.draw_transformed(sa, sb, pa, pb, replace_first)
            self.save_to_db_button.setEnabled(True)
            self.save_as_png_button.setEnabled(True)
            self.saved_title = entry["title"]

    def save_as_png(self):
        if not self.canvas.transformed:
            self.handle_error("Najpierw wykonaj zamianę unitermów.")
            return
        
        default_name = "Untitled"
        if hasattr(self, "saved_title") and self.saved_title:
            default_name = self.saved_title

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz obraz jako PNG",
            f"{default_name}.png",
            "PNG Files (*.png)"
        )

        if not path:
            return
        
        pixmap = QPixmap(self.canvas.size())
        self.canvas.render(pixmap)
        if not pixmap.save(path):
            self.handle_error("Nie udało się zapisać obrazu.")
        else:
            QMessageBox.information(self, "Sukces", f"Obraz zapisany jako:\n{path}")

    def is_valid_uniterm(self, s):
        return bool(s.strip()) and not re.search(r"[;,]", s)

    def handle_error(self, message):
        QMessageBox.warning(self, "Błąd", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UnitermApp()
    window.resize(800, 500)
    window.show()
    sys.exit(app.exec_())