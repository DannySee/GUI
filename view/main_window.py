import sys
import model.data_pull as db
import view.styles.style_sheets as style
import pandas as pd
import json
import time
import asyncio
from controller.sidebar_map import map as naviButtonMap
from ui_elements.sidebar_combobox import map as menuBoxMap
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QModelIndex, QItemSelectionModel, QTimer
from PyQt6.QtGui import QIcon, QMouseEvent, QPalette, QColor, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout, 
                             QLabel, QLineEdit, QMainWindow, QPushButton, QScrollArea, 
                             QSizePolicy, QSpacerItem, QSplitter, QSplitterHandle, 
                             QStyledItemDelegate, QTableView, QVBoxLayout, QWidget, QMessageBox, 
                             QAbstractItemView, QGraphicsDropShadowEffect, QGridLayout, QSizeGrip,
                             QCheckBox, QListView)



    

# ------------------------- MyWindow Class -------------------------
class MyWindow(QMainWindow):
    data = pd.DataFrame()
    changes = {}

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
                #index.model().setData(index, "")


    # ------------------------- TableModel Class -------------------------
    class TableModel(QtCore.QAbstractTableModel):
        def __init__(self, data):
            super(MyWindow.TableModel, self).__init__()
            self._data = data
            self._changes = {}

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

                actual_row = self._data.iloc[row].name
                MyWindow.data.iat[actual_row, col] = value
                self.handleChanges(actual_row, col, value)
                return True
            return False
        
        def handleChanges(self, row, col, value):

            if row not in MyWindow.changes: 
                MyWindow.changes[row] = {} 

            column_name = self._data.columns[col]  
            MyWindow.changes[row][column_name] = value  # Update the value in the nested dictionary
            print(MyWindow.changes)

        def headerData(self, section, orientation, role):
            if role == Qt.ItemDataRole.DisplayRole:
                if orientation == Qt.Orientation.Horizontal:
                    return str(self._data.columns[section])

                if orientation == Qt.Orientation.Vertical:
                    return str(self._data.index[section])

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
        self.collapseButton.setIcon(QIcon("ui_elements/icons/double-chevron-left.svg"))
        self.collapseButton.setFixedWidth(25)
        self.collapseButton.setStyleSheet(style.discrete_standard)
        self.collapseButton.clicked.connect(self.resizeSidebar)
        self.resizeLayout.addWidget(self.collapseButton)

    def resizeSidebar(self):  

        if self.containerSplitter.sizes()[0] > 50:
            width = 50
            icon = QIcon("ui_elements/icons/double-chevron-right.svg")
            activeButtonCSS = style.toggle_active
            alignment = Qt.AlignmentFlag.AlignCenter
            mgn = 0
            collapse = True

        else:
            width = self.sidebar_width
            icon = QIcon("ui_elements/icons/double-chevron-left.svg")
            activeButtonCSS = style.toggle_active
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
                button.setStyleSheet(style.toggle_inactive)
                button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed) 

            else:
                button.setToolTip("")
                button.setIcon(QIcon())
                button.setText(naviButtonMap[button.objectName()]["text"])
                button.setStyleSheet(style.toggle_inactive)
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed) 

        if self.menuFrame.isVisible(): self.activeNaviButton.setStyleSheet(activeButtonCSS)
            
    def buildMainPage(self):
        self.mainPage = QFrame(self.containerSplitter)
        self.mainPage.setMinimumWidth(200)
        self.mainPage.setStyleSheet(style.hidden)

        self.mainLayout = QVBoxLayout(self.mainPage)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)

        self.bannerLayout = QHBoxLayout()
        self.bannerLayout.setContentsMargins(5,5,5,5)
        self.bannerLayout.setSpacing(2)
        self.mainLayout.addLayout(self.bannerLayout)

        self.bannerLayout.addSpacerItem(QSpacerItem(10,10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.bannerLabel = QLabel(self.mainPage)
        self.bannerLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.bannerLabel.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: #BDBDBD;
                border-radius: 8px;
                font-family: "Microsoft Sans Serif";
                font-size: 12px;
            }
        """)
        self.bannerLabel.setFixedWidth(150)
        self.bannerLayout.addWidget(self.bannerLabel)

        self.bannerLayout.addSpacerItem(QSpacerItem(10,10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.exportButton = QPushButton(self.mainPage)
        self.exportButton.setIcon(QIcon("ui_elements/icons/export.svg"))
        self.exportButton.setIconSize(QSize(20,20))
        #self.exportButton.clicked.connect(db.save_changes(self.activeTable, MyWindow.changes))
        self.exportButton.setToolTip("Export Table to Excel")
        self.exportButton.setStyleSheet(style.discrete_small)
        self.bannerLayout.addWidget(self.exportButton)

        self.importButton = QPushButton(self.mainPage)
        self.importButton.setIcon(QIcon("ui_elements/icons/import.svg"))
        self.importButton.setIconSize(QSize(20,20))
        #self.importButton.clicked.connect(db.save_changes(self.activeTable, MyWindow.changes))
        self.importButton.setToolTip("Import Table to Excel")
        self.importButton.setStyleSheet(style.discrete_small)
        self.bannerLayout.addWidget(self.importButton)

        self.saveButton = QPushButton(self.mainPage)
        self.saveButton.setIcon(QIcon("ui_elements/icons/save.svg"))
        self.saveButton.setIconSize(QSize(20,20))
        self.saveButton.clicked.connect(self.initiateSave)
        self.saveButton.setToolTip("Save Changes")
        self.saveButton.setStyleSheet(style.discrete_small)
        self.bannerLayout.addWidget(self.saveButton)


        self.pageScrollArea = QScrollArea(self.mainPage)
        self.pageScrollArea.setStyleSheet(style.hidden)
        self.pageScrollArea.setWidgetResizable(True)
        self.pageScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.pageScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.mainLayout.addWidget(self.pageScrollArea)

        self.pageScrollWidget = QWidget(self.pageScrollArea)
        self.pageScrollWidget.setStyleSheet(style.hidden)
        self.pageScrollWidget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.pageScrollArea.setWidget(self.pageScrollWidget)

        self.pageLayout = QVBoxLayout(self.pageScrollWidget)
        self.pageLayout.setContentsMargins(50,20,50,50)
        self.pageLayout.setSpacing(10)

        self.pageLayout.addSpacing(10)
        
        self.pageLabel = QLabel(self.pageScrollWidget)
        self.pageLabel.setText("Welcome to Commercial Services Hive")
        self.pageLabel.setStyleSheet(style.header)
        self.pageLayout.addWidget(self.pageLabel)

        self.pageLayout.addSpacing(10)

        self.pageSubLabel = QLabel(self.pageScrollWidget)
        self.pageSubLabel.setText("Welcome to Commercial Services Hive")
        self.pageSubLabel.setStyleSheet(style.page_sub_label)
        self.pageLayout.addWidget(self.pageSubLabel)

        self.allFilterFrame = QFrame(self.pageScrollWidget)
        self.allFilterFrame.setStyleSheet("""
            QFrame {
                background-color: #1f1f1f;
                border-radius: 10px;
                border:1px solid #3c3c3c;
            }                                         
        """)
        self.pageLayout.addWidget(self.allFilterFrame)

        self.allFilterLayout = QVBoxLayout(self.allFilterFrame)
        self.allFilterLayout.setContentsMargins(0,0,0,0)
        self.allFilterLayout.setSpacing(0)
        self.allFilterFrame.setLayout(self.allFilterLayout)

        self.allFilterHeaderLayout = QHBoxLayout()
        self.allFilterHeaderLayout.setContentsMargins(0,0,0,0)
        self.allFilterHeaderLayout.setSpacing(4)
        self.allFilterLayout.addLayout(self.allFilterHeaderLayout)

        self.allFilterButton = QPushButton()
        self.allFilterButton.setText("All Filters")
        self.allFilterButton.setIcon(QIcon("ui_elements/icons/chevron-down.svg"))
        self.allFilterButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #BDBDBD;
                font-family: "Microsoft Sans Serif";
                font-size: 14px;
                text-align: left;  
                padding: 10;
                qproperty-layoutDirection: RightToLeft;
                outline: 0;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2F2F2F;
                color: #EEEEEE;
            }
        """)
        self.allFilterButton.clicked.connect(self.expandAllFilters)
        self.allFilterHeaderLayout.addWidget(self.allFilterButton)

        self.clearAllFiltersButton = QPushButton(self.allFilterFrame)
        self.clearAllFiltersButton.setText("Clear Filters")
        self.clearAllFiltersButton.setIcon(QIcon("ui_elements/icons/clear-filter.svg"))
        self.clearAllFiltersButton.clicked.connect(self.clearAllFilters)
        self.clearAllFiltersButton.setMaximumWidth(self.clearAllFiltersButton.sizeHint().width() + 25)
        self.clearAllFiltersButton.setStyleSheet("""
            QPushButton {
                text-align: center;
                background-color: #2F2F2F;
                border: none;
                color: #EEEEEE;
                font-family: "Microsoft Sans Serif";
                font-size: 14px;
                text-align: left;  
                padding: 10px;
                qproperty-layoutDirection: RightToLeft;
                outline: 0;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #3F3F3F;
            }
        """)
        self.clearAllFiltersButton.hide()
        self.allFilterHeaderLayout.addWidget(self.clearAllFiltersButton)
        self.resetAllFilters()

        self.table = QTableView(self.pageScrollWidget)
        self.tableDelegate = self.CustomDelegate(self.table)
        self.table.setItemDelegate(self.tableDelegate)
        self.table.horizontalScrollBar().setStyleSheet(style.horizontal_scrollbar)
        self.table.verticalScrollBar().setStyleSheet(style.vertical_scrollbar)
        self.table.setStyleSheet(style.table)
        self.table.verticalHeader().setVisible(False) 
        self.table.setSortingEnabled(True)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setMinimumHeight(300)
        self.pageLayout.addWidget(self.table)



        #self.pageUtility = QFrame(self.pageScrollWidget)
        #self.pageUtility.setStyleSheet("""
        #    QFrame {
        #        background-color: #1f1f1f;
        #        border-radius: 10px;
        #        border:1px solid #3c3c3c;
        #    }                                         
        #""")
        #self.pageUtility.setFixedHeight(100)
        #self.pageLayout.addWidget(self.pageUtility)


    def expandAllFilters(self):

        if self.allFilterFrame.findChildren(QLineEdit) == []:
            self.allFilterButton.setIcon(QIcon("ui_elements/icons/chevron-up.svg"))
            self.allFilterButton.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #EEEEEE;
                    font-family: "Microsoft Sans Serif";
                    font-size: 14px;
                    text-align: left;  
                    padding: 10;
                    qproperty-layoutDirection: RightToLeft;
                    outline: 0;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #2F2F2F;
                    color: #EEEEEE;
                }
            """)

            self.filterGrid = QGridLayout()
            self.filterGrid.setContentsMargins(10,10,10,10)
            self.filterGrid.setSpacing(10)
            self.allFilterLayout.addLayout(self.filterGrid)

            fields = MyWindow.data.columns.tolist()
            row = 0

            for col_idx, col_name in enumerate(fields):
                if col_idx % 7 == 0:
                    row += 1

                filter = QLineEdit(self.allFilterFrame)
                filter.setPlaceholderText(col_name) 
                
                if self.appliedFilters is not None:
                    filter.setText(self.appliedFilterDict[col_name])

                filter.setStyleSheet(style.input_box)
                filter.textChanged.connect(self.allFilterchanged)
                self.filterGrid.addWidget(filter, row, col_idx % 7)

        else:
            self.collapseAllFilters()


    def collapseAllFilters(self):
        self.allFilterButton.setIcon(QIcon("ui_elements/icons/chevron-down.svg"))
        self.allFilterButton.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #BDBDBD;
                    font-family: "Microsoft Sans Serif";
                    font-size: 14px;
                    text-align: left;  
                    padding: 10;
                    qproperty-layoutDirection: RightToLeft;
                    outline: 0;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #2F2F2F;
                    color: #EEEEEE;
                }
            """)
        
        for child in self.allFilterFrame.findChildren(QLineEdit):
            child.deleteLater()

        self.filterGrid.deleteLater()


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
            naviButton.setStyleSheet(style.toggle_inactive)
            naviButton.clicked.connect(self.naviButtonClicked)
            self.naviLayout.addWidget(naviButton)

        self.activeNaviButton = None
        self.naviLayout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def naviButtonClicked(self):
        if self.activeNaviButton is not self.sender():
            self.pageScrollArea.hide()
            self.quickFilterSettings.hide()
            self.quickFilterFrame.hide()
            self.quickFilterClearButton.hide()

            self.activeNaviButton = self.sender()
            activeObject = self.activeNaviButton.objectName()
            activeText = self.activeNaviButton.text()

            self.pageLabel.setText(naviButtonMap[self.activeNaviButton.objectName()]['page_label'])
            self.pageLabel.adjustSize()

            self.menuLabel.setText(naviButtonMap[self.activeNaviButton.objectName()]['text'])
            self.menuLabel.adjustSize()

            self.populateSidebarMenu(naviButtonMap[activeObject]["options"])

            inactiveCSS = style.toggle_inactive if activeText == "" else style.toggle_inactive 
            activeCSS = style.toggle_active if activeText == "" else style.toggle_active

            for button in self.naviButtonFrame.findChildren(QPushButton):
                button.setStyleSheet(inactiveCSS)

            self.activeNaviButton.setStyleSheet(activeCSS)

    def initiateSave(self):
        # This method starts the saving process and updates the UI
        if self.activeTable is not None and MyWindow.changes != {}:
            self.saveMessage()
            QTimer.singleShot(0, self.saveChanges)  # This will call saveChanges() almost immediately but still allow the UI to update
        else:
            self.noChanges()
            
    def saveMessage(self):
        # This method updates the UI to show the saving message
        self.bannerLabel.setText("Saving Changes...")

    def saveChanges(self):
        # This method performs the actual saving logic
        db.save_changes(self.activeTable, MyWindow.changes)
        MyWindow.changes = {}
        QTimer.singleShot(500, self.finishSaving)  # Call finishSaving() after 1 second to update the message

    def finishSaving(self):
        # This method updates the UI after saving is done
        self.bannerLabel.setText("Changes Saved!")
        self.bannerLabel.setStyleSheet("""
            QLabel {
                background-color: rgba(99,111,100, 0.5);
                color: #EEEEEE;
                border-radius: 8px;
                font-family: "Microsoft Sans Serif";
                font-size: 12px;
            }
        """)
        QTimer.singleShot(2000, self.clearMessage)  # Schedule the clearing of the message after another second

    def noChanges(self):
        # This method updates the UI after saving is done
        self.bannerLabel.setText("No Changes to Save")
        QTimer.singleShot(1000, self.clearMessage)

    def clearMessage(self):
        # This method clears the saving message from the UI
        self.bannerLabel.setText("")
        self.bannerLabel.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: #BDBDBD;
                border-radius: 8px;
                font-family: "Microsoft Sans Serif";
                font-size: 12px;
            }
        """)




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
        self.menuLabel.setStyleSheet(style.menu)               
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
        self.quickFilterHeaderLayout.setSpacing(4)
        self.quickFilterHeaderLayout.setContentsMargins(0,0,0,0)

        self.quickFilterLabel = QLabel(self.quickFilterHeader)
        self.quickFilterLabel.setText("")
        self.quickFilterLabel.setStyleSheet(style.slicer)      
        self.quickFilterHeaderLayout.addWidget(self.quickFilterLabel)   

        self.quickFilterClearButton = QPushButton(self.quickFilterHeader)
        self.quickFilterClearButton.setIcon(QIcon("ui_elements/icons/clear-filter.svg"))
        self.quickFilterClearButton.setStyleSheet(style.discrete_standard)
        self.quickFilterClearButton.setFixedWidth(self.quickFilterClearButton.height())
        self.quickFilterClearButton.setToolTip("Clear Filters")
        self.quickFilterClearButton.clicked.connect(self.clearQuickFilters)     
        self.quickFilterHeaderLayout.addWidget(self.quickFilterClearButton)
        self.quickFilterClearButton.hide()

        self.menuLayout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.quickFilterSettings = QPushButton(self.menuFrame)
        self.quickFilterSettings.setIcon(QIcon("ui_elements/icons/settings.svg"))
        self.quickFilterSettings.setStyleSheet(style.discrete_standard)
        self.quickFilterSettings.setToolTip("Quick Slicer Settings")
        self.quickFilterSettings.setFixedWidth(30)
        self.quickFilterSettings.clicked.connect(self.quickFilterSettingsClicked)
        self.menuLayout.addWidget(self.quickFilterSettings)

        self.quickFilterSettings.hide()
        self.quickFilterFrame.hide()
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

    def populateQuickFilters(self):
        self.quickFilterLabel.setText("Quick Slicers:")  
        self.quickFilterLabel.adjustSize()  

        with open(f"default_config/table_map/{self.activeTable}.json", "r") as f:
            filters = json.load(f)

        for child in self.quickFilterFrame.findChildren(QLineEdit):
            child.deleteLater()

        for filter in filters['slicers']:
            quickFilter = QLineEdit(self.quickFilterFrame)
            quickFilter.setPlaceholderText(filter) 
            quickFilter.setStyleSheet(style.input_box)
            quickFilter.textChanged.connect(self.quickFilterChanged)
            self.quickFilterLayout.addWidget(quickFilter)


    def clearAllFilters(self):
        # Ensure the widget is in the layout
        self.clearAllFiltersButton.hide()

        
        # Clear line edits
        for child in self.allFilterFrame.findChildren(QLineEdit):
            child.setText("")
        
        # Reset the table model
        self.populateTable(MyWindow.data)
        
        # Reset filters
        self.resetAllFilters()


    def populateTable(self, df):
        model = self.TableModel(df)
        self.table.setModel(model)
        self.vertical_resize_table_to_content()


    def hideClearFilterButton(self):
        self.clearAllFiltersButton.hide()
       


    def resetAllFilters(self):  
        # Reset filters
        self.appliedFilters = None
        self.appliedFilterDict = {}
        self.filterCount = 0


    def allFilterchanged(self):
        df = MyWindow.data

        self.appliedFilterDict = {}
        self.filterCount = 0

        for filter in self.allFilterFrame.findChildren(QLineEdit):
            self.appliedFilterDict[filter.placeholderText()] = filter.text()

            if filter.text() != "":
                self.filterCount += 1
                field = filter.placeholderText()
                value = filter.text()
                df = df[df[field].str.contains(value, case=False)]
                self.populateTable(df)
    
        if self.filterCount == 0:
            self.clearAllFiltersButton.hide()
            self.appliedFilters = None
            self.populateTable(MyWindow.data)
            
        else:
            self.appliedFilters = df
            self.vertical_resize_table_to_content()
            
            if self.clearAllFiltersButton.isHidden():
                self.clearAllFiltersButton.show()


    def quickFilterChanged(self):
        df = self.appliedFilters if self.appliedFilters is not None else MyWindow.data
        quickFilterCount = 0

        for quickFilter in self.quickFilterFrame.findChildren(QLineEdit):
            if quickFilter.text() != "":
                quickFilterCount += 1
                field = quickFilter.placeholderText()
                value = quickFilter.text()
                df = df[df[field].str.contains(value, case=False)]

                self.populateTable(df)

        if quickFilterCount == 0:
            self.quickFilterClearButton.hide()
            self.populateTable(df)
        else:
            self.quickFilterClearButton.show()
            self.vertical_resize_table_to_content()


    def vertical_resize_table_to_content(self):
        suggestedSize = self.table.verticalHeader().sectionSize(0) * self.table.verticalHeader().count() + self.table.horizontalHeader().height() + self.table.horizontalScrollBar().height() + 5

        if self.pageLayout.itemAt(self.pageLayout.count()-1).spacerItem():
            expanded = True
            availableSize = self.table.height()
            
        else:
            expanded = False
            availableSize = self.pageScrollWidget.height() - self.pageLabel.height() - self.pageSubLabel.height() - self.allFilterFrame.height() + 10

        if suggestedSize > availableSize: 
            if expanded:
                self.pageLayout.removeItem(self.pageLayout.itemAt(self.pageLayout.count()-1))
                self.table.setMinimumHeight(300)
                self.table.setMaximumHeight(100000)
        else:

            if not expanded:
                self.pageLayout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

            self.table.setMinimumHeight(suggestedSize)
            self.table.setMaximumHeight(suggestedSize)

        

    def adjust_column_widths(self):

        if self.table.horizontalHeader().count() * 100 < self.table.width():
            self.table.resizeColumnsToContents()

        else:
            for i in range(self.table.horizontalHeader().count()):
                self.table.setColumnWidth(i, 100)



    def quickFilterSettingsClicked(self):
        def positionTop():
            selected = selectedList.selectionModel().selectedRows()
            if selected:
                selected_row = selected[0].row()

                if selected_row > 0:
                    item = selectedModel.takeItem(selected_row)  # Remove the item from the source position
                    selectedModel.insertRow(0, item)  # Insert the item at the destination
                    selectedModel.removeRow(selected_row + 1)
                    index = selectedModel.indexFromItem(item)
                    selectedList.selectionModel().select(index, QItemSelectionModel.SelectionFlag.Select)

        def positionUp():
            selected = selectedList.selectionModel().selectedRows()
            if selected:
                selected_row = selected[0].row()

                if selected_row > 0:
                    item = selectedModel.takeItem(selected_row)  # Remove the item from the source position
                    selectedModel.insertRow(selected_row - 1, item)  # Insert the item at the destination
                    selectedModel.removeRow(selected_row + 1)
                    index = selectedModel.indexFromItem(item)
                    selectedList.selectionModel().select(index, QItemSelectionModel.SelectionFlag.Select)

        def positionDown():
            selected = selectedList.selectionModel().selectedRows()
            if selected:
                selected_row = selected[0].row()

                if selected_row + 1 < selectedModel.rowCount():
                    item = selectedModel.takeItem(selected_row)  # Remove the item from the source position
                    selectedModel.insertRow(selected_row + 2, item)  # Insert the item at the destination
                    selectedModel.removeRow(selected_row)
                    index = selectedModel.indexFromItem(item)
                    selectedList.selectionModel().select(index, QItemSelectionModel.SelectionFlag.Select)

        def positionBottom():
            selected = selectedList.selectionModel().selectedRows()
            if selected:
                selected_row = selected[0].row()

                if selected_row < selectedModel.rowCount():
                    item = selectedModel.takeItem(selected_row)  # Remove the item from the source position
                    selectedModel.appendRow(item)  # Insert the item at the destination
                    selectedModel.removeRow(selected_row)
                    index = selectedModel.indexFromItem(item)
                    selectedList.selectionModel().select(index, QItemSelectionModel.SelectionFlag.Select)


        def addButtonClicked():
            selected = allFieldList.selectedIndexes()

            if selected != []:
                selectedModel.appendRow(QStandardItem(selected[0].data()))
                allModel.removeRow(allFieldList.selectionModel().selectedRows()[0].row())
                removeButton.setEnabled(True)
                removeAllButton.setEnabled(True)

                if selectedModel.rowCount() == 5:
                    addButton.setEnabled(False)
                
        def removeButtonClicked():
            selected = selectedList.selectedIndexes()

            if selected != []:
                allModel.appendRow(QStandardItem(selected[0].data()))
                selectedModel.removeRow(selectedList.selectionModel().selectedRows()[0].row())
                addButton.setEnabled(True)

                if selectedModel.rowCount() == 0:
                    removeButton.setEnabled(False)
                    removeAllButton.setEnabled(False)

        def removeAllButtonClicked():
            row_count = selectedModel.rowCount()
            for _ in range(row_count):
                item = selectedModel.item(0)  # Always get the first item since the list will reduce in size with each iteration
                allModel.appendRow(QStandardItem(item.text()))
                selectedModel.removeRow(0)  

            addButton.setEnabled(True)
            removeButton.setEnabled(False)
            removeAllButton.setEnabled(False)


        popup = QMessageBox(self)
        popup.setWindowTitle("Modify Quick Slicers")
        popup.setStandardButtons(QMessageBox.StandardButton.Apply | QMessageBox.StandardButton.Cancel)
        popup.setDefaultButton(QMessageBox.StandardButton.Cancel)

        popup.setStyleSheet("""
            QMessageBox {   
                background-color: #2f2f2f;
                color: #EEEEEE;
                border:1px solid #3c3c3c;
            }
        """)

        mainFrame = QFrame(popup)
        mainFrame.setStyleSheet("""
            QFrame {   
                background-color: #2f2f2f;
                color: #EEEEEE;
            }
        """)
        pageLayout = QVBoxLayout()
        headerLayout = QVBoxLayout()
        pageLayout.addLayout(headerLayout)
        mainLayout = QHBoxLayout()
        pageLayout.addLayout(mainLayout)

        popupLabel = QLabel(mainFrame)
        popupLabel.setText("Select (5) Quick Slicer fields to display in the sidebar.")
        headerLayout.addWidget(popupLabel)
        headerLayout.addSpacing(10)

        allFieldList = QListView(mainFrame)
        allFieldList.setStyleSheet("""
            QListView {
                background-color: #1f1f1f;
                color: #EEEEEE;
                border-radius: 10px;
                border:1px solid #3c3c3c;
                padding: 5px;                                   
            }
        """)
        mainLayout.addWidget(allFieldList)

        controlFrame = QFrame(mainFrame)
        controlLayout = QVBoxLayout(controlFrame)
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.setSpacing(5)

        controlLayout.addSpacerItem(QSpacerItem(10,10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        addButton = QPushButton(controlFrame)
        addButton.setIcon(QIcon("ui_elements/icons/chevron-right.svg"))
        addButton.setStyleSheet("""
            QPushButton {
                background-color: #1f1f1f;
                color: #EEEEEE;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        addButton.clicked.connect(addButtonClicked)
        addButton.setEnabled(False)
        controlLayout.addWidget(addButton)

        removeButton = QPushButton(controlFrame)
        removeButton.setIcon(QIcon("ui_elements/icons/chevron-left.svg"))
        removeButton.setStyleSheet("""
            QPushButton {
                background-color: #1f1f1f;
                color: #EEEEEE;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        removeButton.clicked.connect(removeButtonClicked)
        controlLayout.addWidget(removeButton)

        removeAllButton = QPushButton(controlFrame)
        removeAllButton.setIcon(QIcon("ui_elements/icons/double-chevron-left-alt.svg"))
        removeAllButton.setStyleSheet("""
            QPushButton {
                background-color: #1f1f1f;
                color: #EEEEEE;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        removeAllButton.clicked.connect(removeAllButtonClicked)
        controlLayout.addWidget(removeAllButton)

        controlLayout.addSpacerItem(QSpacerItem(10,10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        controlFrame.setLayout(controlLayout)
        mainLayout.addWidget(controlFrame)

        selectedList = QListView(mainFrame)
        selectedList.setStyleSheet("""
            QListView {
                background-color: #1f1f1f;
                color: #EEEEEE;
                border-radius: 10px;
                border:1px solid #3c3c3c;
                padding: 5px;
            }
        """)
        mainLayout.addWidget(selectedList)

        positionFrame = QFrame(mainFrame)
        positionLayout = QVBoxLayout(positionFrame)
        positionLayout.setContentsMargins(0, 0, 0, 0)
        positionLayout.setSpacing(0)

        positionLayout.addSpacerItem(QSpacerItem(10,10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        positionTopButton = QPushButton(positionFrame)
        positionTopButton.setIcon(QIcon("ui_elements/icons/double-chevron-up.svg"))
        positionTopButton.clicked.connect(positionTop)
        positionLayout.addWidget(positionTopButton)

        positionUpButton = QPushButton(positionFrame)
        positionUpButton.setIcon(QIcon("ui_elements/icons/chevron-up.svg"))
        positionUpButton.clicked.connect(positionUp)
        positionLayout.addWidget(positionUpButton)

        positionLayout.addSpacing(10)

        positionDownButton = QPushButton(positionFrame)
        positionDownButton.setIcon(QIcon("ui_elements/icons/chevron-down.svg"))
        positionDownButton.clicked.connect(positionDown)
        positionLayout.addWidget(positionDownButton)

        positionBottomButton = QPushButton(positionFrame)
        positionBottomButton.setIcon(QIcon("ui_elements/icons/double-chevron-down.svg"))
        positionBottomButton.clicked.connect(positionBottom)
        positionLayout.addWidget(positionBottomButton)

        positionLayout.addSpacerItem(QSpacerItem(10,10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
    
        mainLayout.addWidget(positionFrame)

        mainFrame.setLayout(pageLayout)
        popup.layout().addWidget(mainFrame, 0, 0, 1, popup.layout().columnCount())

        fields = MyWindow.data.columns.tolist()

        with open(f"default_config/table_map/{self.activeTable}.json", "r") as f:
            activeSlicers = json.load(f)

        allModel = QStandardItemModel()
        allFieldList.setModel(allModel)
        selectedModel = QStandardItemModel()
        selectedList.setModel(selectedModel)

        for field in fields:
            item = QStandardItem(field)
            if field in activeSlicers['slicers']:
                selectedModel.appendRow(item)
            else:
                allModel.appendRow(item)

        allFieldList.setFixedSize(200, 300)
        selectedList.setFixedSize(200, 300)

        if popup.exec() == QMessageBox.StandardButton.Apply:

            fields = [selectedModel.item(row).text() for row in range(selectedModel.rowCount())]
            with open(f"default_config/table_map/{self.activeTable}.json", "r") as f:
                quick_slicers = json.load(f)

            quick_slicers['slicers'] = fields

            with open(f"default_config/table_map/{self.activeTable}.json", "w") as f:
                json.dump(quick_slicers, f)

            self.populateQuickFilters()

        








        
    def clearQuickFilters(self):        
        for child in self.quickFilterFrame.findChildren(QLineEdit):
            child.setText("")

        df = self.appliedFilters if self.appliedFilters is not None else MyWindow.data
        self.populateTable(df)

    def menuComboBoxChanged(self):

        if MyWindow.changes != {}:
            popup = QMessageBox(self)
            popup.setText("You have unsaved changes. Would you like to save them?")
            popup.setWindowTitle("Unsaved Changes")
            popup.setStandardButtons(QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard)
            popup.setDefaultButton(QMessageBox.StandardButton.Save)

            if popup.exec() == QMessageBox.StandardButton.Save:
                self.initiateSave()
            
            MyWindow.changes = {}

        menuSelection = self.menuComboBox.currentText()
        self.activeTable = menuBoxMap[menuSelection]["table"]
        self.menuComboBox.setStyleSheet(style.active_combobox)

        # clear filters
        if self.filterCount > 0:
            self.clearAllFiltersButton.hide()
        if self.allFilterFrame.findChildren(QLineEdit) != []:
            self.collapseAllFilters()

        self.resetAllFilters()

        if self.activeTable is not None:
            self.showLoadingPage()
            MyWindow.data = db.get_cal_programs(self.activeTable)
            self.hideLoadingPage()

            self.pageSubLabel.setText(menuBoxMap[menuSelection]["sub_label"])
            self.pageLabel.adjustSize()
            self.populateTable(MyWindow.data)
            self.pageScrollArea.show()
            self.adjust_column_widths()


            self.populateQuickFilters()
            self.quickFilterFrame.show()
            self.quickFilterSettings.show()



    def showLoadingPage(self):
        self.pageScrollArea.hide()
        self.savedLabel = self.pageLabel.text()
        self.pageLabel.setText("Loading....")
        self.pageLabel.adjustSize()

        QApplication.processEvents()

    def hideLoadingPage(self):
        self.pageScrollArea.show()
        self.pageLabel.setText(self.savedLabel)
        self.pageLabel.adjustSize()



# ------------------------- Main Execution -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())