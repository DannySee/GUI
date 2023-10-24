import sys
import data_pull as db
import style_sheets as style
from sidebar_maps import button_map as naviButtonMap, filter_map as filterMap
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QMouseEvent, QPalette
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
        self.setGeometry(200, 500, 1000, 800)
        self.setWindowTitle("Hive Data Center")
        self.initUI()

    def initUI(self):
        # Calling setup functions to initialize UI components
        self.buildContainer()
        self.buildSidebar()
        self.buildMainPage()       

        # Configuring sidebar and scroll area sizes
        self.containerSplitter.setStretchFactor(0, 0)
        self.containerSplitter.setStretchFactor(1, 1)
        self.containerSplitter.setSizes([self.sidebar.minimumWidth(), self.container.width()])

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
        self.containerSplitter.setStretchFactor(0, 0)
        self.containerSplitter.setStretchFactor(1, 1)

    def buildSidebar(self):
        self.sidebar = QFrame(self.containerSplitter)
        self.sidebar.setStyleSheet(style.light_gray_frame)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(0,0,0,0)

        self.buildSidebarResizeButton()
        self.buildSidebarSplitter()
        self.buildSidebarNavigation()
        self.buildSidebarMenu()

        self.sidebar_height = self.naviButtonFrame.sizeHint().height()
        self.sidebar_width = 200

        self.sidebar.setMinimumWidth(self.sidebar_width)
        self.sidebar.setMaximumWidth(self.sidebar_width+100)
        self.naviScrollArea.setMaximumHeight(self.sidebar_height)
        self.sidebarSplitter.setSizes([self.sidebar_height,10])

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
            activeButtonCSS = style.icon_button_active
            alignment = Qt.AlignmentFlag.AlignCenter
            mgn = 0
            collapse = True

        else:
            width = self.sidebar_width
            icon = QIcon("icons/chevron-left.svg")
            activeButtonCSS = style.text_button_active
            alignment = Qt.AlignmentFlag.AlignLeft
            mgn = 10
            collapse = False

        self.sidebar.setMinimumWidth(width)
        self.sidebar.setMaximumWidth(width+100)
        self.containerSplitter.setSizes([width, self.container.width()])
        self.collapseButton.setIcon(icon)
        self.naviLayout.setAlignment(alignment)
        self.naviLayout.setContentsMargins(mgn,mgn,mgn,mgn)

        for button in self.naviButtonFrame.findChildren(QPushButton):

            if collapse:
                button.setIconSize(QSize(20,20))
                button.setToolTip(button.text())
                button.setIcon(naviButtonMap[button.objectName()]["icon"])
                button.setText("")
                button.setStyleSheet(style.icon_button_inactive)
                button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed) 

            else:
                button.setToolTip("")
                button.setIcon(QIcon())
                button.setText(naviButtonMap[button.objectName()]["text"])
                button.setStyleSheet(style.text_button_inactive)
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed) 

        if self.menuFrame.isVisible(): self.activeNaviButton.setStyleSheet(activeButtonCSS)
            
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

        self.activeNaviButton = None
        self.naviLayout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def naviButtonClicked(self):
        if self.activeNaviButton is not self.sender():
            self.tableScrollArea.hide()
            self.quickFilterFrame.hide()

            self.activeNaviButton = self.sender()
            activeObject = self.activeNaviButton.objectName()
            activeLabel = naviButtonMap[self.activeNaviButton.objectName()]['text']
            activeText = self.activeNaviButton.text()

            self.pageLabel.setText(activeLabel)
            self.pageLabel.adjustSize()

            self.menuLabel.setText(activeLabel)
            self.menuLabel.adjustSize()

            self.populateSidebarMenu(naviButtonMap[activeObject]["tables"].keys())
            self.tableRef = naviButtonMap[activeObject]["tables"]

            inactiveCSS = style.icon_button_inactive if activeText == "" else style.text_button_inactive 
            activeCSS = style.icon_button_active if activeText == "" else style.text_button_active

            for button in self.naviButtonFrame.findChildren(QPushButton):
                button.setStyleSheet(inactiveCSS)

            self.activeNaviButton.setStyleSheet(activeCSS)

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

        self.menuComboBox = QComboBox(self.menuFrame)
        self.menuComboBox.setPlaceholderText("--Select Data--")
        self.menuLayout.addWidget(self.menuComboBox)

        self.menuLayout.addSpacerItem(QSpacerItem(15,15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.quickFilterFrame = QFrame(self.menuFrame)
        self.quickFilterFrame.setStyleSheet(style.hidden)
        self.menuLayout.addWidget(self.quickFilterFrame)

        self.quickFilterLayout = QVBoxLayout(self.quickFilterFrame)
        self.quickFilterLayout.setSpacing(4)
        self.quickFilterLayout.setContentsMargins(0,0,0,0)

        self.menuLine = QFrame(self.quickFilterFrame)
        self.menuLine.setFrameShape(QFrame.Shape.HLine)
        self.menuLine.setFixedHeight(1)
        self.menuLine.setStyleSheet(style.dividing_line)
        self.quickFilterLayout.addWidget(self.menuLine)

        self.quickFilterHeader = QFrame(self.quickFilterFrame)
        self.quickFilterLayout.addWidget(self.quickFilterHeader)

        self.quickFilterHeaderLayout = QHBoxLayout(self.quickFilterHeader)

        self.quickFilterLabel = QLabel(self.quickFilterHeader)
        self.quickFilterLabel.setText("")
        self.quickFilterLabel.setStyleSheet(style.sidebar_label)      
        self.quickFilterHeaderLayout.addWidget(self.quickFilterLabel)   

        self.quickFilterClearButton = QPushButton(self.quickFilterHeader)
        self.quickFilterClearButton.setIcon(QIcon("icons/clear-filter.svg"))
        self.quickFilterClearButton.setStyleSheet(style.control_button)
        self.quickFilterClearButton.setFixedWidth(self.quickFilterClearButton.height())
        self.quickFilterClearButton.setToolTip("Clear Filters")
        self.quickFilterHeaderLayout.addWidget(self.quickFilterClearButton)
        self.quickFilterClearButton.clicked.connect(self.clearQuickFilters)     

        self.menuLayout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.menuFrame.hide()

    def populateSidebarMenu(self, releventTables):

        if self.menuComboBox.count() > 0: 
            self.menuComboBox.currentIndexChanged.disconnect(self.menuComboBoxChanged)
            self.menuComboBox.clear()
        else:
            self.menuFrame.show()

        self.menuComboBox.setStyleSheet(style.default_combobox)           
        self.menuComboBox.addItems(releventTables)
        self.menuComboBox.setCurrentIndex(-1)
        self.menuComboBox.currentIndexChanged.connect(self.menuComboBoxChanged)

    def populateQuickFilters(self, menuSelection):
        self.quickFilterLabel.setText("Quick Filters:")  
        self.quickFilterLabel.adjustSize()      
        filters = filterMap[menuSelection]

        for child in self.quickFilterFrame.findChildren(QLineEdit):
            child.deleteLater()

        for filter in filters:
            quickFilter = QLineEdit(self.quickFilterFrame)
            quickFilter.setPlaceholderText(filter) 
            quickFilter.setStyleSheet(style.quick_filter)
            quickFilter.textChanged.connect(self.quickFilterChanged)
            self.quickFilterLayout.addWidget(quickFilter)

    def quickFilterChanged(self):
        df = self.df
        
        for quickFilter in self.quickFilterFrame.findChildren(QLineEdit):
            if quickFilter.text() != "":
                field = quickFilter.placeholderText()
                value = quickFilter.text()
                df = df[df[field].str.contains(value, case=False)]
                model = TableModel(df)
                self.table.setModel(model)
        
    def clearQuickFilters(self):
        for child in self.quickFilterFrame.findChildren(QLineEdit):
            child.setText("")

        model = TableModel(self.df)
        self.table.setModel(model)

    def menuComboBoxChanged(self):
        menuSelection = self.menuComboBox.currentText()
        self.activeTable = self.tableRef[menuSelection]
        self.menuComboBox.setStyleSheet(style.active_combobox)

        if self.activeTable is not None:
            self.showLoadingPage()
            self.df = db.get_cal_programs(self.activeTable)
            self.hideLoadingPage()

            self.pageLabel.setText(menuSelection)
            model = TableModel(self.df)
            self.table.setModel(model)
            self.tableScrollArea.setMaximumWidth(self.table.horizontalHeader().length()+40)
            self.tableScrollArea.show()

            self.populateQuickFilters(menuSelection)
            self.quickFilterFrame.show()

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
