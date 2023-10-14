import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFrame,
                             QVBoxLayout, QSpacerItem, QSizePolicy, QSplitter,
                             QWidget, QScrollArea, QSplitterHandle)
from PyQt6.QtGui import QFont, QMouseEvent
from PyQt6.QtCore import Qt


class MySplitterHandle(QSplitterHandle):
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        parent_splitter = self.parent()
        sizes = parent_splitter.sizes()

        if sizes[0] > 50:
            sizes[0] = 50
        else:
            sizes[0] = 180

        parent_splitter.setSizes(sizes)


class MySplitter(QSplitter):
    def createHandle(self):
        return MySplitterHandle(self.orientation(), self)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 500, 800, 600)
        self.setWindowTitle("Hive Data Center")
        self.initUI()

    def initUI(self):
        self.setupMainFrame()
        self.setupSplitter()
        self.setupSidebar()
        self.setupDataFrame()
        self.setupScrollArea()
        self.setupSidebarButtons()
        self.setupDividingLine()

        self.setCentralWidget(self.mainFrame)

    def setupMainFrame(self):
        self.mainFrame = QFrame(self)
        self.mainFrame.setStyleSheet("background-color: #181818;")
        self.layout = QVBoxLayout(self.mainFrame)
        self.layout.setContentsMargins(10,10,10,10)

    def setupSplitter(self):
        self.splitter = MySplitter(Qt.Orientation.Horizontal, self.mainFrame)
        self.splitter.setHandleWidth(10)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setStyleSheet("QSplitter::Handler {background-color: transparent; border: none; color: #3c3c3c;}")
        self.layout.addWidget(self.splitter)

    def setupSidebar(self):
        self.sidebar = QFrame(self.splitter)
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar.setMinimumWidth(50)
        self.sidebar.setMaximumWidth(180)
        self.sidebar.setStyleSheet("background-color: #1f1f1f; border: 1px solid #3c3c3c; border-radius: 5px;")
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(0, 0, 0, 0)

    def setupDataFrame(self):
        self.dataFrame = QWidget(self.splitter)
        self.dataFrame.setMinimumWidth(200)
        self.dataFrame.setStyleSheet("background-color: #1f1f1f; border: 1px solid #3c3c3c; border-radius: 5px;")

    def setupScrollArea(self):
        self.scrollArea = QScrollArea(self.sidebar)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("background-color: transparent; border: none;")

        self.scrollWidget = QWidget(self.scrollArea)
        self.scrollWidget.setStyleSheet("background-color: transparent; border: none;")

        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setSpacing(3)

        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.sidebarLayout.addWidget(self.scrollArea)

    def setupSidebarButtons(self):
        teams = [
            "SMS & Costing",
            "Customer Disputes",
            "Customer Incentives",
            "Deviated Agreements",
            "USDA Agreements",
            "Quality Assurance",
            "SMS & Costing",
            "Customer Disputes",
            "Customer Incentives",
            "Deviated Agreements",
            "USDA Agreements",
            "Quality Assurance"
        ]
        
        for team in teams:
            self.createButton(team)

    def createButton(self, text):
        button = QPushButton(text, self.scrollWidget)
        button.setFont(QFont("Microsoft Sans Serif", 11))
        button.setStyleSheet(self.getButtonStyleSheet())
        button.clicked.connect(self.onButtonClicked)
        self.scrollLayout.addWidget(button)

    def setupDividingLine(self):
        dividingLine = QFrame(self.sidebar)
        dividingLine.setFrameShape(QFrame.Shape.HLine)
        dividingLine.setFrameShadow(QFrame.Shadow.Plain)
        dividingLine.setStyleSheet("background-color: #3c3c3c; border: none;")
        self.sidebarLayout.addWidget(dividingLine)
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.sidebarLayout.addSpacerItem(spacer)

    def getButtonStyleSheet(self, active=False):
        baseStyle = """
            QPushButton {{
                text-align: left;
                border: none;
                padding: 10px;
                color: {color};
                background-color: {bg_color};
            }}
            QPushButton:hover {{
                background-color: {hover_bg_color};
                color: #FFFFFF;
            }}
        """

        if active:
            return baseStyle.format(color="#EEEEEE", bg_color="#2F2F2F", hover_bg_color="#3F3F3F")

        return baseStyle.format(color="#BDBDBD", bg_color="transparent", hover_bg_color="#2F2F2F")

    def onButtonClicked(self):
        clickedButton = self.sender()
        
        for button in self.scrollWidget.findChildren(QPushButton):
            if button is clickedButton:
                button.setStyleSheet(self.getButtonStyleSheet(True))
            else:
                button.setStyleSheet(self.getButtonStyleSheet())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
