from PyQt6.QtWidgets import QSplitter, QSizePolicy


class SplitterWidget(QSplitter):
    def __init__(self, orientation, style_sheet, collapsible, width=0, size_policy=QSizePolicy.Policy.Expanding):
        super().__init__()
        self.setSizePolicy(size_policy, size_policy)
        self.setOrientation(orientation)
        self.setChildrenCollapsible(collapsible)
        self.setStyleSheet(style_sheet)
        self.setHandleWidth(width)

