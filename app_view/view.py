import sys
import pandas as pd  

from app_view.widgets.button_widget import ButtonWidget
from app_view.widgets.combo_box_widget import ComboBoxWidget
from app_view.widgets.frame_widget import FrameWidget
from app_view.widgets.layout_widget import VerticalBox, HorizontalBox, Grid
from app_view.widgets.scroll_area_widget import ScrollWidget, NoScrollWidget
from app_view.widgets.splitter_widget import SplitterWidget
from app_view.widgets.label_widget import LabelWidget
from app_view.widgets.line_edit_widget import LineEditWidget
from app_view.widgets.table_widget import TableWidget
from PyQt6.QtWidgets import QMainWindow, QSizePolicy
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from typing import Protocol
from app_view.ui_map import navi_map, combo_map
from app_view.style_sheets import (button_style, splitter_style, table_style, universal_style, 
                                   combo_box_style, label_style, line_edit_style, frame_style, scroll_bar_style)


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
    def save_binding(self) -> None:
        ...
    def import_binding(self) -> None:
        ...
    def export_binding(self) -> None:
        ...
    def filter_toggle_binding(self) -> None:
        ...
    def clear_filter_binding(self) -> None:
        ...
    def filter_binding(self) -> None:
        ...
    def refresh_binding(self) -> None:
        ...
    def toolbox_binding(self) -> None:
        ...
    

class View(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 500, 1000, 800)
        self.setWindowTitle("CS Hive")

        
    def init_ui(self, presenter: Presenter) -> None:

        # ------------------------------- application container -------------------------------
        self.app_container = FrameWidget(universal_style.dark_gray, VerticalBox(alignment=None))
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

        # sidebar splitter to separate navigation buttons from menu dropdowns
        self.sidebar_splitter = SplitterWidget(Qt.Orientation.Vertical, splitter_style.visible,False, width=1)
        self.sidebar.layout().addWidget(self.sidebar_splitter)

        # sidebar navigation  
        self.construct_navigation(self.sidebar_splitter, presenter.navigation_binding)

        # sidebar menu box
        self.menu = FrameWidget(universal_style.hidden, VerticalBox(content_margins=[10,10,10,10],spacing=5))
        self.menu_scroll_area = ScrollWidget(universal_style.hidden, widget=self.menu)
        self.sidebar_splitter.addWidget(self.menu_scroll_area)

        # sidebar menu items
        self.construct_menu(self.menu.layout(), presenter.combo_binding, presenter.toolbox_binding)

        # quick slicers
        self.construct_slicers(self.menu.layout(), presenter.slicer_binding, presenter.clear_slicer_binding, 
                               presenter.slicer_settings_binding)

        # -------------------------------------- page --------------------------------------

        # main page container
        self.main_page = FrameWidget(universal_style.hidden, VerticalBox())
        self.page_splitter.addWidget(self.main_page)

        # toolbar 
        self.construct_toolbar(self.main_page.layout(), presenter.save_binding, presenter.import_binding, presenter.export_binding)

        # page container
        self.page = FrameWidget(universal_style.hidden, VerticalBox(content_margins=[30,40,30,30], spacing=10))
        self.page_scroll_area = ScrollWidget(universal_style.hidden,widget=self.page)
        self.main_page.layout().addWidget(self.page_scroll_area)

        # landing page
        self.construct_landing_page(self.page.layout())

        # page header
        self.header = LabelWidget(label_style.header)
        self.page.layout().addWidget(self.header)

        # spacer to separate sub header from filters
        self.page.layout().addSpacing(15)

        # sub header and spacer to header from sub header 
        self.construct_sub_header(self.page.layout(), presenter.refresh_binding)

        # filters
        self.construct_filters(self.page.layout(), presenter.filter_toggle_binding, presenter.clear_filter_binding)

        # data table
        self.table = TableWidget(table_style.table, scroll_bar_style.table_vertical, scroll_bar_style.table_horizontal, visible=False)
        self.page.layout().addWidget(self.table)

        # hidden table container for loading/mid page purposes
        self.construct_page_placeholder(self.page.layout())

        # status bar 
        self.construct_status_bar(self.main_page.layout())

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
        sidebar_collapser_layout = HorizontalBox(content_margins=[5,5,5,5], alignment=Qt.AlignmentFlag.AlignRight)
        sidebar_collapser_layout.addWidget(self.sidebar_collapser_button)
        parent.addLayout(sidebar_collapser_layout)

        # create spacer
        parent.addSpacing(20)



    def construct_navigation(self, parent: object, binding: callable) -> None:

        # sidebar navigation container
        self.navigation = FrameWidget(universal_style.hidden,VerticalBox(content_margins=[10,10,10,10],spacing=5), minimum_width=10)
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
    
    
    def construct_menu(self, parent: object, combo_binding: callable, toobox_binding: callable) -> None:

        # sidebar combo container
        self.menu_container = FrameWidget(universal_style.hidden, vertical_size_policy=QSizePolicy.Policy.Fixed,visible=False,
                                          layout=VerticalBox(content_margins=[0,20,0,10], spacing=5), minimum_width=10)
        parent.addWidget(self.menu_container)

        # combo label
        self.combo_label = LabelWidget(label_style.combo)
        self.menu_container.layout().addWidget(self.combo_label)

        # disabled button to hold collapsed combo icon
        self.combo_icon = ButtonWidget(button_style.combo, visible=False, icon_size=[20,20], fixed_width=36)
        self.menu_container.layout().addWidget(self.combo_icon)
        self.menu_container.layout().addSpacing(5)

        # combo dropdowns
        self.combo_box = ComboBoxWidget(combo_box_style.inactive, "--Select Data--")
        self.combo_box.currentIndexChanged.connect(combo_binding)
        self.menu_container.layout().addWidget(self.combo_box)

        # toolbox button 
        self.toolbox_button = ButtonWidget(button_style.toggle_inactive, "Toolbox", icon=QIcon("app_view/icons/toolbox.svg"), icon_size=[20,20])
        self.toolbox_button.clicked.connect(toobox_binding)
        self.menu_container.layout().addWidget(self.toolbox_button)

        # toolbox container
        self.toolbox_container = FrameWidget(universal_style.generic_border_pane, VerticalBox(content_margins=[5,5,5,5],spacing=5), visible=False)
        self.menu_container.layout().addWidget(self.toolbox_container)

        # dividing line
        self.menu_container.layout().addSpacing(10)
        self.dividing_line = FrameWidget(universal_style.bright_gray, fixed_height=1)
        self.menu_container.layout().addWidget(self.dividing_line)


    def construct_slicers(self, parent: object, slicer_binding: callable, clear_binding: callable, 
                          settings_binding: callable, count=5) -> None:

        # slicer container
        self.slicer_container = FrameWidget(universal_style.hidden, VerticalBox(spacing=5), 
                                            visible=False, vertical_size_policy=QSizePolicy.Policy.Maximum)
        parent.addWidget(self.slicer_container)

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

    
    def construct_toolbar(self, parent: object, save_binding: callable, import_binding: callable, export_binding: callable) -> None:

        # create toolbar container
        self.toolbar = FrameWidget(frame_style.toolbar, 
                                   HorizontalBox(content_margins=[5,2,5,2], spacing=2,alignment=Qt.AlignmentFlag.AlignLeft), 
                                   vertical_size_policy=QSizePolicy.Policy.Maximum)
        parent.addWidget(self.toolbar)

        # save button
        self.save_button = ButtonWidget(button_style.toolbar, text="Save", enabled=False)
        self.save_button.clicked.connect(save_binding)
        self.toolbar.layout().addWidget(self.save_button)

        # export button
        self.export_button = ButtonWidget(button_style.toolbar, text="Export")
        self.export_button.clicked.connect(export_binding)
        self.toolbar.layout().addWidget(self.export_button)

        # import button
        self.import_button = ButtonWidget(button_style.toolbar, text="Import")
        self.import_button.clicked.connect(import_binding)
        self.toolbar.layout().addWidget(self.import_button)


    def construct_landing_page(self, parent: object) -> None:

        # landing page container
        self.landing_page = FrameWidget(universal_style.hidden, VerticalBox(alignment=Qt.AlignmentFlag.AlignCenter))
        parent.addWidget(self.landing_page)

        # frame to hold icon
        frame = FrameWidget(universal_style.generic_border_pane_transparent, VerticalBox(content_margins=[50,50,50,50],spacing=10, alignment=Qt.AlignmentFlag.AlignCenter),
                            vertical_size_policy=QSizePolicy.Policy.Fixed, horizontal_size_policy=QSizePolicy.Policy.Fixed)
        self.landing_page.layout().addWidget(frame)

        # create hive image parameters
        max_width = 280
        width = 160
        over_the_hump = False

        # loop to create 6 segments
        for _ in range(6):

            # create frame object and add to layout
            layout = HorizontalBox(alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(FrameWidget(universal_style.hive_segments, fixed_height=40, fixed_width=width))
            frame.layout().addLayout(layout)

            # increment/decrement width
            width = width - 40 if over_the_hump else width + 40
            if width == max_width: over_the_hump = True

        
    def construct_filters(self, parent: object, fitler_toggle_binding: callable, clear_filter_binding: callable) -> None:
        
        # filter frame 
        self.filter_container = FrameWidget(frame_style.filter, VerticalBox(), vertical_size_policy=QSizePolicy.Policy.Minimum, visible=False)
        parent.addWidget(self.filter_container)

        # header layout 
        header_layout = HorizontalBox(spacing=10)
        self.filter_container.layout().addLayout(header_layout)

        # expand filter button
        self.filter_toggle = ButtonWidget(button_style.filter, text="Filters", icon=QIcon("app_view/icons/chevron-down.svg"))
        self.filter_toggle.clicked.connect(fitler_toggle_binding)
        header_layout.addWidget(self.filter_toggle)

        # clear filter button 
        self.clear_filter = ButtonWidget(button_style.clear_filter, text="Clear Filters", 
                                         icon=QIcon("app_view/icons/clear-filter.svg"), 
                                         visible=False, fixed_width=120)        
        self.clear_filter.clicked.connect(clear_filter_binding)
        header_layout.addWidget(self.clear_filter)


    def construct_sub_header(self, parent: object, refresh_binding: callable) -> None:

        # sub header layout
        self.sub_header_container = FrameWidget(universal_style.hidden, HorizontalBox(), visible=False, 
                                                vertical_size_policy=QSizePolicy.Policy.Maximum)
        parent.addWidget(self.sub_header_container)

        # sub header label 
        self.sub_header = LabelWidget(label_style.sub_header)
        self.sub_header_container.layout().addWidget(self.sub_header)

        # add strech to separate label from 
        self.sub_header_container.layout().addStretch()

        # refresh timestamp 
        self.refresh = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/refresh.svg"), tool_tip="Refresh")
        self.refresh.clicked.connect(refresh_binding)
        self.sub_header_container.layout().addWidget(self.refresh)


    def construct_page_placeholder(self, parent: object) -> None:

        # loading container
        self.page_placeholder = FrameWidget(universal_style.hidden, VerticalBox(spacing=10, alignment=Qt.AlignmentFlag.AlignCenter), visible=False)
        parent.addWidget(self.page_placeholder)

        # add spacer
        self.page_placeholder.layout().addSpacing(6)

        # sub header 
        ph_sub_header_layout = HorizontalBox()
        ph_sub_header_label = FrameWidget(frame_style.loader_bright, fixed_height=20, maximum_width=400)
        ph_sub_header_layout.addWidget(ph_sub_header_label)
        ph_sub_header_layout.addStretch()
        ph_sub_header_button = FrameWidget(frame_style.loader_bright, fixed_height=20, maximum_width=160)
        ph_sub_header_layout.addWidget(ph_sub_header_button)
        self.page_placeholder.layout().addLayout(ph_sub_header_layout)

        # filters
        ph_filters = FrameWidget(frame_style.loader_light, VerticalBox([10,0,10,0], alignment=Qt.AlignmentFlag.AlignCenter), fixed_height=38)
        self.page_placeholder.layout().addWidget(ph_filters)
        ph_filters_layout = HorizontalBox()
        ph_filter_label = FrameWidget(frame_style.loader_bright, fixed_height=20, maximum_width=300)
        ph_filters_layout.addWidget(ph_filter_label)
        ph_filters_layout.addStretch()
        ph_filter_button = FrameWidget(frame_style.loader_bright, fixed_height=20, maximum_width=220)
        ph_filters_layout.addWidget(ph_filter_button)
        ph_filters.layout().addLayout(ph_filters_layout)

        # table
        ph_table = FrameWidget(universal_style.hidden, VerticalBox([20,20,20,20], spacing=20, alignment=Qt.AlignmentFlag.AlignTop))
        ph_table_scroll = NoScrollWidget(universal_style.generic_border_pane, widget=ph_table, minimum_height=100)
        self.page_placeholder.layout().addWidget(ph_table_scroll)

        # table contents
        padding = True
        rows = self.height() // 40
        for _ in range(rows):
            if padding:
                row_layout = HorizontalBox(alignment=Qt.AlignmentFlag.AlignLeft)
                row_layout.addSpacing(40)
                ph_row = FrameWidget(frame_style.loader_bright, fixed_height=20)
                row_layout.addWidget(ph_row)
                row_layout.addSpacing(40)
                ph_table.layout().addLayout(row_layout)
                padding = False
            else:
                ph_row = FrameWidget(frame_style.loader_bright, fixed_height=20)
                ph_table.layout().addWidget(ph_row)
                padding = True
    

    def construct_status_bar(self, parent: object) -> None:

        # status bar container
        status_container = FrameWidget(frame_style.status_bar, HorizontalBox(), fixed_height=25)
        parent.addWidget(status_container)

        # status bar
        self.status_bar = FrameWidget(universal_style.hidden, visible=False,
                                      layout=HorizontalBox(content_margins=[20,2,20,2], spacing=10, alignment=Qt.AlignmentFlag.AlignRight))
        status_container.layout().addWidget(self.status_bar)

        # status message
        self.status_indicator = LabelWidget(label_style.indicator_neutral, fixed_width=14, fixed_height=14)
        self.status_bar.layout().addWidget(self.status_indicator)
        self.save_status = LabelWidget(label_style.status, "No Changes")
        self.status_bar.layout().addWidget(self.save_status)

        # add stretch to center status message 
        self.status_bar.layout().addStretch()

        # table info
        self.table_status = LabelWidget(label_style.status)
        self.status_bar.layout().addWidget(self.table_status)

        # add divinding line to separate table status from refresh state
        dividing_line = FrameWidget(universal_style.bright_gray, fixed_width=1)
        self.status_bar.layout().addWidget(dividing_line)
 
         # refresh state
        self.refresh_state = LabelWidget(label_style.status)
        self.status_bar.layout().addWidget(self.refresh_state)
     

    # ------------------------------ ui update functions ------------------------------
    def collapse_sidebar(self) -> None:

        # get collapsed sidebar width
        sidebar_width = self.navigation.findChild(ButtonWidget).height() + 20

        # adjust navigation width and remove text 
        self.navigation.setMaximumWidth(sidebar_width)
        for navi_button in self.navigation.findChildren(ButtonWidget):
            navi_button.setText("")

        # adjust menu width and remove text/visibility
        self.menu_container.setMaximumWidth(sidebar_width - 20)
        self.combo_label.setVisible(False)
        self.combo_icon.setVisible(True)
        self.toolbox_button.setText("")

        # hide slicer container
        self.toggle_slicer_visibility(False)

        # set sidebar collapser icon
        self.sidebar_collapser_button.setIcon(QIcon("app_view/icons/double-chevron-right.svg"),)

        # adjust sidebar and splitter width
        self.sidebar.setMinimumWidth(sidebar_width)
        self.sidebar.setMaximumWidth(sidebar_width)
        self.page_splitter.setSizes([sidebar_width, self.width() - sidebar_width])


    def expand_sidebar(self) -> None:

        # adjust navigation width and add text 
        self.navigation.setMaximumWidth(DEFAULT_MINIMUM_WIDTH + 100)
        for navi_button in self.navigation.findChildren(ButtonWidget):
            navi_button.setText(navi_map[navi_button.objectName()]["text"])

        # adjust menu width and add text/visibility
        self.menu_container.setMaximumWidth(DEFAULT_MINIMUM_WIDTH + 1000)
        self.combo_label.setVisible(True)
        self.combo_icon.setVisible(False)
        self.toolbox_button.setText("Toolbox")

        # set sidebar collapser icon
        self.sidebar_collapser_button.setIcon(QIcon("app_view/icons/double-chevron-left.svg"),)

         # adjust sidebar width 
        self.sidebar.setMinimumWidth(DEFAULT_MINIMUM_WIDTH)
        self.sidebar.setMaximumWidth(DEFAULT_MINIMUM_WIDTH + 100)
        self.page_splitter.setSizes([DEFAULT_MINIMUM_WIDTH, self.width() - DEFAULT_MINIMUM_WIDTH])


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


    def populate_combo(self, label: str, icon: QIcon, options: list[str]) -> None:

        # show combo container
        self.menu_container.setVisible(True)

        # set combo label, icon and populate dropdown options
        self.combo_label.setText(label)
        self.combo_icon.setIcon(icon)
        self.combo_box.clear()
        self.combo_box.addItems(options)


    def populate_slicers(self, fields) -> None:

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

        # hide clear slicer button
        self.clear_slicer_button.setVisible(False)

        # clear all slicers values
        for slicer in self.slicer_container.findChildren(LineEditWidget):
            slicer.clear()

    
    def update_header(self, text: str) -> None:
        self.header.setText(text)


    def toggle_page_visibility(self, visible: bool) -> None:

        # hide landing page
        self.landing_page.setVisible(False)

        # hide page contents other than header
        self.sub_header_container.setVisible(visible)
        self.filter_container.setVisible(visible)
        self.table.setVisible(visible)
        self.page_placeholder.setVisible(not visible)


    def update_sub_header(self, text: str) -> None:
        self.sub_header.setText(text)


    def populate_table(self, model: object) -> None:
        self.table.setModel(model)


    def populate_toolbox(self, tools: dict=None) -> None:
        if tools is None: 
            self.toolbox_container.layout().addWidget(LabelWidget(label_style.slicer, "No tools added yet!"))

        # activate button and show toolbox
        self.toolbox_button.setStyleSheet(button_style.toggle_active)
        self.toolbox_container.setVisible(True)


    def collapse_toolbox(self) -> None:
        for widget in self.toolbox_container.children():
            if widget is not self.toolbox_container.layout(): widget.deleteLater()

        # deactivate button and hide toolbox
        self.toolbox_button.setStyleSheet(button_style.toggle_inactive)
        self.toolbox_container.setVisible(False)


    def expand_filters(self, fields: list[str], filter_map: dict, binding: callable) -> None:
            
        # update filter toggle style and icon
        self.filter_toggle.setStyleSheet(button_style.filter_highlight)
        self.filter_toggle.setIcon(QIcon("app_view/icons/chevron-up.svg"))

        # grid layout to hold filter fields
        self.filter_grid = Grid(content_margins=[10,10,10,10], spacing=10)
        self.filter_container.layout().addLayout(self.filter_grid)

        # create filter fields (7 columns x however many rows necessary)
        row = 0
        for index, field in enumerate(fields):

            # create filter field + binding and add to grid
            value = filter_map[field] if field in filter_map else ""
            filter = LineEditWidget(line_edit_style.input_box, field, value)
            filter.textChanged.connect(binding)

            # add widget to apprioriate grid cell
            if index % 7 == 0: row += 1
            self.filter_grid.addWidget(filter, row, index % 7)

        
    def collapse_filters(self) -> None:

        # update filter toggle style and icon
        self.filter_toggle.setStyleSheet(button_style.filter)
        self.filter_toggle.setIcon(QIcon("app_view/icons/chevron-down.svg"))

        # remove filter fields from grid
        for filter in self.filter_container.findChildren(LineEditWidget):
            filter.deleteLater()

        # remove grid layout from filter frame
        self.filter_grid.deleteLater()


    def toggle_clear_filter_visibility(self, visible: bool) -> None:
        self.clear_filter.setVisible(visible)


    def clear_filters(self) -> None:

        # clear all filter values
        for filter in self.filter_container.findChildren(LineEditWidget):
            filter.clear()


    def set_save_status(self, message: str, indicator: ['red','yellow','green']) -> None:

        # set status message 
        self.save_status.setText(message)

        # set status indicator color
        if indicator == "red":
            pass
            #self.status_indicator.setStyleSheet(label_style.indicator_red)
        elif indicator == "yellow":
            self.status_indicator.setStyleSheet(label_style.indicator_yellow)
        elif indicator == "green":
            self.status_indicator.setStyleSheet(label_style.indicator_green)


    def reset_save_status(self) -> None:
        self.status_indicator.setStyleSheet(label_style.indicator_neutral)
        self.save_status.setText("No Changes")

    
    def set_table_status(self, message: str) -> None:
        self.table_status.setText(message)

    
    def set_refresh_state(self, message: str) -> None:
        self.refresh_state.setText(message)


    def toggle_status_bar_visibility(self, visible: bool) -> None:
        self.status_bar.setVisible(visible)

    
    def toggle_save(self, enabled: bool) -> None:
        self.save_button.setEnabled(enabled)