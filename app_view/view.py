import sys

from app_view.widgets.button_widget import ButtonWidget
from app_view.widgets.combo_box_widget import ComboBoxWidget
from app_view.widgets.frame_widget import FrameWidget
from app_view.widgets.layout_widget import VerticalBox, HorizontalBox
from app_view.widgets.scroll_area_widget import ScrollWidget
from app_view.widgets.splitter_widget import SplitterWidget
from app_view.widgets.label_widget import LabelWidget
from app_view.widgets.line_edit_widget import LineEditWidget
from app_view.widgets.popup_widget import SlicerSettingsPopup
from app_view.style_sheets import button_style, splitter_style, universal_style, combo_box_style, label_style, line_edit_style
from PyQt6.QtWidgets import QMainWindow
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

        # -------------------------------- main page container --------------------------------
        self.main_page = FrameWidget(universal_style.hidden, VerticalBox())
        self.page_splitter.addWidget(self.main_page)
        #self.buildMainPage()       

        # ----------------------------- splitter default position -----------------------------
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
            slicer = LineEditWidget(line_edit_style.input_box, "shabooya")
            slicer.textChanged.connect(slicer_binding)
            self.slicer_container.layout().addWidget(slicer)

        # slicer settings button
        slicer_settings = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/settings.svg"),
                                       fixed_width=26, tool_tip="Slicer Settings")
        slicer_settings.clicked.connect(settings_binding)
        self.slicer_container.layout().addWidget(slicer_settings)


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


    def populate_combo(self, selection: str) -> None:

        # show combo container
        self.combo_container.setVisible(True)

        # get combo options based on navi selection
        navi = navi_map[selection]

        # set combo label and populate dropdown options
        self.combo_label.setText(navi["text"])
        self.combo_box.clear()
        self.combo_box.addItems(navi["options"])


    def populate_slicers(self, fields) -> None:

        # show slicer container
        self.slicer_container.setVisible(True)

        # clear all slicers values
        for slicer, field in zip(self.slicer_container.findChildren(LineEditWidget), fields):
            slicer.setPlaceholderText(field)
            slicer.clear()
    

    def toggle_slicer_visibility(self, active: bool) -> None:

        # update combo box style
        self.slicer_container.setVisible(active)


    def toggle_clear_slicer_visibility(self, active: bool) -> None:

        # update combo box style
        self.clear_slicer_button.setVisible(active)


    def clear_slicers(self) -> None:

        # clear all slicers values
        for slicer in self.slicer_container.findChildren(LineEditWidget):
            slicer.clear()