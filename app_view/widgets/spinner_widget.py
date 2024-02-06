from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QWidget
import app_view.style_sheets.color_palette as color


class SpinnerWidget(QWidget):
    def __init__(self, parent=None, visible=False):
        super().__init__(parent=parent)  # Added parent argument for better widget hierarchy management
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.setFixedWidth(38)
        self.setFixedHeight(38)
        self.setVisible(False)  # Default to not visible; toggle with start/stopAnimation()

    def rotate(self):
        self.angle = (self.angle + 25) % 360
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(color.background_bright), 5, Qt.PenStyle.SolidLine))
        # Use QRectF for precise control over the drawing rectangle
        rect = self.rect().adjusted(10, 10, -10, -10)  # Adjust if needed
        painter.drawArc(rect, self.angle * 16, 270 * 16)  # 270 * 16 = 3/4 circle

    def start(self):
        self.setVisible(True)
        self.timer.start(40)  # Adjust the interval for speed

    def stop(self):
        self.setVisible(False)
        self.timer.stop()
