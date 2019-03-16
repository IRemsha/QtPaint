import random

from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QImage, QPainter, QPen, QColor, QPixmap, QBrush, QTransform
from PyQt5.QtWidgets import QWidget, QLabel, QColorDialog

CANVAS_DIMENSIONS = 600, 450


class Canvas(QLabel):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.drawing = False
        self.canvas_conf_brush = 3.14
        self.canvas_conf_spray = 5

        self.mode = 'Pen'

        self.primary_color = QColor(Qt.black)
        self.secondary_color = QColor(Qt.white)

        self.brush_size = 2
        self.brush_color = self.primary_color
        self.last_point = QPoint()

    def initialize(self):
        self.background_color = QColor(self.secondary_color) if self.secondary_color else QColor(Qt.white)
        self.eraser_color = QColor(self.secondary_color) if self.secondary_color else QColor(Qt.white)
        self.eraser_color.setAlpha(100)
        self.reset()

    def reset(self):
        self.setPixmap(QPixmap(*CANVAS_DIMENSIONS))
        self.pixmap().fill(self.background_color)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            if self.mode == 'Pen':
                self.mouseMoveEventPen(event)
            elif self.mode == 'Brush':
                self.mouseMoveEventBrush(event)
            elif self.mode == 'Spray':
                self.mouseMoveEventSpray(event)
            elif self.mode == 'Pencil':
                self.mouseMoveEventPencil(event)
            elif self.mode == 'Rect':
                self.mouseMoveEventRect(event)
            elif self.mode == 'Marker':
                self.mouseMoveEventMarker(event)

    def mouseMoveEventPen(self, event):
        qt_pointer = QPainter(self.pixmap())
        qt_pointer.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        qt_pointer.drawLine(self.last_point, event.pos())
        self.last_point = event.pos()
        self.update()

    def mouseMoveEventPencil(self, event):
        qt_pointer = QPainter(self.pixmap())
        qt_pointer.setPen(QPen(self.brush_color, self.brush_size/10, Qt.SolidLine, Qt.FlatCap, Qt.BevelJoin))
        qt_pointer.drawLine(self.last_point, event.pos())
        self.last_point = event.pos()
        self.update()

    def mouseMoveEventBrush(self, event):
        qt_pointer = QPainter(self.pixmap())
        qt_pointer.setPen(QPen(self.brush_color, self.brush_size*self.canvas_conf_brush,
                               Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        qt_pointer.drawLine(self.last_point, event.pos())
        self.last_point = event.pos()
        self.update()

    def mouseMoveEventMarker(self, event):
        qt_pointer = QPainter(self.pixmap())
        qt_pointer.setPen(QPen(self.brush_color, self.brush_size,
                               Qt.DashLine, Qt.RoundCap, Qt.RoundJoin))
        qt_pointer.setBrush(QBrush(Qt.TexturePattern))
        qt_pointer.drawLine(self.last_point, event.pos())
        self.last_point = event.pos()
        self.update()

    def mouseMoveEventSpray(self, event):
        qt_pointer = QPainter(self.pixmap())
        qt_pointer.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for n in range(100):
            xo = random.gauss(0, self.brush_size * self.canvas_conf_spray)
            yo = random.gauss(0, self.brush_size * self.canvas_conf_spray)
            qt_pointer.drawPoint(event.x() + xo, event.y() + yo)
        self.update()

    def mouseMoveEventRect(self, event):
        qt_pointer = QPainter(self.pixmap())
        qt_pointer.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin))
        qt_pointer.drawRect(self.last_point.x(), self.last_point.y(), event.pos().x(),  event.pos().y())
        self.last_point = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def choose_color(self):
        choose_color = QColorDialog.getColor()
        self.primary_color = choose_color
        self.update_brush()

    def change_value_brush(self, value):
        self.brush_size = value / 10

    def update_brush(self):
        self.brush_color = self.primary_color

    def clear(self):
        self.pixmap().fill(self.background_color)
        self.update()

    def next(self):
        pass

    def back(self):
        pass

    def flip_horizontal(self):
        pixmap = self.pixmap()
        self.setPixmap(pixmap.transformed(QTransform().scale(-1, 1)))

    def flip_vertical(self):
        pixmap = self.pixmap()
        self.setPixmap(pixmap.transformed(QTransform().scale(1, -1)))

    def scaled_canvas(self, value):
        set_size = value*7
        if set_size >= 100:
            pixmap = self.pixmap()
            self.setPixmap(pixmap.scaled(set_size, set_size, Qt.IgnoreAspectRatio))


