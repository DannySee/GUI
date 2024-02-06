from app_view.widgets.button_widget import ButtonWidget
from app_view.widgets.layout_widget import HorizontalBox
from app_view.widgets.label_widget import LabelWidget
from app_view.widgets.frame_widget import FrameWidget
from app_view.style_sheets import button_style, label_style, frame_style, universal_style
from PyQt6.QtWidgets import QFrame, QApplication
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon


class TitleBarWidget(QFrame):
    def __init__(self):

        super().__init__()

        fixed_height = 35
        
        self.snap_right = False 
        self.snap_left = False
        self.snap_top = False
        self.snap = False

        self.setFixedHeight(fixed_height)

        self.layout = HorizontalBox()
        self.setStyleSheet(frame_style.titlebar)

        self.content_layout = HorizontalBox(content_margins=[10,5,10,5], spacing=10)
        self.layout.addLayout(self.content_layout)

        self.icon = ButtonWidget(button_style.titlebar_icon, icon=QIcon("icon.svg"), parent=self)
        self.content_layout.addWidget(self.icon)

        self.content_layout.addStretch()

        self.title = LabelWidget(label_style.titlebar, "Commercial Services Hive", parent=self)
        self.content_layout.addWidget(self.title)

        self.content_layout.addStretch()

        self.minimizeBtn = ButtonWidget(button_style.titlebar_generic, icon=QIcon("app_view/icons/window-minimize.svg"), fixed_height=fixed_height, fixed_width=fixed_height+5, parent=self)
        self.layout.addWidget(self.minimizeBtn)

        self.maximizeBtn = ButtonWidget(button_style.titlebar_generic, icon=QIcon("app_view/icons/window-maximize.svg"), fixed_height=fixed_height, fixed_width=fixed_height+5, parent=self)
        self.layout.addWidget(self.maximizeBtn)

        self.closeBtn = ButtonWidget(button_style.titlebar_close, icon=QIcon("app_view/icons/window-close.svg"), fixed_height=fixed_height, fixed_width=fixed_height+5, parent=self)
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

            self.screen_geo = QApplication.primaryScreen().availableGeometry()

            # snap back to default move position (centered on cursor)
            if self.snap:
                self.parent().setGeometry(self.parent().pos().x() + event.position().toPoint().x() - int(self.app_geo.width()/2), 
                                          self._drag_pos.y() - int(self.height() / 2), self.app_geo.width(), self.app_geo.height()) 
                self._drag_pos = QPoint(QPoint().x() + int(self.app_geo.width()/2), QPoint().y()+int(self.height() / 2))
                self.snap = False

            # move window
            else:
                self.parent().move(self.parent().pos() + event.position().toPoint() - self._drag_pos)
                
            # left
            if self.parent().pos().x() + self._drag_pos.x() == self.screen_geo.left():
                self.snap_left = True

            # right
            elif self.parent().pos().x() + self._drag_pos.x() == self.screen_geo.right():
                self.snap_right = True

            # top
            elif self.parent().pos().y() + self._drag_pos.y() == self.screen_geo.top():
                self.snap_top = True

            else:
                self.snap_left = False
                self.snap_right = False
                self.snap_top = False

            event.accept()


    def mouseReleaseEvent(self, event):
        self._drag_pos = QPoint()
        self.app_geo = self.parent().geometry()

        # left
        if self.snap_left:
            self.parent().setGeometry(self.screen_geo.left(), self.screen_geo.top(),
                             int(self.screen_geo.width() / 2), self.screen_geo.height())
            self.snap = True

        # right
        elif self.snap_right:
            self.parent().setGeometry(int(self.screen_geo.width() / 2), self.screen_geo.top(),
                             int(self.screen_geo.width() / 2), self.screen_geo.height())
            self.snap = True

        # top 
        elif self.snap_top:
            self.parent().showMaximized()
            self.snap = True
            
        event.accept()

  