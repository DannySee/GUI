import sys
import data_pull as db
import style_sheets as style
from sidebar_maps import map as naviButtonMap
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
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
    

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

        # Configuring sidebar and scroll area sizes
        #self.configureSidebarAndScrollAreaSizes()

        # Configuring splitter sizes
        #self.configureSplitterSizes()

        # Setting central widget
        self.setCentralWidget(self.container)

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

        self.buildSidebarResizeButton()
        self.buildSidebarSplitter()
        self.buildSidebarNavigation()
        self.buildSidebarMenu()

        self.naviScrollArea.setMaximumHeight(self.naviButtonFrame.sizeHint().height())
        self.sidebarSplitter.setSizes([self.naviScrollArea.maximumHeight(),10])

    def buildSidebarResizeButton(self):
        self.resizeFrame = QFrame(self.sidebar)
        self.resizeFrame.setFixedHeight(35)
        self.resizeFrame.setStyleSheet(style.hidden)
        self.sidebarLayout.addWidget(self.resizeFrame)

        self.resizeLayout = QHBoxLayout(self.resizeFrame)
        self.resizeLayout.setContentsMargins(5,5,5,5)
        self.resizeLayout.addSpacerItem(QSpacerItem(25,25, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.collapseButton = QPushButton(self.resizeFrame)
        self.collapseButton.setIcon(QIcon("icons/chevron-left.svg"))
        self.collapseButton.setFixedWidth(25)
        self.collapseButton.setStyleSheet(style.ui_button)
        self.collapseButton.clicked.connect(self.resizeSidebar)
        self.resizeLayout.addWidget(self.collapseButton)

    def resizeSidebar(self):  

        if self.containerSplitter.sizes()[0] > 50:
            width = 50
            icon = QIcon("icons/chevron-right.svg")
            alignment = Qt.AlignmentFlag.AlignCenter
            margin = 0
            collapse = True

        else:
            width = 200
            icon = QIcon("icons/chevron-left.svg")
            alignment = Qt.AlignmentFlag.AlignLeft
            margin = 10
            collapse = False

        self.sidebar.setMinimumWidth(width)
        self.sidebar.setMaximumWidth(width+100)
        self.containerSplitter.setSizes([width, self.container.width()])
        self.collapseButton.setIcon(icon)
        self.naviLayout.setContentsMargins(margin,margin,margin,margin)
        self.naviLayout.setAlignment(alignment)

        for button in self.naviButtonFrame.findChildren(QPushButton):

            if collapse:
                button.setToolTip(button.text())
                button.setIcon(naviButtonMap[button.objectName()]["icon"])
                button.setText("")
                button.adjustSize()
                button.setStyleSheet(style.icon_button_inactive)

            else:
                button.setToolTip("")
                button.setIcon(QIcon())
                button.setText(naviButtonMap[button.objectName()]["text"])
                button.adjustSize()
                button.setStyleSheet(style.text_button_inactive)

    def buildMainPage(self):
        self.mainPage = QFrame(self.containerSplitter)
        self.mainPage.setMinimumWidth(200)
        self.mainPage.setStyleSheet(style.hidden)

        self.mainLayout = QVBoxLayout(self.mainPage)
        self.mainLayout.setContentsMargins(50,20,50,20)

        self.bannerFrame = QFrame(self.mainPage)
        self.bannerFrame.setFixedHeight(50)
        self.bannerFrame.setStyleSheet(style.hidden)
        self.mainLayout.addWidget(self.bannerFrame)

        self.headerFrame = QFrame(self.mainPage)
        self.headerFrame.setFixedHeight(50)
        self.headerFrame.setStyleSheet(style.hidden)
        self.mainLayout.addWidget(self.headerFrame)

        self.pageLabel = QLabel(self.headerFrame)
        self.pageLabel.setText("Welcome to Commercial Services Hive")
        self.pageLabel.setStyleSheet(style.page_label)

        self.bodyFrame = QFrame(self.mainPage)
        self.bodyFrame.setStyleSheet(style.hidden)
        self.mainLayout.addWidget(self.bodyFrame)

        self.tableSplitter = QSplitter(Qt.Orientation.Vertical, self.bodyFrame)
        self.tableSplitter.setChildrenCollapsible(False)
        self.tableSplitter.setStyleSheet(style.hidden_splitter)
        self.mainLayout.addWidget(self.tableSplitter)

        self.tableScrollArea = QScrollArea(self.tableSplitter)
        self.tableScrollArea.setWidgetResizable(True)
        self.tableScrollArea.setStyleSheet(style.hidden)

        self.utilityScrollArea = QScrollArea(self.tableSplitter)
        self.utilityScrollArea.setWidgetResizable(True)
        self.utilityScrollArea.setStyleSheet(style.hidden)

        self.table = QTableView(self.tableScrollArea)
        self.tableDelegate = CustomDelegate(self.table)
        self.table.setItemDelegate(self.tableDelegate)
        self.table.horizontalScrollBar().setStyleSheet(style.horizontal_scrollbar)
        self.table.verticalScrollBar().setStyleSheet(style.vertical_scrollbar)
        self.table.setStyleSheet(style.table)

         # keeping layout although it is not really necessary in case I do not like the utility scoll area in separate space
        self.tableScrollLayout = QVBoxLayout(self.tableScrollArea)
        self.tableScrollLayout.setSpacing(4)
        self.tableScrollLayout.setContentsMargins(10,10,10,10)
        self.tableScrollLayout.addWidget(self.table)

        self.tableScrollArea.setWidget(self.table)
        self.tableScrollArea.hide()

    def buildSidebarSplitter(self):
        self.sidebarSplitter = QSplitter(Qt.Orientation.Vertical, self.sidebar)
        self.sidebarSplitter.setChildrenCollapsible(False)
        self.sidebarSplitter.setHandleWidth(1)
        self.sidebarSplitter.setStyleSheet(style.visible_splitter)
        self.sidebarLayout.addWidget(self.sidebarSplitter)

    def buildSidebarNavigation(self):
        self.naviScrollArea = QScrollArea(self.sidebarSplitter)
        self.naviScrollArea.setWidgetResizable(True)
        self.naviScrollArea.setStyleSheet(style.hidden)
        self.naviScrollArea.setMinimumHeight(100)
        self.naviScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.naviScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.naviButtonFrame = QWidget(self.naviScrollArea)
        self.naviButtonFrame.setStyleSheet(style.hidden)
        self.naviScrollArea.setWidget(self.naviButtonFrame)

        self.naviLayout = QVBoxLayout(self.naviButtonFrame)
        self.naviLayout.setSpacing(4)
        self.naviLayout.setContentsMargins(10,10,10,10)

        for button_name, map in naviButtonMap.items():
            naviButton = QPushButton(map["text"], self.naviButtonFrame)
            naviButton.setObjectName(button_name)
            naviButton.setStyleSheet(style.text_button_inactive)
            naviButton.clicked.connect(self.naviButtonClicked)
            self.naviLayout.addWidget(naviButton)

        self.naviLayout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def naviButtonClicked(self):
        clickedButton = self.sender()

        self.pageLabel.setText(clickedButton.text())
        self.pageLabel.adjustSize()

        self.menuLabel.setText(clickedButton.text())
        self.menuLabel.adjustSize()

        self.populateSidebarMenu(naviButtonMap[clickedButton.objectName()]["tables"].keys())
        self.tableRef = naviButtonMap[clickedButton.objectName()]["tables"]

        if self.containerSplitter.sizes()[0] == 50:
            self.resizeSidebar()

    def buildSidebarMenu(self):
        self.menuScrollArea = QScrollArea(self.sidebarSplitter)
        self.menuScrollArea.setWidgetResizable(True)
        self.menuScrollArea.setMinimumHeight(100)
        self.menuScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.menuScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.menuScrollArea.setStyleSheet(style.hidden)

        self.menuFrame = QWidget(self.menuScrollArea)
        self.menuFrame.setStyleSheet(style.hidden)
        self.menuScrollArea.setWidget(self.menuFrame)

        self.menuLayout = QVBoxLayout(self.menuFrame)
        self.menuLayout.setSpacing(4)
        self.menuLayout.setContentsMargins(10,10,10,10)

        self.menuLabel = QLabel(self.menuFrame)
        self.menuLabel.setText("")
        self.menuLabel.setStyleSheet(style.sidebar_label)               
        self.menuLayout.addWidget(self.menuLabel)

        self.menuLayout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.menuComboBox = QComboBox(self.menuFrame)
        self.menuComboBox.setStyleSheet(style.combobox)
        self.menuLayout.addWidget(self.menuComboBox)

        self.menuLayout.addSpacerItem(QSpacerItem(20,20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.menuLine = QFrame(self.menuFrame)
        self.menuLine.setFrameShape(QFrame.Shape.HLine)
        self.menuLine.setFixedHeight(1)
        self.menuLine.setStyleSheet(style.dividing_line)
        self.menuLayout.addWidget(self.menuLine)

        self.menuLayout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.menuFrame.hide()

    def populateSidebarMenu(self, releventTables):

        if self.menuComboBox.count() > 0: 
            self.menuComboBox.currentIndexChanged.disconnect(self.menuComboBoxChanged)
            self.menuComboBox.clear()
        else:
            self.menuFrame.show()
            
        self.menuComboBox.addItems(releventTables)
        self.menuComboBox.setCurrentIndex(0)
        self.menuComboBox.currentIndexChanged.connect(self.menuComboBoxChanged)

    def menuComboBoxChanged(self):
        menuSelection = self.menuComboBox.currentText()
        table = self.tableRef[menuSelection]

        if table is not None:
            self.showLoadingPage()

            df = db.get_cal_programs(table)

            self.hideLoadingPage()

            self.pageLabel.setText(menuSelection)
            model = TableModel(df)
            self.table.setModel(model)
            self.tableSplitter.setMaximumWidth(self.table.horizontalHeader().length())
            self.tableScrollArea.show()

    def showLoadingPage(self):
        self.table.hide()
        self.savedLabel = self.pageLabel.text()
        self.pageLabel.setText("Loading....")
        QApplication.processEvents()

    def hideLoadingPage(self):
        self.table.show()
        self.pageLabel.setText(self.savedLabel)


# ------------------------- Main Execution -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
