import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFrame,
                             QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QSplitter,
                             QWidget, QScrollArea, QSplitterHandle, QLabel, QTableView, 
                             QStyledItemDelegate, QHeaderView, QAbstractItemView, QLineEdit,
                             QStyle, QComboBox, QGraphicsDropShadowEffect, QDialog, QProgressBar)
from PyQt6.QtGui import QFont, QMouseEvent, QIcon, QPalette, QPainter, QColor
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6 import QtCore
import data_pull as db

import time



class CustomComboBox(QComboBox):
    def showPopup(self):
        super().showPopup()
        # Ensure no item gets the focus when the popup is shown
        self.view().setCurrentIndex(QtCore.QModelIndex())


class CustomDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            editor.setFont(QFont("Microsoft Sans Serif", 8))
            palette = editor.palette()
            palette.setColor(QPalette.ColorRole.Text, QColor("#BABABA"))
            editor.setPalette(palette)

            value = index.data(Qt.ItemDataRole.EditRole) or index.data(Qt.ItemDataRole.DisplayRole)
            editor.setText(value)
            
            
            index.model().setData(index, "", Qt.ItemDataRole.EditRole)
        return editor
    
    def setEditorData(self, editor, index):
        if not isinstance(editor, QLineEdit):
            super().setEditorData(editor, index)

    
    def setModelData(self, editor, model, index):
        if isinstance(editor, QLineEdit):
            model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)
        else:
            super().setModelData(editor, model, index)
           

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
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])


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
        
        self.sidebarSplitter.setSizes([self.scrollWidget.sizeHint().height(), self.filterWidget.sizeHint().height()])

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

            maxWidth = max(self.scrollWidget.sizeHint().width(), self.filterWidget.sizeHint().width())

            self.sidebar.setMinimumWidth(maxWidth)
            self.sidebar.setMaximumWidth(maxWidth+100)
            self.splitter.setSizes([maxWidth, self.mainFrame.width()])


    def setupTableView(self):
        
        df = db.get_cal_programs()
        df.fillna("", inplace=True)

        

        self.table = QTableView(self.dataScrollArea)
        self.delegate = CustomDelegate(self.table)
        self.table.setItemDelegate(self.delegate)
    

        model = TableModel(df)
        self.table.setModel(model)

        

        self.dataScrollLayout = QVBoxLayout(self.dataScrollArea)
        self.dataScrollLayout.setSpacing(4)
        self.dataScrollLayout.setContentsMargins(10,10,10,10)
        self.dataScrollLayout.addWidget(self.table)
        

        self.dataScrollArea.setWidget(self.table)

 
        #self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        #self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        #self.dataScrollArea.setMaximumWidth(self.table.horizontalHeader().length())
        #self.dataSplitter.setMaximumWidth(self.table.horizontalHeader().length())
        
        self.dataScrollArea.setMaximumWidth(self.table.horizontalHeader().length())
        self.dataSplitter.setMaximumWidth(self.table.horizontalHeader().length())

        self.table.horizontalScrollBar().setStyleSheet("""
            QScrollBar:horizontal {
                background: #1f1f1f;
                height: 15px;
                border: none;
                margin: 0 15px; /* Adjust spacing for the left and right arrows */
            }
            QScrollBar::add-line:horizontal {
                border: none;
                width: 15px; /* Adjust width as required */
                subcontrol-position: right;
                subcontrol-origin: margin;
                background: #3c3c3c; /* Background color for the button */
            }
            QScrollBar::sub-line:horizontal {
                border: none;
                width: 15px; /* Adjust width as required */
                subcontrol-position: left;
                subcontrol-origin: margin;
                background: #3c3c3c; /* Background color for the button */
            }
            QScrollBar::handle:horizontal {
                background: #3c3c3c;
                border: none;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #555555;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: #2f2f2f;
            }
            QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal {
                border: none;
                width: 7px;
                height: 7px;
                background: #555555;
            }
            QScrollBar::right-arrow:horizontal:hover, QScrollBar::left-arrow:horizontal:hover {
                background: #777777;
            }
        """)



        self.table.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {
                background: #1f1f1f;
                width: 15px;
                border: none;
                margin: 15px 0; /* Adjust spacing for the top and bottom arrows */
            }
            QScrollBar::add-line:vertical {
                border: none;
                height: 15px; /* Adjust height as required */
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                background: #3c3c3c; /* Background color for the button */
            }
            QScrollBar::sub-line:vertical {
                border: none;
                height: 15px; /* Adjust height as required */
                subcontrol-position: top;
                subcontrol-origin: margin;
                background: #3c3c3c; /* Background color for the button */
            }
            QScrollBar::handle:vertical {
                background: #3c3c3c;
                border: none;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #555555;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #2f2f2f;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: none;
                width: 7px;
                height: 7px;
                background: #555555;
            }
            QScrollBar::up-arrow:vertical:hover, QScrollBar::down-arrow:vertical:hover {
                background: #777777;
            }
        """)

        self.table.setStyleSheet("""
            QTableView {
                background-color: #1f1f1f;
                color: #BABABA;
                gridline-color: #333333;
            }
            
            QTableView::item {
                background-color: #1f1f1f;
                color: #BABABA;
                border: none;
            }

            QHeaderView::section {
                background-color: #1f1f1f;
                color: #BABABA;
                border: 1px solid #333333;
                border-left: none;
                border-top: none;
            }

            QTableView::horizontal {
                border-left: 1px solid #333333;
            }

            QTableView::vertical {
                border-top: 1px solid #333333;
                border-left: 1px solid #333333;                
            }
            QTableView QTableCornerButton::section {
                background-color: #1f1f1f;
                border-top : none;
                border-left: none;
                border-right: 1px solid #333333;
                border-bottom: 1px solid #333333;  
            }
                                 
        """)

        #self.table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)

        



                










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
        self.filterLayout.setContentsMargins(10,10,10,10)
        

        self.filterArea.setWidget(self.filterWidget)
        self.filterArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.filterArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.filterArea.setMinimumHeight(100)


        self.filterLabel = QLabel(self.filterWidget)
        self.filterLabel.setFont(QFont("Microsoft Sans Serif", 14, QFont.Weight.Bold))
        self.filterLabel.setText("")
        self.filterLabel.setStyleSheet("""
            QLabel {
                padding: 20px 0px 0px 0px;
                color: #EEEEEE;
                background-color: transparent;
            }
        """)
                                       
        self.filterLayout.addWidget(self.filterLabel)
        self.filterLayout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # make the combobox flat
        self.combobox = CustomComboBox(self.filterWidget)
        self.combobox.setFont(QFont("Microsoft Sans Serif", 11))
        self.combobox.setStyleSheet("""
            QComboBox {
                background-color: #181818;
                border: none;
                border-radius: 4px;
                padding: 8px;
                min-width: 6em;
                color: #BDBDBD;
            }
            QComboBox::drop-down {
                width: 30px;
                border-left: none;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }
            QComboBox::down-arrow {
                image: url(icons/menu-down.svg);
            }
            QComboBox:editable {
                background: #181818;    
            }
            QComboBox QAbstractItemView {
                color: #BDBDBD;
                padding:  0px 8px 0px 8px ;
                border: 1px solid #333333;
                border-radius: 4px;
            }
            QComboBox QAbstractItemView::item {
                color: #BDBDBD;
                padding: 6px;
            }

                      
        """)
        self.filterLayout.addWidget(self.combobox)
        self.combobox.setVisible(False)

        self.filterLayout.addSpacerItem(QSpacerItem(20,20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))


        self.horizontalLine = QFrame(self.filterWidget)
        self.horizontalLine.setFrameShape(QFrame.Shape.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLine.setStyleSheet("background-color: #3c3c3c; border: none; padding: 10px;")
        self.horizontalLine.setLineWidth(1)
        self.horizontalLine.setFixedHeight(1)

        self.filterLayout.addWidget(self.horizontalLine)

        self.filterLayout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))




    def setupComboBox(self, activeTables):


        
        if self.combobox.count() > 0: 
            self.combobox.currentIndexChanged.disconnect(self.onComboBoxChanged)
            self.combobox.clear()
        else:
            self.combobox.setVisible(True)
            

        self.combobox.addItems(activeTables)
        self.combobox.setCurrentIndex(0)
        self.combobox.currentIndexChanged.connect(self.onComboBoxChanged)
        


    def loadingTable(self):

        self.table.hide()
        self.textLabel = self.pageLabel.text()
        self.pageLabel.setText("Loading....")
        
        #process events
        QApplication.processEvents()


    def tableLoaded(self):

        self.table.isVisible = True
        self.table.show()
        self.pageLabel.setText(self.textLabel)



    def onComboBoxChanged(self):

        if self.combobox.currentText() != "" :
            if self.tableLookup[self.combobox.currentText()] is not None:

                self.loadingTable()
                
                table_name = self.tableLookup[self.combobox.currentText()]
                df = db.pull_records(table_name)
                model = TableModel(df)
                self.table.setModel(model)

                self.tableLoaded()




    def setupDataFrame(self):
        
        self.dataFrame = QFrame(self.splitter)
        self.dataFrame.setMinimumWidth(200)
        self.dataFrame.setStyleSheet("background-color: transparent; border: none;")

        dataFrameLayout = QVBoxLayout(self.dataFrame)
        dataFrameLayout.setContentsMargins(50,20,50,20)

        self.dataFrameBanner = QFrame(self.dataFrame)
        self.dataFrameBanner.setStyleSheet("background-color: transparent; border: none;")
        self.dataFrameBanner.setFixedHeight(50)
        dataFrameLayout.addWidget(self.dataFrameBanner)


        #self.b1 = QPushButton("Button 1", self.dataFrameBanner)
        #self.b1.setObjectName("btn1")
        #self.b1.setFont(QFont("Microsoft Sans Serif", 11))
        #self.b1.setStyleSheet(self.getButtonStyleSheet("text"))
        #self.b1.clicked.connect(self.printDF)




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

        self.tablViewPane = QFrame(self.dataFrame)
        self.dataFrameBanner.setStyleSheet("background-color: transparent; border: none;")
        dataFrameLayout.addWidget(self.tablViewPane)

        self.dataSplitter = QSplitter(Qt.Orientation.Vertical, self.tablViewPane)
        self.dataSplitter.setHandleWidth(1)
        self.dataSplitter.setChildrenCollapsible(False)
        self.dataSplitter.setStyleSheet("QSplitter::handle {background-color: transparent; border: none; color: #3c3c3c;}")
        dataFrameLayout.addWidget(self.dataSplitter)


        self.dataScrollArea = QScrollArea(self.dataSplitter)
        self.dataScrollArea.setWidgetResizable(True)
        
        self.dataScrollArea.setStyleSheet("background-color: transparent; border: none;")

        self.dataScrollArea2 = QScrollArea(self.dataSplitter)
        self.dataScrollArea2.setWidgetResizable(True)
          
        self.dataScrollArea2.setStyleSheet("background-color: transparent; border: none;")


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


    #def printDF(self):

        #print(self.table.model()._data)


    def setupSidebarButtons(self):

        self.teams = {
            "btnSMS": {
                "text":"SMS & Costing",
                "icon":QIcon("icons/sms_costing.svg"),
                "tables":{
                    "SMS Agreements": "SMS_Agreements",
                    "Costing": "Costing"
                }
            },
            "btnCAD": {
                "text":"Customer Disputes",
                "icon":QIcon("icons/customer_disputes.svg"),
                "tables":{
                    "Audit History": None,
                    "Account Assignments": "CAL_Account_Assignments",
                }
            },
            "btnCIR": {
                "text":"Customer Incentives",
                "icon":QIcon("icons/customer_incentives.svg"), 
                "tables": {
                    "REBA Tracker": None,
                    "Agreements": None,
                }
            },
            "btnDPM": {
                "text":"Deviated Agreements",
                "icon":QIcon("icons/deviated_agreements.svg"),
                "tables": {
                    "DPM Agreements": "CAL_Programs",
                    "Customer Profile": "CAL_Customer_Profile",
                    "Deviation Loads": "CAL_Deviation_Loads",
                    "Account Assignments": "CAL_Account_Assignments",
                    "Org Chart": "UL_Org"
                }
            },
            "btnUSDA": {
                "text":"USDA Agreements",
                "icon":QIcon("icons/usda.svg"),
                "tables": {
                    "Agreements": None,
                    "Bot Tracker": None
                }
            },
            "btnQA": {
                "text":"Quality Assurance",
                "icon":QIcon("icons/quality_assurance.svg"),
                "tables": {
                    "Metrics Agreement": "Dash_Agreement",
                    "Metrics Inquiry": "Dash_Inquiry",
                    "Metrics Price Rule": "Dash_PriceRule",
                    "Price Rule Tracker": "PR_Master"
                }
            }
        }

        self.tableLookup = {
            "SMS Agreements": None,
            "Costing": None,
            "Audit History": None,
            "Account Assignments": "CAL_Account_Assignments",
            "REBA Tracker": None,
            "DPM Agreements": "CAL_Programs",
            "Customer Profile": "CAL_Customer_Profile",
            "Deviation Loads": "CAL_Deviation_Loads",
            "Agreements": None,
            "Bot Tracker": None,
            "Metrics Agreement": "Dash_Agreement",
            "Metrics Inquiry": "Dash_Inquiry",
            "Metrics Price Rule": "Dash_PriceRule",
            "Price Rule Tracker": "PR_Master",
            "Org Chart": "UL_Org"
        }
        
        for team in self.teams:
            self.createButton(team, self.teams[team]["text"])

        footerSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
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

        self.filterLabel.setText(self.teams[clickedButton.objectName()]["text"])
        self.setupComboBox(self.teams[clickedButton.objectName()]["tables"].keys())
        

        maxWidth = max(self.scrollWidget.sizeHint().width(), self.filterWidget.sizeHint().width())

        if maxWidth > self.sidebar.width():

            self.sidebar.setMinimumWidth(maxWidth)
            self.sidebar.setMaximumWidth(maxWidth+100)

            self.splitter.setSizes([maxWidth, self.mainFrame.width()])
        
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
