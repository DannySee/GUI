from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QPoint

class TitleBarWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel("My Application")
        self.minimizeBtn = QPushButton("-")
        self.maximizeBtn = QPushButton("□")
        self.closeBtn = QPushButton("X")

        self.layout.addWidget(self.title)
        self.layout.addStretch()
        self.layout.addWidget(self.minimizeBtn)
        self.layout.addWidget(self.maximizeBtn)
        self.layout.addWidget(self.closeBtn)
        self.setLayout(self.layout)

        # Styling
        self.setStyleSheet("""
            QFrame {
                background-color: #181818;
                color: white;
            }
            QPushButton {
                border: none;
                background-color: #181818;
                color: white;
            }
            QPushButton:hover {
                background-color: red;
            }
        """)

        self.minimizeBtn.clicked.connect(self.on_minimize)
        self.maximizeBtn.clicked.connect(self.on_maximize)
        self.closeBtn.clicked.connect(self.on_close)

        self._drag_pos = QPoint()

    def on_minimize(self):
        self.parent().showMinimized()

    def on_maximize(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
        else:
            self.parent().showMaximized()

    def on_close(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.position().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos is not None:
            self.parent().move(self.parent().pos() + event.position().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = QPoint()
        event.accept()