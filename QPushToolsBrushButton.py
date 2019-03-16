from PyQt5.QtWidgets import QPushButton


class QPushToolsBrushButton (QPushButton):
    """
    Класс расширение для QPushButton
    """
    def __init__(self, tools_mode, canvas):
        super().__init__()
        self.mode = tools_mode
        self.canvas = canvas

    def setModeForBrush(self):
        self.canvas.mode = self.mode
