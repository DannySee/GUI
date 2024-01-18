from PyQt6.QtWidgets import QLineEdit


class LineEditWidget(QLineEdit):
    def __init__(self, style_sheet, placeholder="", text="", echo_mode=QLineEdit.EchoMode.Normal):
        super().__init__()
        self.setStyleSheet(style_sheet)
        self.setPlaceholderText(placeholder)
        self.setText(text)
        self.setEchoMode(echo_mode)
    