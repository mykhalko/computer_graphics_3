import json
from contextlib import contextmanager

from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QPushButton
)
from PyQt5.QtGui import (
    QPixmap,
    QColor,
    QPainter,
)
from PyQt5.QtCore import Qt

from legacy_tools import with_neighbour
from bezier import BezierCalculator


class GenericCanvas(QLabel):
    _default_size = 700
    _default_virtual_size = 10
    _default_pen_width = 1

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._calc = kwargs.get("calc")
        self._size = kwargs.get("size", self._default_size)
        self._virtual_size = kwargs.get("virtual_size", self._default_virtual_size)
        self._default_pen_width = kwargs.get("default_pen_width", self._default_pen_width)
        self._init_ui()
        self.clicks = []

    def _init_ui(self):
        pixmap = QPixmap(self._size, self._size)
        self.setPixmap(pixmap)
        self.clear()
        self._default_pen_color = QColor('#ff0000')
        # self.paint_cartesian()
        self.show()

    @contextmanager
    def painting(self, width=None, color=None):
        painter = QPainter(self.pixmap())
        pen = painter.pen()
        pen.setWidth(width or self._default_pen_width)
        pen.setColor(color or self._default_pen_color)
        painter.setPen(pen)
        yield painter
        painter.end()
        self.update()

    def paint_cartesian(self):
        safe_size = self._size - 1
        virtual_cell_size = round(safe_size / self._virtual_size / 2)
        splitters = tuple(range(0, safe_size, virtual_cell_size))
        splitters_count = len(splitters)
        for i, splitter in enumerate(splitters):
            if i == splitters_count // 2:
                color = QColor(0, 0, 0, 255)
            else:
                color = QColor(0, 0, 0, 25)
            with self.painting(color=color) as painter:
                painter.drawLine(splitter, 0, splitter, safe_size)
                painter.drawLine(0, splitter, safe_size, splitter)

    def clear(self):
        self.pixmap().fill(Qt.white)

    def draw_outline(self, points):
        with self.painting(color=QColor(255, 0, 0, 255)) as painter:
            for start, end in with_neighbour(points, last_with_first=False):
                painter.drawLine(start[0], start[1], end[0], end[1])
                print(f"drawing line for {(start[0], start[1], end[0], end[1])}")

    def mousePressEvent(self, event):
        if event.buttons() == Qt.RightButton:
            self.clicks = []
        dots_limit = self._calc.power
        if len(self.clicks) == dots_limit:
            outline_dots = self._calc.get_dots(self.clicks)
            self.draw_outline(outline_dots)
            self.clicks = []
        else:
            dot = event.pos().x(), event.pos().y()
            if self.clicks:
                last_dot = self.clicks[-1]
                self.draw_outline([(last_dot[0], last_dot[1]), (dot[0], dot[1])])
            print(dot)
            self.clicks.append(dot)

    def redraw(self):
        pass
# class MainWindow(QMainWindow):
#     def __init__(self, *args, **kwargs):
#         def f(*args):
#             this = self
#             print()
#         super().__init__()
#         self._model = kwargs.get("model")
#         self._canvas = GenericCanvas(*args, **kwargs)
#         self._init_ui()
#
#     def _init_ui(self):
#         widget = QWidget()
#         layout = QHBoxLayout()
#         widget.setLayout(layout)
#         layout.addWidget(self._canvas)
#         layout.addWidget(self._control_panel)
#         self.setCentralWidget(widget)
#
#     def redraw(self, data):
#         with self._model.transformation(data):
#             self._canvas.clear()
#             self._canvas.paint_cartesian()
#             for outline in self._model.outlines:
#                 self._canvas.draw_outline(outline)


@contextmanager
def App(*args, **kwargs):
    app = QApplication(*args, **kwargs)
    yield app
    app.exec_()
