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
        painter.fillRect(self.rect(), Qt.white)
        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        margin_x = 20
        y = 50

        if self.transformed:
            sa, sb, pa, pb, replace_first = self.transformed

            if replace_first:
                expr = f"{pa}  ,  {pb}  ;  {sb}"
            else:
                expr = f"{sa}  ;  {pa}  ,  {pb}"

            painter.drawText(margin_x, y, expr)

            full_width = painter.fontMetrics().width(expr)
            paral_width = painter.fontMetrics().width(f"{pa}  ,  {pb}")

            if replace_first:
                paral_x = margin_x
            else:
                offset = painter.fontMetrics().width(f"{sa}  ;  ")
                paral_x = margin_x + offset

            painter.drawLine(paral_x - 5, y - 25, paral_x + paral_width + 5, y - 25)
            painter.drawLine(paral_x - 5, y - 25, paral_x - 5, y - 20)
            painter.drawLine(paral_x + paral_width + 5, y - 25, paral_x + paral_width + 5, y - 20)

            painter.drawArc(margin_x - 10, y - 40, full_width + 20, 20, 0 * 16, 180 * 16)

        else:
            if self.seq:
                a, b = self.seq
                expr = f"{a}  ;  {b}"
                width = painter.fontMetrics().width(expr)
                painter.drawText(margin_x, y, expr)
                painter.drawArc(margin_x - 5, y - 30, width + 10, 20, 0 * 16, 180 * 16)
                margin_x += painter.fontMetrics().width(expr) + 250

            if self.paral:
                a, b = self.paral
                expr = f"{a}  ,  {b}"
                width = painter.fontMetrics().width(expr)
                painter.drawText(margin_x, y, expr)
                painter.drawLine(margin_x - 5, y - 25, margin_x + width + 5, y - 25)
                painter.drawLine(margin_x - 5, y - 25, margin_x - 5, y - 20)
                painter.drawLine(margin_x + width + 5, y - 25, margin_x + width + 5, y - 20)