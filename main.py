#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import Qt, pyqtSignal, QRect, QPoint, QMargins
from PyQt5.QtGui import QImage, QColor, QPixmap, QTransform, QIcon
from PyQt5.QtWidgets import (QWidget, QGridLayout, QApplication, QPushButton,
                             QDesktopWidget, QSizePolicy, QColorDialog, QComboBox, QButtonGroup, QFileDialog,
                             QMainWindow, QSlider, QFrame, QVBoxLayout, QHBoxLayout)

from QPushColorButton import QPushColorButton
from QPushToolsBrushButton import QPushToolsBrushButton
from сanvas import Canvas, CANVAS_DIMENSIONS

TOOLS = [
    'Pen', 'Brush', 'Spray', 'Rect', 'Pencil', 'Marker'
]
COLORS = [
    '#000000', '#82817f', '#820300', '#868417', '#007e03', '#037e7b', '#040079',
    '#81067a', '#7f7e45', '#05403c', '#0a7cf6', '#093c7e', '#7e07f9', '#7c4002',

    '#ffffff', '#c1c1c1', '#f70406', '#fffd00', '#08fb01', '#0bf8ee', '#0000fa',
    '#b92fc2', '#fffc91', '#00fd83', '#87f9f9', '#8481c4', '#dc137d', '#fb803c',
]


class GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.canvas = Canvas(self)
        self.canvas.initialize()
        "Создаём Grid Layout 15х3(Y:X)"
        self.grid = QGridLayout()
        self.setupUI()
        self.init_screen()

    def init_screen(self):
        self.setWindowTitle('QPaint')
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.center_screen()

    def setupUI (self):
        self.init_layouts()
        self.show()

    def init_layouts(self):

        open_button = QPushButton("Open")
        open_button.pressed.connect(self.open_file)

        save_button = QPushButton("Save")
        save_button.pressed.connect(self.save_file)

        clear_button = QPushButton("Clear")
        clear_button.pressed.connect(self.canvas.clear)

        load_img_button = QPushButton("Load IMG")
        push_img_button = QPushButton("Push IMG")

        grid_button_flip = QGridLayout()

        button_flip_h = QPushButton()
        button_flip_h.setIcon(QIcon("icon\Flip_h"))
        button_flip_h.pressed.connect(self.canvas.flip_horizontal)
        grid_button_flip.addWidget(button_flip_h, 0, 0)

        button_flip_v = QPushButton()
        button_flip_v.setIcon(QIcon("icon\Flip_v"))
        grid_button_flip.addWidget(button_flip_v, 0, 1)
        button_flip_v.pressed.connect(self.canvas.flip_vertical)

        choose_color_button = QPushButton("Choose Color")
        choose_color_button.setIcon(QIcon("icon\Palette"))
        choose_color_button.pressed.connect(self.canvas.choose_color)

        grid_tools = QGridLayout()

        slider_brush_size = QSlider(Qt.Horizontal, self)
        slider_brush_size.setFixedSize(100, 15)
        slider_brush_size.valueChanged[int].connect(self.canvas.change_value_brush)

        slider_canvas_size = QSlider(Qt.Horizontal, self)
        slider_canvas_size.setFixedSize(100, 15)
        slider_canvas_size.valueChanged[int].connect(self.canvas.scaled_canvas)

        "Генератор кнопок инструментов"
        for n, mode in enumerate(TOOLS, 0):
            tools_mode_button = QPushToolsBrushButton(mode, self.canvas)
            tools_mode_button.setFixedSize(35, 35)
            tools_mode_button.setIcon(QIcon("icon\%s" % mode))
            tools_mode_button.pressed.connect(tools_mode_button.setModeForBrush)
            grid_tools.addWidget(tools_mode_button, n // 6, n % 7)

        grid_color = QGridLayout()

        "Генератор цветных кнопок"
        for n, HTML in enumerate(COLORS, 0):
            button_color = QPushColorButton(HTML, self.canvas)
            button_color.setFixedSize(20, 20)
            button_color.setStyleSheet('QPushButton { background-color: %s; }' % HTML)
            button_color.pressed.connect(button_color.setColorMethod)
            grid_color.addWidget(button_color, n // 14, n % 14)

        grid_menu = QGridLayout()
        grid_button = QGridLayout()

        grid_button.addWidget(open_button, 0, 0, 1, 2)
        grid_button.addWidget(save_button)
        grid_button.addWidget(clear_button)
        grid_button.addWidget(load_img_button)
        grid_button.addWidget(push_img_button)
        grid_button.addWidget(choose_color_button, 7, 0, 1, 2)
        grid_button.addWidget(slider_brush_size, 9, 1)
        grid_button.addItem(grid_color, 8, 0, 1, 2)
        grid_button.addItem(grid_tools, 9, 0)
        grid_button.addItem(grid_button_flip, 10, 0)
        grid_button.addWidget(slider_canvas_size, 10, 1)
        grid_menu.addItem(grid_button)

        grid_canvas = QGridLayout()
        grid_canvas.addWidget(self.canvas)

        self.grid.addItem(grid_menu, 0, 0, 5, 1)
        self.grid.addItem(grid_canvas, 0, 1, 1, 10)

        self.setLayout(self.grid)

    def keyPressEvent(self, event):
        """
        Метод обработки ввода с клав.
        :param event: Параметр сигнала с квал.
        :return: None
        """
        if event.key() == Qt.Key_C:
            self.canvas.clear()
        elif event.key() == Qt.Key_B:
            self.canvas.back()
        elif event.key() == Qt.Key_N:
            self.canvas.get_color()
        elif event.key() == Qt.Key_S:
            self.save_file()
        elif event.key() == Qt.Key_O:
            self.open_file()

    def center_screen(self):
        """
        Метод размещает игровое окно по середине экрана.
        :return: None
        """
        geometry_menu = self.frameGeometry()
        center_menu = QDesktopWidget().availableGeometry().center()
        geometry_menu.moveCenter(center_menu)
        self.move(geometry_menu.topLeft())

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "PNG Image file (*.png)")

        if path:
            pixmap = self.canvas.pixmap()
            pixmap.save(path, "PNG")

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                              "PNG image files (*.png); JPEG image files (*jpg); All files (*.*)")

        if path:
            pixmap = QPixmap()
            pixmap.load(path)

            iw = pixmap.width()
            ih = pixmap.height()
            cw, ch = CANVAS_DIMENSIONS

            if iw / cw < ih / ch:
                pixmap = pixmap.scaledToWidth(cw)
                hoff = (pixmap.height() - ch) // 2
                pixmap = pixmap.copy(
                    QRect(QPoint(0, hoff), QPoint(cw, pixmap.height() - hoff))
                )

            elif iw / cw > ih / ch:
                pixmap = pixmap.scaledToHeight(ch)
                woff = (pixmap.width() - cw) // 2
                pixmap = pixmap.copy(
                    QRect(QPoint(woff, 0), QPoint(pixmap.width() - woff, ch))
                )

            self.canvas.setPixmap(pixmap)

    def flip_horizontal(self):
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap.transformed(QTransform().scale(-1, 1)))

    def flip_vertical(self):
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap.transformed(QTransform().scale(1, -1)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
