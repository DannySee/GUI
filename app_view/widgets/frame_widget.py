from PyQt6.QtWidgets import QFrame, QSizePolicy


class FrameWidget(QFrame):
    def __init__(self, style_sheet, layout=None, minimum_width=100, maximum_width=None, fixed_height=None, fixed_width=None, 
                 maximum_height=None, vertical_size_policy=QSizePolicy.Policy.Expanding, 
                 horizontal_size_policy=QSizePolicy.Policy.Expanding, visible=True, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet(style_sheet)
        self.setMinimumWidth(minimum_width)
        self.setSizePolicy(horizontal_size_policy, vertical_size_policy)
        self.setVisible(visible)
        
        if layout is not None: self.setLayout(layout)
        if maximum_width is not None: self.setMaximumWidth(maximum_width)
        if maximum_height is not None: self.setMaximumHeight(maximum_height)
        if fixed_height is not None: self.setFixedHeight(fixed_height)
        if fixed_width is not None: self.setFixedWidth(fixed_width)
