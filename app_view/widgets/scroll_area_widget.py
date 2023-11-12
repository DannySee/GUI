from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtCore import Qt


class ScrollWidget(QScrollArea):
    def __init__(self, style_sheet, layout=None, minimum_height=100, maximum_height=None, 
                 widget=None, scroll_policy=Qt.ScrollBarPolicy.ScrollBarAlwaysOff, 
                 minimum_width=100, visible=True):
        
        super().__init__()
        self.setWidgetResizable(True)
        self.setStyleSheet(style_sheet)
        self.setMinimumHeight(minimum_height)
        self.setHorizontalScrollBarPolicy(scroll_policy)
        self.setVerticalScrollBarPolicy(scroll_policy)
        self.setMinimumWidth(minimum_width)
        self.setVisible(visible)

        if layout is not None: self.setLayout(layout)
        if widget is not None: self.setWidget(widget)
        if maximum_height is not None: self.setMaximumHeight(maximum_height)
        