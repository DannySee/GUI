import sys

from app_view.widgets.button_widget import ButtonWidget
from app_view.widgets.combo_box_widget import ComboBoxWidget
from app_view.widgets.frame_widget import FrameWidget
from app_view.widgets.layout_widget import VerticalBox, HorizontalBox
from app_view.widgets.scroll_area_widget import ScrollWidget
from app_view.widgets.splitter_widget import SplitterWidget
from app_view.widgets.label_widget import LabelWidget
from app_view.widgets.line_edit_widget import LineEditWidget
from app_view.widgets.table_widget import TableWidget
from app_view.widgets.popup_widget import SlicerSettingsPopup
from app_view.style_sheets import button_style, splitter_style, table_style, universal_style, combo_box_style, label_style, line_edit_style, frame_style, scroll_bar_style
from PyQt6.QtWidgets import QMainWindow, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from typing import Protocol
from app_view.ui_map import navi_map, combo_map

DEFAULT_MINIMUM_WIDTH = 200


class Presenter(Protocol):
    def collapser_binding(self) -> None:
        ...
    def navigation_binding(self) -> None:
        ...
    def combo_binding(self) -> None:
        ...
    def slicer_binding(self) -> None:
        ...
    def clear_slicer_binding(self) -> None:
        ...
    def slicer_settings_binding(self) -> None:
        ...
    def expand_filter_binding(self) -> None:
        ...
    def filter_binding(self) -> None:
        ...
    

class View(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 500, 1000, 800)
        self.setWindowTitle("CS Hive")

        
    def init_ui(self, presenter: Presenter) -> None:

        # ------------------------------- application container -------------------------------
        self.app_container = FrameWidget(universal_style.dark_gray, VerticalBox())
        self.setCentralWidget(self.app_container)

        # ---------------------- splitter to separate sidebar main page ----------------------
        self.page_splitter = SplitterWidget(Qt.Orientation.Horizontal, splitter_style.hidden, False)
        self.app_container.layout().addWidget(self.page_splitter)
        
        # -------------------------------------- sidebar --------------------------------------
        
        # sidebar container
        self.sidebar = FrameWidget(universal_style.light_gray_1, VerticalBox(), 
                                                minimum_width=DEFAULT_MINIMUM_WIDTH, 
                                                maximum_width=DEFAULT_MINIMUM_WIDTH+100)
        self.page_splitter.addWidget(self.sidebar)
        
        # sidebar collapser button and spacer to separate collapser button from navigation buttons
        self.construct_sidebar_collapser(self.sidebar.layout(), presenter.collapser_binding)
        self.sidebar.layout().addSpacing(20)

        # sidebar splitter to separate navigation buttons from menu dropdowns
        sidebar_splitter = SplitterWidget(Qt.Orientation.Vertical, splitter_style.visible,False, width=1)
        self.sidebar.layout().addWidget(sidebar_splitter)

        # sidebar navigation  
        self.construct_navigation(sidebar_splitter, presenter.navigation_binding)

        # sidebar menu container
        self.menu = FrameWidget(universal_style.hidden, VerticalBox(content_margins=[10,10,10,10],spacing=5))
        self.menu_scroll_area = ScrollWidget(universal_style.hidden, widget=self.menu)
        sidebar_splitter.addWidget(self.menu_scroll_area)

        # sidebar combo box
        self.construct_combo(self.menu.layout(), presenter.combo_binding)

        # spacing to divide menu from quick-slicers
        self.menu.layout().addSpacing(20)

        # quick slicers
        self.construct_slicers(self.menu.layout(), presenter.slicer_binding, presenter.clear_slicer_binding, 
                               presenter.slicer_settings_binding)

        # stretch to push menu items to top of menu
        self.menu.layout().addStretch()

        # -------------------------------------- page --------------------------------------

        # main page container
        self.main_page = FrameWidget(universal_style.hidden, VerticalBox(spacing=40))
        self.page_splitter.addWidget(self.main_page)

        # banner frame
        self.banner = FrameWidget(universal_style.hidden, HorizontalBox(content_margins=[5,5,5,5], spacing=5), fixed_height=20)
        self.main_page.layout().addWidget(self.banner)

        # page container
        self.page = FrameWidget(universal_style.hidden, VerticalBox(content_margins=[30,0,30,10], spacing=10))
        self.page_scroll_area = ScrollWidget(universal_style.hidden,widget=self.page)
        self.main_page.layout().addWidget(self.page_scroll_area)

        # page header
        self.header = LabelWidget(label_style.header, "Commercial Services Hive")
        self.page.layout().addWidget(self.header)

        # spacer to separate sub header from filters
        self.page.layout().addSpacing(15)

        # sub header and spacer to header from sub header 
        self.sub_header = LabelWidget(label_style.sub_header, "Welcome to the Commercial Services Hive. Please select a navigation option to begin.", visible=False)
        self.page.layout().addWidget(self.sub_header)

        # filters
        self.construct_filters(self.page.layout(), presenter.expand_filter_binding, presenter.filter_binding)

        # data table
        self.table = TableWidget(table_style.table, scroll_bar_style.vertical, scroll_bar_style.horizontal, visible=False)
        self.page.layout().addWidget(self.table)

        # add stretch to push content to top of page
        self.page.layout().addStretch()

        # ----------------------------- splitter default position -----------------------------

        # paget contents take horizontal priority over sidebar
        self.page_splitter.setStretchFactor(0, 0)
        self.page_splitter.setStretchFactor(1, 1)


    # ------------------------------ ui cunstructor functions ------------------------------
    def construct_sidebar_collapser(self, parent: object, binding: callable) -> None:

        # collapse button widget and bind to presenter operation
        self.sidebar_collapser_button = ButtonWidget(button_style.discrete,icon=QIcon("app_view/icons/double-chevron-left.svg"))
        self.sidebar_collapser_button.clicked.connect(binding)

        # create custom layout to push button to right of sidebar and add to parent layout
        sidebar_collapser_layout = HorizontalBox(content_margins=[5,5,5,5])
        sidebar_collapser_layout.addStretch()
        sidebar_collapser_layout.addWidget(self.sidebar_collapser_button)
        parent.addLayout(sidebar_collapser_layout)


    def construct_navigation(self, parent: object, binding: callable) -> None:

        # sidebar navigation container
        self.navigation = FrameWidget(universal_style.hidden,VerticalBox(content_margins=[10,10,10,10],spacing=5))
        self.navi_scroll_area = ScrollWidget(universal_style.hidden,widget=self.navigation,maximum_height=len(navi_map)*40+21)
        parent.addWidget(self.navi_scroll_area)

        # create a button widget for each navigation option, bind, and add to parent layout
        for navi in navi_map:
            navi_button = ButtonWidget(
                button_style.toggle_inactive, 
                icon=navi_map[navi]["icon"], 
                icon_size=[20,20], 
                text=navi_map[navi]["text"], object_name=navi
            )
            navi_button.clicked.connect(binding)
            self.navigation.layout().addWidget(navi_button)
    
    
    def construct_combo(self, parent: object, binding: callable) -> None:

        # sidebar combo container
        self.combo_container = FrameWidget(universal_style.hidden, VerticalBox(spacing=5), visible=False)
        parent.addWidget(self.combo_container)
        
        # combo label
        self.combo_label = LabelWidget(label_style.combo)
        self.combo_container.layout().addWidget(self.combo_label)

        # combo dropdowns
        self.combo_box = ComboBoxWidget(combo_box_style.inactive, "--Select Data--")
        self.combo_box.currentIndexChanged.connect(binding)
        self.combo_container.layout().addWidget(self.combo_box)

        # set combo container height to match content
        self.combo_container.setFixedHeight(self.combo_container.sizeHint().height())


    def construct_slicers(self, parent: object, slicer_binding: callable, clear_binding: callable, 
                          settings_binding: callable, count=5) -> None:

        # slicer container
        self.slicer_container = FrameWidget(universal_style.hidden, VerticalBox(spacing=5), visible=False)
        parent.addWidget(self.slicer_container)

        # dividing spacing & line to separate combo options from quick-slicers
        dividing_line = FrameWidget(universal_style.bright_gray, fixed_height=1)
        self.slicer_container.layout().addWidget(dividing_line)

        # layout to hold label and clear slicer button
        slicer_layout = HorizontalBox()

        # slicer label and stretch separator
        slicer_label = LabelWidget(label_style.slicer, "Quick Slicers")
        slicer_layout.addWidget(slicer_label)
        slicer_layout.addStretch()

        # clear slicer button
        self.clear_slicer_button = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/clear-filter.svg"), visible=False)
        self.clear_slicer_button.clicked.connect(clear_binding)
        slicer_layout.addWidget(self.clear_slicer_button)

        # add slicer layout to container layout
        self.slicer_container.layout().addLayout(slicer_layout)

        # create a slicer widgets, bind, and add to parent layout
        for _ in range(count):
            slicer = LineEditWidget(line_edit_style.input_box)
            slicer.textChanged.connect(slicer_binding)
            self.slicer_container.layout().addWidget(slicer)

        # slicer settings button
        slicer_settings = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/settings.svg"),
                                       fixed_width=26, tool_tip="Slicer Settings")
        slicer_settings.clicked.connect(settings_binding)
        self.slicer_container.layout().addWidget(slicer_settings)

    
    def construct_filters(self, parent: object, expand_filter_binding: callable, clear_binding: callable) -> None:
        
        # filter frame 
        self.filter_frame = FrameWidget(frame_style.filter, VerticalBox(), vertical_size_policy=QSizePolicy.Policy.Minimum, visible=False)
        parent.addWidget(self.filter_frame)

        # header layout 
        header_layout = HorizontalBox(spacing=10)
        self.filter_frame.layout().addLayout(header_layout)

        # expand filter button
        self.expand_filter = ButtonWidget(button_style.filter, text="Filters", icon=QIcon("app_view/icons/chevron-down.svg"))
        self.expand_filter.clicked.connect(expand_filter_binding)
        header_layout.addWidget(self.expand_filter)

        # clear filter button 
        self.clear_filter = ButtonWidget(button_style.filter, text="Clear Filters", icon=QIcon("app_view/icons/clear-filter.svg"), visible=False, fixed_width=100)        
        self.clear_filter.clicked.connect(clear_binding)
        header_layout.addWidget(self.clear_filter)


    # ------------------------------ ui update functions ------------------------------
    def collapse_sidebar(self) -> None:

        # remove text from navigation buttons and resize
        for navi_button in self.navigation.findChildren(ButtonWidget):
            navi_button.setText("")
            navi_button.setMaximumWidth(navi_button.height())
        
        # update combo label to be active navi icon
        #self.combo_label.setText("")

        # get button height and set width to match + content margins (20px)
        sidebar_width = self.navigation.findChild(ButtonWidget).height() + 20
        self.sidebar.setMinimumWidth(sidebar_width)
        self.sidebar.setMaximumWidth(sidebar_width)

        # set sidebar collapser icon
        self.sidebar_collapser_button.setIcon(QIcon("app_view/icons/double-chevron-right.svg"),)


    def expand_sidebar(self) -> None:

        # add text to navigation buttons and resize
        for navi_button in self.navigation.findChildren(ButtonWidget):
            navi_button.setText(navi_map[navi_button.objectName()]["text"])
            navi_button.setMaximumWidth(DEFAULT_MINIMUM_WIDTH + 100)

        # set sidebar height to default 
        self.sidebar.setMinimumWidth(DEFAULT_MINIMUM_WIDTH)
        self.sidebar.setMaximumWidth(DEFAULT_MINIMUM_WIDTH + 100)

        # set sidebar collapser icon
        self.sidebar_collapser_button.setIcon(QIcon("app_view/icons/double-chevron-left.svg"),)


    def toggle_navi_selection(self, selection: object) -> None:

        # set all navigation buttons to inactive style
        for navi_button in self.navigation.findChildren(ButtonWidget):
            navi_button.setStyleSheet(button_style.toggle_inactive)

        # set selected navigation button to active style
        selection.setStyleSheet(button_style.toggle_active)

    
    def toggle_combo_focus(self, active: bool) -> None:

        # update combo box style
        if active:
            self.combo_box.setStyleSheet(combo_box_style.active)
        else:
            self.combo_box.setStyleSheet(combo_box_style.inactive)


    def populate_combo(self, label: str, options: list[str]) -> None:

        # show combo container
        self.combo_container.setVisible(True)

        # set combo label and populate dropdown options
        self.combo_label.setText(label)
        self.combo_box.clear()
        self.combo_box.addItems(options)


    def populate_slicers(self, fields) -> None:

        # show slicer container
        self.slicer_container.setVisible(True)

        # clear all slicers values
        for slicer, field in zip(self.slicer_container.findChildren(LineEditWidget), fields):
            slicer.setPlaceholderText(field)
            slicer.clear()
    

    def toggle_slicer_visibility(self, visible: bool) -> None:

        # update combo box style
        self.slicer_container.setVisible(visible)


    def toggle_clear_slicer_visibility(self, visible: bool) -> None:

        # update combo box style
        self.clear_slicer_button.setVisible(visible)


    def clear_slicers(self) -> None:

        # clear all slicers values
        for slicer in self.slicer_container.findChildren(LineEditWidget):
            slicer.clear()

    
    def update_header(self, text: str) -> None:
        self.header.setText(text)


    def toggle_page_visibility(self, visible: bool) -> None:

        # hide page contents other than header
        self.sub_header.setVisible(visible)
        self.filter_frame.setVisible(visible)
        self.table.setVisible(visible)


    def update_sub_header(self, text: str) -> None:
        self.sub_header.setText(text)