from app_view.widgets.button_widget import ButtonWidget
from app_view.widgets.layout_widget import HorizontalBox
from app_view.widgets.label_widget import LabelWidget
from app_view.style_sheets import button_style, label_style, frame_style, universal_style
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon

class TitleBarWidget(QFrame):
    def __init__(self):

        super().__init__()

        self.layout = HorizontalBox()
        self.setStyleSheet(frame_style.titlebar)

        self.icon = ButtonWidget(universal_style.hidden, icon=QIcon("icon.svg"), parent=self)
        self.title = LabelWidget(label_style.titlebar, "Hive", parent=self)
        self.minimizeBtn = ButtonWidget(button_style.titlebar_generic, icon=QIcon("app_view/icons/window-minimize.svg"), parent=self)
        self.maximizeBtn = ButtonWidget(button_style.titlebar_generic, icon=QIcon("app_view/icons/window-maximize.svg"), parent=self)
        self.closeBtn = ButtonWidget(button_style.titlebar_close, icon=QIcon("app_view/icons/window-close.svg"), parent=self)

        self.layout.addWidget(self.icon)
        self.layout.addStretch()
        self.layout.addWidget(self.title)
        self.layout.addStretch()
        self.layout.addWidget(self.minimizeBtn)
        self.layout.addWidget(self.maximizeBtn)
        self.layout.addWidget(self.closeBtn)
        self.setLayout(self.layout)

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