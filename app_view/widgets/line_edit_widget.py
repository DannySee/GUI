from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt, QTimer


class LineEditWidget(QLineEdit):
    def __init__(self, style_sheet, placeholder="", text="", echo_mode=QLineEdit.EchoMode.Normal, parent=None, debounce_event=None):
        super().__init__(parent)
        
        self.setStyleSheet(style_sheet)
        self.setPlaceholderText(placeholder)
        self.setText(text)
        self.setEchoMode(echo_mode)


        if debounce_event is not None:
            self.debounce_event = debounce_event
            self.debounceTimer = QTimer(self)
            self.debounceTimer.setSingleShot(True)
            self.debounceTimer.timeout.connect(self.onTextChangedDebounced)
            self.textChanged.connect(self.startDebounceTimer)


    def startDebounceTimer(self):
        # Restart the timer every time text is changed
        # Set the interval to 500ms or whatever suits your need
        self.debounceTimer.start(500)

    def onTextChangedDebounced(self):
        # This function will be called when the user stops typing for 500ms
        self.debounce_event(self.placeholderText(), self.text())









