from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt

class UnitermCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.seq = None
        self.paral = None
        self.transformed = None

    def draw_seq(self, a, b):
        self.seq = (a, b)
        self.transformed = None
        self.update()

    def draw_paral(self, a, b):
        self.paral = (a, b)
        self.transformed = None
        self.update()

    def draw_transformed(self, seq_a, seq_b, paral_a, paral_b, replace_first):
        self.transformed = (seq_a, seq_b, paral_a, paral_b, replace_first)
        self.seq = None
        self.paral = None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(QFont("Arial", 16))
        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        margin_x = 20
        y = 50

        if self.transformed:
            sa, sb, pa, pb, replace_first = self.transformed

            if replace_first:
                expr = f"{pa} , {pb} ; {sb}"
                paral_part = f"{pa} , {pb}"
            else:
                expr = f"{sa} ; {pa} , {pb}"
                paral_part = f"{pa} , {pb}"

            # Draw full expression
            painter.drawText(margin_x, y, expr)

            # Measure full and partial text widths
            full_width = painter.fontMetrics().width(expr)
            paral_width = painter.fontMetrics().width(paral_part)

            # Offset for [ around parallel part
            if replace_first:
                paral_x = margin_x
            else:
                offset = painter.fontMetrics().width(f"{sa} ; ")
                paral_x = margin_x + offset

            # Draw [ roof
            painter.drawLine(paral_x - 5, y - 25, paral_x + paral_width + 10, y - 25)
            painter.drawLine(paral_x - 5, y - 25, paral_x - 5, y - 15)
            painter.drawLine(paral_x + paral_width + 10, y - 25, paral_x + paral_width + 10, y - 15)

            # Draw ( arc roof for whole expression
            painter.drawArc(margin_x - 10, y - 40, full_width + 20, 30, 0 * 16, 180 * 16)

        else:
            if self.seq:
                a, b = self.seq
                expr = f"{a} ; {b}"
                width = painter.fontMetrics().width(expr)
                painter.drawText(margin_x, y, expr)
                painter.drawArc(margin_x - 10, y - 40, width + 20, 30, 0 * 16, 180 * 16)
                margin_x += 300

            if self.paral:
                a, b = self.paral
                expr = f"{a} , {b}"
                width = painter.fontMetrics().width(expr)
                painter.drawText(margin_x, y, expr)
                painter.drawLine(margin_x - 5, y - 25, margin_x + width + 10, y - 25)
                painter.drawLine(margin_x - 5, y - 25, margin_x - 5, y - 15)
                painter.drawLine(margin_x + width + 10, y - 25, margin_x + width + 10, y - 15)