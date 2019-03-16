from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QPushButton


class QPushColorButton (QPushButton):
    """
    Класс расширение для QPushButton
    Нужен для того, чтобы в генераторе кнопок не париться с назначением на них методов.
    """
    def __init__(self, HTML, canvas):
        super().__init__()
        self.HTML_color = HTML
        self.canvas = canvas

    def setColorMethod(self):
        self.canvas.primary_color = QColor(self.HTML_color)
        self.canvas.update_brush()
