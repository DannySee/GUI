import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFrame,
                             QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QSplitter,
                             QWidget, QScrollArea, QSplitterHandle, QLabel, QTableWidget)
from PyQt6.QtGui import QFont, QMouseEvent, QIcon
from PyQt6.QtCore import Qt


class MySplitterHandle(QSplitterHandle):
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        parent_splitter = self.parent()
        sizes = parent_splitter.sizes()

        if sizes[0] > 50:
            sizes[0] = 50
        else:
            sizes[0] = 150

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
        self.setupSidebarCollapse()
        self.setupDataFrame()
        self.setupTableView()
        self.setupsidebarSplitter()
        self.setupScrollArea()
        self.setupFilters()
        self.setupSidebarButtons()

        self.sidebar.setMinimumWidth(self.scrollWidget.sizeHint().width())
        self.sidebar.setMaximumWidth(self.scrollWidget.sizeHint().width()+100)

        # Assuming self.scrollWidget is the child widget of the QScrollArea
        self.scrollArea.setMaximumHeight(self.scrollWidget.sizeHint().height())

        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([self.sidebar.minimumWidth(), self.mainFrame.width()])

        self.setCentralWidget(self.mainFrame)

    def collapseSidebar(self):  
        if self.splitter.sizes()[0] > 50:
            self.sidebar.setMaximumWidth(50)
            self.sidebar.setMinimumWidth(50)
            self.splitter.setSizes([50, self.mainFrame.width()])
            self.sidebarCollapse.setIcon(QIcon("icons/chevron-right.svg"))           
        
            for button in self.scrollWidget.findChildren(QPushButton):
                button.setToolTip(self.teams[button.objectName()]["text"])
                button.setIcon(self.teams[button.objectName()]["icon"])
                button.setText("")
                button.adjustSize()
                button.setStyleSheet(self.getButtonStyleSheet("icon"))
            
            self.scrollLayout.setContentsMargins(0,0,0,0)
            self.scrollLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        else:
            self.sidebarCollapse.setIcon(QIcon("icons/chevron-left.svg"))

            for button in self.scrollWidget.findChildren(QPushButton):
                button.setToolTip("")
                button.setIcon(QIcon())
                button.setText(self.teams[button.objectName()]["text"])
                button.adjustSize()
                button.setStyleSheet(self.getButtonStyleSheet("text"))

            self.scrollLayout.setContentsMargins(10,10,10,10)
            self.scrollLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            self.sidebar.setMinimumWidth(self.scrollWidget.sizeHint().width())
            self.sidebar.setMaximumWidth(self.scrollWidget.sizeHint().width()+100)
            self.splitter.setSizes([self.sidebar.minimumWidth(), self.mainFrame.width()])


    def setupTableView(self):
        
        pass


    def setupSidebarCollapse(self):

        collapsePanel = QFrame(self.sidebar)
        collapsePanel.setStyleSheet("background-color: transparent; border: none;")
        collapsePanel.setFixedHeight(35)
        self.sidebarLayout.addWidget(collapsePanel)

        collapseLayout = QHBoxLayout(collapsePanel)
        collapseLayout.setContentsMargins(5,5,5,5)
        collapseLayout.addSpacerItem(QSpacerItem(25,25, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        icon = QIcon("icons/chevron-left.svg")
        self.sidebarCollapse = QPushButton(collapsePanel)
        self.sidebarCollapse.setIcon(icon)
        self.sidebarCollapse.setFixedWidth(25)
        self.sidebarCollapse.setStyleSheet("""
            QPushButton {
                color: #EEEEEE;
                background-color: transparent;
                padding: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
                border-radius: 4px;                           
                color: #FFFFFF;
            }
        """)
        self.sidebarCollapse.clicked.connect(self.collapseSidebar)
        collapseLayout.addWidget(self.sidebarCollapse)

        

    def setupMainFrame(self):
        self.mainFrame = QFrame(self)
        self.mainFrame.setStyleSheet("background-color: #181818;")
        self.layout = QVBoxLayout(self.mainFrame)
        self.layout.setContentsMargins(0,0,0,0)

    def setupSplitter(self):
        self.splitter = MySplitter(Qt.Orientation.Horizontal, self.mainFrame)
        self.splitter.setHandleWidth(1)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setStyleSheet("QSplitter::handle {background-color: transparent; border: none; color: #3c3c3c;}")
        
        self.layout.addWidget(self.splitter)

    def setupsidebarSplitter(self):
        self.sidebarSplitter = QSplitter(Qt.Orientation.Vertical, self.sidebar)
        self.sidebarSplitter.setChildrenCollapsible(False)
        self.sidebarSplitter.setHandleWidth(1)
        self.sidebarSplitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #3c3c3c; 
                border: 12px transparent;
                color: #1f1f1f;
            } 
            QSplitter {
                background-color: transparent;
                border: none;
            }
        """)
        self.sidebarLayout.addWidget(self.sidebarSplitter)

    def setupSidebar(self):
        self.sidebar = QFrame(self.splitter)
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        
        self.sidebar.setStyleSheet("background-color: #1f1f1f; border: none;")
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(0,0,0,0)

    def setupFilters(self):
        self.filterArea = QScrollArea(self.sidebarSplitter)
        self.filterArea.setWidgetResizable(True)
        self.filterArea.setStyleSheet("background-color: transparent; border: none;")


        self.filterWidget = QWidget(self.filterArea)
        self.filterWidget.setStyleSheet("background-color: transparent; border: none;")

        self.filterLayout = QVBoxLayout(self.filterWidget)
        self.filterLayout.setSpacing(4)
        self.filterLayout.setContentsMargins(0,0,0,0)

        self.filterArea.setWidget(self.filterWidget)
        self.filterArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.filterArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.filterArea.setMinimumHeight(100)


    def setupDataFrame(self):
        

        self.dataFrame = QFrame(self.splitter)
        self.dataFrame.setMinimumWidth(200)
        self.dataFrame.setStyleSheet("background-color: transparent; border: none;")

        dataFrameLayout = QVBoxLayout(self.dataFrame)
        dataFrameLayout.setContentsMargins(0,0,0,0)

        self.dataFrameBanner = QFrame(self.dataFrame)
        self.dataFrameBanner.setStyleSheet("background-color: transparent; border: none;")
        self.dataFrameBanner.setFixedHeight(50)
        dataFrameLayout.addWidget(self.dataFrameBanner)

        self.dataFrameHeader = QFrame(self.dataFrame)
        self.dataFrameHeader.setStyleSheet("background-color: transparent; border: none;")
        self.dataFrameHeader.setFixedHeight(50)
        dataFrameLayout.addWidget(self.dataFrameHeader)

        self.pageLabel = QLabel(self.dataFrameHeader)
        self.pageLabel.setFont(QFont("Microsoft Sans Serif", 18))
        self.pageLabel.setText("Welcome to Hive!")
        self.pageLabel.setStyleSheet("""
            QLabel {
                color: #EEEEEE;
                background-color: transparent;
                padding: 0px 0px 0px 30px;
            }
        """)
        

        self.dataScrollArea = QScrollArea(self.dataFrame)
        self.dataScrollArea.setWidgetResizable(True)
        self.dataScrollArea.setStyleSheet("background-color: transparent; border: none;")

        self.dataScrollWidget = QWidget(self.dataScrollArea)
        self.dataScrollWidget.setStyleSheet("background-color: transparent; border: none;")

        self.dataScrollLayout = QVBoxLayout(self.dataScrollWidget)
        self.dataScrollLayout.setSpacing(4)
        self.dataScrollLayout.setContentsMargins(10,10,10,10)

        self.dataScrollArea.setWidget(self.dataScrollWidget)
        self.dataScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.dataScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.dataScrollArea.setMinimumHeight(100)

        dataFrameLayout.addWidget(self.dataScrollArea)


    def setupScrollArea(self):
        self.scrollArea = QScrollArea(self.sidebarSplitter)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("background-color: transparent; border: none;")

        self.scrollWidget = QWidget(self.scrollArea)
        self.scrollWidget.setStyleSheet("background-color: transparent; border: none;")

        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setSpacing(4)
        self.scrollLayout.setContentsMargins(10,10,10,10)

        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scrollArea.setMinimumHeight(100)


    def setupSidebarButtons(self):

        self.teams = {
            "btnSMS": {"text":"SMS & Costing","icon":QIcon("icons/sms_costing.svg")},
            "btnCAD": {"text":"Customer Disputes","icon":QIcon("icons/customer_disputes.svg")},
            "btnCIR": {"text":"Customer Incentives","icon":QIcon("icons/customer_incentives.svg")},
            "btnDPM": {"text":"Deviated Agreements","icon":QIcon("icons/deviated_agreements.svg")},
            "btnUSDA": {"text":"USDA Agreements","icon":QIcon("icons/usda.svg")},
            "btnQA": {"text":"Quality Assurance","icon":QIcon("icons/quality_assurance.svg")}
        }
        
        for team in self.teams:
            self.createButton(team, self.teams[team]["text"])

        footerSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.scrollLayout.addSpacerItem(footerSpacer)

    def createButton(self, objName, text):
        button = QPushButton(text, self.scrollWidget)
        button.setObjectName(objName)
        button.setFont(QFont("Microsoft Sans Serif", 11))
        button.setStyleSheet(self.getButtonStyleSheet("text"))
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

    def getButtonStyleSheet(self, bType, active=False):
        baseStyle = """
            QPushButton {{
                text-align: {alignment};
                border: none;
                padding: 8px;
                border-radius: 4px;
                color: {color};
                background-color: {bg_color};
            }}
            QPushButton:hover {{
                background-color: {hover_bg_color};
                color: #FFFFFF;
            }}
        """

        align = "left" if bType == "text" else "center"

        if active:
            return baseStyle.format(alignment=align, color="#EEEEEE", bg_color="#2F2F2F", hover_bg_color="#3F3F3F")

        return baseStyle.format(alignment=align, color="#BDBDBD", bg_color="transparent", hover_bg_color="#2F2F2F")

    def onButtonClicked(self):
        clickedButton = self.sender()
        self.pageLabel.setText(self.teams[clickedButton.objectName()]["text"])
        self.pageLabel.adjustSize()
        
        for button in self.scrollWidget.findChildren(QPushButton):

            bType = "icon" if button.text() == "" else "text"
            if button is clickedButton:
                button.setStyleSheet(self.getButtonStyleSheet(bType, True))
            else:
                button.setStyleSheet(self.getButtonStyleSheet(bType))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
