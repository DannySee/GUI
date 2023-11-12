from PyQt6.QtWidgets import QLabel


class LabelWidget(QLabel):
    def __init__(self, style_sheet, text="", visible=True):
        super().__init__()
        self.setText(text)
        self.setStyleSheet(style_sheet)
        self.setVisible(visible)
    