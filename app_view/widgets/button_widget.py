from PyQt6.QtWidgets import QPushButton, QSpacerItem 
from PyQt6.QtCore import QSize


class ButtonWidget(QPushButton):
    def __init__(self, style_sheet, text=None, icon=None, icon_size=None, visible=True, enabled=True,
                 fixed_height=None, fixed_width=None, layout=None, object_name=None, tool_tip=None, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet(style_sheet)
        self.setVisible(visible)
        self.setEnabled(enabled)

        if text is not None: self.setText(text)
        if icon is not None: self.setIcon(icon)
        if icon_size is not None: self.setIconSize(QSize(*icon_size))
        if fixed_height is not None: self.setFixedHeight(fixed_height)
        if fixed_width is not None: self.setFixedWidth(fixed_width)
        if layout is not None: self.setLayout(layout)
        if object_name is not None: self.setObjectName(object_name)
        if tool_tip is not None: self.setToolTip(tool_tip)

        


