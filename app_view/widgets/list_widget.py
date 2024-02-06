from PyQt6.QtWidgets import QListView
from app_view.style_sheets import scroll_bar_style
from PyQt6.QtCore import Qt


class ListWidget(QListView):
    def __init__(self, style_sheet, options, fixed_height=None, fixed_width=None, parent=None):  
        super().__init__(parent)

        self.setStyleSheet(style_sheet)
        self.setModel(options)
        self.verticalScrollBar().setStyleSheet(scroll_bar_style.list_vertical)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        if fixed_height is not None: self.setFixedHeight(fixed_height)
        if fixed_width is not None: self.setFixedWidth(fixed_width)
