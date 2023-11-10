from PyQt6.QtWidgets import QSplitter


class SplitterWidget(QSplitter):
    def __init__(self, orientation, style_sheet, collapsible, width=0):
        super().__init__()
        self.setOrientation(orientation)
        self.setChildrenCollapsible(collapsible)
        self.setStyleSheet(style_sheet)
        self.setHandleWidth(width)

