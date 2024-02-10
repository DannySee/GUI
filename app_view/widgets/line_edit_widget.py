from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFontMetrics


class LineEditWidget(QLineEdit):
    def __init__(self, style_sheet, placeholder="", text="", echo_mode=QLineEdit.EchoMode.Normal, parent=None, debounce_event=None, tooltip=False):
        super().__init__(parent)
        
        self.setStyleSheet(style_sheet)
        self.setPlaceholderText(placeholder)
        self.setText(text)
        self.setEchoMode(echo_mode)
        self.dynamic_tooltip_enabled = tooltip
        self.placeholder_full_text = placeholder

        if debounce_event is not None:
            self.debounce_event = debounce_event
            self.debounceTimer = QTimer(self)
            self.debounceTimer.setSingleShot(True)
            self.debounceTimer.timeout.connect(self.onTextChangedDebounced)
            self.textChanged.connect(self.startDebounceTimer)


    def paintEvent(self, event):
        super().paintEvent(event)
        if self.dynamic_tooltip_enabled and not self.text():
            # Check if placeholder text is cut off
            fm = self.fontMetrics()
            text_width = fm.horizontalAdvance(self.placeholderText())
            if text_width > self.width() - 20:  # Adjust based on your widget's padding
                self.setToolTip(self.placeholder_full_text)
            else:
                self.setToolTip("")  # Disable tooltip if text fits


    def startDebounceTimer(self):
        # Restart the timer every time text is changed
        # Set the interval to 500ms or whatever suits your need
        self.debounceTimer.start(500)

    def onTextChangedDebounced(self):
        # This function will be called when the user stops t
        # yping for 500ms
        self.debounce_event(self.placeholderText(), self.text())









