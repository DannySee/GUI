import sys
import data_pull as db
import style_sheets as style

from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFrame,
                             QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QSplitter,
                             QWidget, QScrollArea, QSplitterHandle, QLabel, QTableView, 
                             QStyledItemDelegate, QLineEdit, QComboBox)
from PyQt6.QtGui import QMouseEvent, QIcon
from PyQt6.QtCore import Qt
from PyQt6 import QtCore


class CustomDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            editor.setStyleSheet(style.table)

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
        self.setupcontainer()
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

        self.containerSplitter.setStretchFactor(0, 0)
        self.containerSplitter.setStretchFactor(1, 1)
        self.containerSplitter.setSizes([self.sidebar.minimumWidth(), self.container.width()])
        
        self.sidebarSplitter.setSizes([self.scrollWidget.sizeHint().height(), self.filterWidget.sizeHint().height()])

        self.setCentralWidget(self.container)

    def collapseSidebar(self):  
        if self.containerSplitter.sizes()[0] > 50:
            self.sidebar.setMaximumWidth(50)
            self.sidebar.setMinimumWidth(50)
            self.containerSplitter.setSizes([50, self.container.width()])
            self.collapseButton.setIcon(QIcon("icons/chevron-right.svg"))           
        
            for button in self.scrollWidget.findChildren(QPushButton):
                button.setToolTip(self.teams[button.objectName()]["text"])
                button.setIcon(self.teams[button.objectName()]["icon"])
                button.setText("")
                button.adjustSize()
                button.setStyleSheet(self.getButtonStyleSheet("icon"))
            
            self.scrollLayout.setContentsMargins(0,0,0,0)
            self.scrollLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        else:
            self.collapseButton.setIcon(QIcon("icons/chevron-left.svg"))

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
            self.containerSplitter.setSizes([maxWidth, self.container.width()])


    def setupTableView(self):
        
        df = db.get_cal_programs("CAL_Programs")
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

        self.dataScrollArea.setMaximumWidth(self.table.horizontalHeader().length())
        self.dataSplitter.setMaximumWidth(self.table.horizontalHeader().length())

        self.table.horizontalScrollBar().setStyleSheet(style.horizontal_scrollbar)
        self.table.verticalScrollBar().setStyleSheet(style.vertical_scrollbar)

        self.table.setStyleSheet(style.table)


    def setupSidebarCollapse(self):

        collapsePanel = QFrame(self.sidebar)
        collapsePanel.setStyleSheet(style.hidden)
        collapsePanel.setFixedHeight(35)
        self.sidebarLayout.addWidget(collapsePanel)

        collapseLayout = QHBoxLayout(collapsePanel)
        collapseLayout.setContentsMargins(5,5,5,5)
        collapseLayout.addSpacerItem(QSpacerItem(25,25, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        icon = QIcon("icons/chevron-left.svg")
        self.collapseButton = QPushButton(self.sidebar)
        self.collapseButton.setIcon(icon)
        self.collapseButton.setFixedSize(25,25)
        self.collapseButton.setStyleSheet(style.ui_button)
        self.collapseButton.clicked.connect(self.collapseSidebar)
        collapseLayout.addWidget(self.collapseButton)

        

    def setupcontainer(self):
        self.container = QFrame(self)
        self.container.setStyleSheet(style.dark_gray_frame)
        self.containerLayout = QVBoxLayout(self.container)
        self.containerLayout.setContentsMargins(0,0,0,0)

    def setupSplitter(self):
        self.containerSplitter = QSplitter(Qt.Orientation.Horizontal, self.container)
        self.containerSplitter.setHandleWidth(1)
        self.containerSplitter.setChildrenCollapsible(False)
        self.containerSplitter.setStyleSheet(style.hidden_splitter)
        
        self.containerLayout.addWidget(self.containerSplitter)

    def setupsidebarSplitter(self):
        self.sidebarSplitter = QSplitter(Qt.Orientation.Vertical, self.sidebar)
        self.sidebarSplitter.setChildrenCollapsible(False)
        self.sidebarSplitter.setHandleWidth(1)
        self.sidebarSplitter.setStyleSheet(style.visible_splitter)
        self.sidebarLayout.addWidget(self.sidebarSplitter)

    def setupSidebar(self):
        self.sidebar = QFrame(self.containerSplitter)
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        
        self.sidebar.setStyleSheet(style.light_gray_frame)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(0,0,0,0)

    def setupFilters(self):
        self.filterArea = QScrollArea(self.sidebarSplitter)
        self.filterArea.setWidgetResizable(True)
        self.filterArea.setStyleSheet(style.hidden)


        self.filterWidget = QWidget(self.filterArea)
        self.filterWidget.setStyleSheet(style.hidden)

        self.filterLayout = QVBoxLayout(self.filterWidget)
        self.filterLayout.setSpacing(4)
        self.filterLayout.setContentsMargins(10,10,10,10)
        

        self.filterArea.setWidget(self.filterWidget)
        self.filterArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.filterArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.filterArea.setMinimumHeight(100)


        self.filterLabel = QLabel(self.filterWidget)
        self.filterLabel.setText("")
        self.filterLabel.setStyleSheet(style.sidebar_label)
                                       
        self.filterLayout.addWidget(self.filterLabel)
        self.filterLayout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # make the combobox flat
        self.combobox = QComboBox(self.filterWidget)
        self.combobox.setStyleSheet(style.combobox)
        self.filterLayout.addWidget(self.combobox)
        self.combobox.setVisible(False)

        self.filterLayout.addSpacerItem(QSpacerItem(20,20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))


        self.horizontalLine = QFrame(self.filterWidget)
        self.horizontalLine.setFrameShape(QFrame.Shape.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLine.setStyleSheet(style.dividing_line)
        self.horizontalLine.setLineWidth(1)
        self.horizontalLine.setFixedHeight(1)

        self.filterLayout.addWidget(self.horizontalLine)

        self.filterLayout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))




    


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
                df = db.get_cal_programs(table_name)
                model = TableModel(df)
                self.table.setModel(model)

                self.tableLoaded()




    def setupDataFrame(self):
        
        self.dataFrame = QFrame(self.containerSplitter)
        self.dataFrame.setMinimumWidth(200)
        self.dataFrame.setStyleSheet(style.hidden)

        dataFrameLayout = QVBoxLayout(self.dataFrame)
        dataFrameLayout.setContentsMargins(50,20,50,20)

        self.dataFrameBanner = QFrame(self.dataFrame)
        self.dataFrameBanner.setStyleSheet(style.hidden)
        self.dataFrameBanner.setFixedHeight(50)
        dataFrameLayout.addWidget(self.dataFrameBanner)

        self.dataFrameHeader = QFrame(self.dataFrame)
        self.dataFrameHeader.setStyleSheet(style.hidden)
        self.dataFrameHeader.setFixedHeight(50)
        dataFrameLayout.addWidget(self.dataFrameHeader)

        self.pageLabel = QLabel(self.dataFrameHeader)
        self.pageLabel.setStyleSheet(style.page_label)

        self.tablViewPane = QFrame(self.dataFrame)
        self.dataFrameBanner.setStyleSheet(style.hidden)
        dataFrameLayout.addWidget(self.tablViewPane)

        self.dataSplitter = QSplitter(Qt.Orientation.Vertical, self.tablViewPane)
        self.dataSplitter.setHandleWidth(1)
        self.dataSplitter.setChildrenCollapsible(False)
        self.dataSplitter.setStyleSheet(style.hidden_splitter)
        dataFrameLayout.addWidget(self.dataSplitter)


        self.dataScrollArea = QScrollArea(self.dataSplitter)
        self.dataScrollArea.setWidgetResizable(True)
        self.dataScrollArea.setStyleSheet(style.hidden)

        self.dataScrollArea2 = QScrollArea(self.dataSplitter)
        self.dataScrollArea2.setWidgetResizable(True)
          
        self.dataScrollArea2.setStyleSheet(style.hidden)


    def setupScrollArea(self):
        self.scrollArea = QScrollArea(self.sidebarSplitter)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet(style.hidden)

        self.scrollWidget = QWidget(self.scrollArea)
        self.scrollWidget.setStyleSheet(style.hidden)

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
        button.setStyleSheet(self.getButtonStyleSheet("text"))
        button.clicked.connect(self.onButtonClicked)
        self.scrollLayout.addWidget(button)


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
