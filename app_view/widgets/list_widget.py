from PyQt6.QtWidgets import QListView


class ListWidget(QListView):
    def __init__(self, style_sheet, options, fixed_height=None, fixed_width=None):  
        super().__init__()
        self.setStyleSheet(style_sheet)
        self.setModel(options)

        if fixed_height is not None: self.setFixedHeight(fixed_height)
        if fixed_width is not None: self.setFixedWidth(fixed_width)
    