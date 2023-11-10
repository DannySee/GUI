from PyQt6.QtWidgets import QComboBox 
from PyQt6.QtCore import QSize


class ComboBoxWidget(QComboBox):
    def __init__(self, style_sheet, placeholder):
        super().__init__()
        self.setStyleSheet(style_sheet)
        self.setPlaceholderText(placeholder)
