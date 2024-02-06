from PyQt6.QtWidgets import QLabel
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt


class LabelWidget(QLabel):
    def __init__(self, style_sheet, text="", visible=True, fixed_width=None, fixed_height=None, parent=None):
        super().__init__(parent)
        
        self.setText(text)
        self.setStyleSheet(style_sheet)
        self.setVisible(visible)

        if fixed_width is not None: self.setFixedWidth(fixed_width)
        if fixed_height is not None: self.setFixedHeight(fixed_height)
