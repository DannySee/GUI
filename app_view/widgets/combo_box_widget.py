from PyQt6.QtWidgets import QComboBox 
from PyQt6.QtCore import QSize


class ComboBoxWidget(QComboBox):
    def __init__(self, style_sheet, placeholder, parent=None):

        super().__init__(parent)
        self.setStyleSheet(style_sheet)
        self.setPlaceholderText(placeholder)
