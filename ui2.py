import sys
import data_pull as db
import style_sheets as style
from sidebar_maps import map as sidebarButtonMap
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout, 
                             QLabel, QLineEdit, QMainWindow, QPushButton, QScrollArea, 
                             QSizePolicy, QSpacerItem, QSplitter, QSplitterHandle, 
                             QStyledItemDelegate, QTableView, QVBoxLayout, QWidget)

# ------------------------- CustomDelegate Class -------------------------
class CustomDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        self.applyStyleSheetAndValueIfLineEdit(editor, index)
        return editor

    def setEditorData(self, editor, index):
        if not isinstance(editor, QLineEdit):
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QLineEdit):
            model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)
        else:
            super().setModelData(editor, model, index)

    def applyStyleSheetAndValueIfLineEdit(self, editor, index):
        if isinstance(editor, QLineEdit):
            editor.setStyleSheet(style.table)
            value = index.data(Qt.ItemDataRole.EditRole) or index.data(Qt.ItemDataRole.DisplayRole)
            editor.setText(value)
            index.model().setData(index, "", Qt.ItemDataRole.EditRole)


# ------------------------- TableModel Class -------------------------
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]
    
    def flags(self, index):
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable
    
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if index.isValid() and role == Qt.ItemDataRole.EditRole:
            row, col = index.row(), index.column()
            self._data.iat[row, col] = value  # Update the pandas DataFrame
            self.dataChanged.emit(index, index)  # Notify listeners that data has been changed
            return True
        return False
    

# ------------------------- MyWindow Class -------------------------
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 500, 800, 600)
        self.setWindowTitle("Hive Data Center")
        self.initUI()

    def initUI(self):
        # Calling setup functions to initialize UI components
        self.buildContainer()
        self.buildSidebar()
        self.buildMainPage()
        


        self.setupTableView()
        
        

        # Configuring sidebar and scroll area sizes
        self.configureSidebarAndScrollAreaSizes()

        # Configuring splitter sizes
        self.configureSplitterSizes()

        # Setting central widget
        self.setCentralWidget(self.mainFrame)

    def buildContainer(self):
        self.container = QFrame(self)
        self.container.setStyleSheet(style.dark_gray_frame)
        self.containerLayout = QVBoxLayout(self.container)
        self.containerLayout.setContentsMargins(0,0,0,0)

        self.buildContainerSplitter()

    def buildContainerSplitter(self):
        self.containerSplitter = QSplitter(Qt.Orientation.Horizontal, self.container)
        self.containerSplitter.setChildrenCollapsible(False)
        self.containerSplitter.setStyleSheet(style.hidden_splitter)
        self.containerLayout.addWidget(self.containerSplitter)

    def buildSidebar(self):
        self.sidebar = QFrame(self.containerSplitter)
        self.sidebar.setStyleSheet(style.light_gray_frame)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(0,0,0,0)

        self.buildCollapseButton()
        self.buildSidebarSplitter()
        self.buildSidebarNavigation()
        self.setupFilters()

    def buildCollapseButton(self):
        frame = QFrame(self.sidebar)
        frame.setFixedHeight(35)
        frame.setStyleSheet(style.hidden)
        self.sidebarLayout.addWidget(frame)
        layout = QHBoxLayout(layout)
        layout.setContentsMargins(5,5,5,5)
        layout.addSpacerItem(QSpacerItem(25,25, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.collapseButton = QPushButton(frame)
        self.collapseButton.setIcon(QIcon("icons/chevron-left.svg"))
        self.collapseButton.setFixedWidth(25)
        self.collapseButton.setStyleSheet(style.ui_button)
        self.collapseButton.clicked.connect(self.collapseSidebar)
        layout.addWidget(self.collapseButton)

    def buildMainPage(self):
        self.mainPage = QFrame(self.containerSplitter)
        self.mainPage.setMinimumWidth(200)
        self.mainPage.setStyleSheet(style.hidden)

        layout = QVBoxLayout(self.mainPage)
        layout.setContentsMargins(50,20,50,20)

        self.bannerFrame = QFrame(self.mainPage)
        self.bannerFrame.setFixedHeight(50)
        self.bannerFrame.setStyleSheet(style.hidden)
        layout.addWidget(self.bannerFrame)

        self.headerFrame = QFrame(self.mainPage)
        self.headerFrame.setFixedHeight(50)
        self.headerFrame.setStyleSheet(style.hidden)
        layout.addWidget(self.headerFrame)

        self.pageLabel = QLabel(self.headerFrame)
        self.pageLabel.setStyleSheet(style.page_label)

        self.bodyFrame = QFrame(self.mainPage)
        self.bodyFrame.setStyleSheet(style.hidden)
        layout.addWidget(self.bodyFrame)

        self.tableSplitter = QSplitter(Qt.Orientation.Vertical, self.bodyFrame)
        self.tableSplitter.setChildrenCollapsible(False)
        self.tableSplitter.setStyleSheet(style.hidden_splitter)
        layout.addWidget(self.tableSplitter)

        self.tableScrollArea = QScrollArea(self.tableSplitter)
        self.tableScrollArea.setStyleSheet(style.hidden)

        self.utilityScrollArea = QScrollArea(self.tableSplitter)
        self.utilityScrollArea.setStyleSheet(style.hidden)

    def buildSidebarSplitter(self):
        self.sidebarSplitter = QSplitter(Qt.Orientation.Vertical, self.sidebar)
        self.sidebarSplitter.setChildrenCollapsible(False)
        self.sidebarSplitter.setStyleSheet(style.visible_splitter)
        self.sidebarLayout.addWidget(self.sidebarSplitter)

    def buildSidebarNavigation(self):
        self.sidebarNaviContainer = QScrollArea(self.sidebarSplitter)
        self.sidebarNaviContainer.setWidgetResizable(True)
        self.sidebarNaviContainer.setStyleSheet(style.hidden)
        self.sidebarNaviContainer.setMinimumHeight(100)

        self.sidebarButtonFrame = QWidget(self.sidebarNaviContainer)
        self.sidebarButtonFrame.setStyleSheet(style.hidden)
        self.sidebarNaviContainer.setWidget(self.sidebarButtonFrame)

        self.sidebarNaviLayout = QVBoxLayout(self.sidebarButtonFrame)
        self.sidebarNaviLayout.setSpacing(4)
        self.sidebarNaviLayout.setContentsMargins(10,10,10,10)

        self.sidebarNaviContainer.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sidebarNaviContainer.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.buildSidebarButtons()




    def buildSidebarButtons(self):  
        for button, map in sidebarButtonMap:
            self.createButton(button, map["text"])

        self.sidebarNaviLayout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def createButton(self, objName, text):
        button = QPushButton(text, self.scrollWidget)
        button.setObjectName(objName)
        button.setStyleSheet(self.getButtonStyleSheet("text"))
        button.clicked.connect(self.onButtonClicked)
        self.sidebarNaviLayout.addWidget(button)


    def getButtonStyleSheet(self, bType, active=False):
        
        if bType == "icon" and active: return style.icon_button_active
        if bType == "icon" and not active: return style.icon_button_inactive
        if bType == "text" and active: return style.text_button_active
        if bType == "text" and not active: return style.text_button_inactive


    def onButtonClicked(self):
        if self.sidebar.maximumWidth() == 50: self.collapseSidebar()
        clickedButton = self.sender()
        self.pageLabel.setText(self.teams[clickedButton.objectName()]["text"])
        self.pageLabel.adjustSize()

        self.filterLabel.setText(self.teams[clickedButton.objectName()]["text"])
        self.setupComboBox(self.teams[clickedButton.objectName()]["tables"].keys())

        self.tableRef = self.teams[clickedButton.objectName()]["tables"]

        maxWidth = max(self.scrollWidget.sizeHint().width(), self.filterWidget.sizeHint().width())

        if maxWidth > self.sidebar.width():

            self.sidebar.setMinimumWidth(maxWidth)
            self.sidebar.setMaximumWidth(maxWidth+100)

            self.containerSplitter.setSizes([maxWidth, self.container.width()])
        
        for button in self.scrollWidget.findChildren(QPushButton):

            bType = "icon" if button.text() == "" else "text"
            if button is clickedButton:
                button.setStyleSheet(self.getButtonStyleSheet(bType, True))
            else:
                button.setStyleSheet(self.getButtonStyleSheet(bType))

    
        
        


    

# ------------------------- Main Execution -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
