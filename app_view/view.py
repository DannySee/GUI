from app_view.widgets.button_widget import ButtonWidget
from app_view.widgets.combo_box_widget import ComboBoxWidget
from app_view.widgets.frame_widget import FrameWidget
from app_view.widgets.layout_widget import VerticalBox, HorizontalBox, Grid
from app_view.widgets.scroll_area_widget import ScrollWidget, NoScrollWidget
from app_view.widgets.splitter_widget import SplitterWidget
from app_view.widgets.label_widget import LabelWidget
from app_view.widgets.line_edit_widget import LineEditWidget
from app_view.widgets.table_widget import TableWidget, CustomDelegate
from app_view.widgets.titlebar_widget import TitleBarWidget
from PyQt6.QtWidgets import QMainWindow, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from typing import Protocol
from app_view.style_sheets import (button_style, splitter_style, table_style, universal_style, 
                                   combo_box_style, label_style, line_edit_style, frame_style, scroll_bar_style)


DEFAULT_MINIMUM_WIDTH = 200


class Presenter(Protocol):
    def collapser_binding(self) -> None:
        ...
    def login_binding(self, email: str, password: str) -> None:
        ...
    def register_binding(self) -> None:
        ...
    def cancel_registration_binding(self) -> None:
        ...
    def complete_registration_binding(self, team: str, first_name: str, last_name: str, email: str, 
                                      network_id: str, sus_id: str, password: str, confirm_password: str) -> None:
        ...
    def forgot_binding(self, email: str) -> None:
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
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.titleBar = TitleBarWidget()
        self.setMenuWidget(self.titleBar)

        
    def init_ui(self, presenter: Presenter, navi_map: dict) -> None:

        # ------------------------------- save navigation map to object -----------------------
        self.navi_map = navi_map

        # ------------------------------- application container -------------------------------
        self.app_container = FrameWidget(universal_style.dark_gray, VerticalBox(alignment=None), parent=self)
        self.setCentralWidget(self.app_container)

        # ---------------------- splitter to separate sidebar main page ----------------------
        self.page_splitter = SplitterWidget(Qt.Orientation.Horizontal, splitter_style.hidden, False)
        self.app_container.layout().addWidget(self.page_splitter)
        
        # -------------------------------------- sidebar --------------------------------------
        
        # sidebar container
        self.sidebar = FrameWidget(universal_style.light_gray_1, VerticalBox(), visible=False,
                                                minimum_width=DEFAULT_MINIMUM_WIDTH, 
                                                maximum_width=DEFAULT_MINIMUM_WIDTH+100)
        self.page_splitter.addWidget(self.sidebar)
        
        # sidebar collapser button and spacer to separate collapser button from navigation buttons
        self.construct_sidebar_collapser(self.sidebar, presenter.collapser_binding)

        # sidebar splitter to separate navigation buttons from menu dropdowns
        self.sidebar_splitter = SplitterWidget(Qt.Orientation.Vertical, splitter_style.visible,False, width=1)
        self.sidebar.layout().addWidget(self.sidebar_splitter)

        # sidebar navigation  
        self.construct_navigation(self.sidebar_splitter, presenter.navigation_binding)

        # sidebar menu box
        self.menu = FrameWidget(universal_style.hidden, VerticalBox(content_margins=[10,10,10,10],spacing=5), parent=self.sidebar_splitter)
        self.menu_scroll_area = ScrollWidget(universal_style.hidden, widget=self.menu, parent=self.sidebar_splitter)
        self.sidebar_splitter.addWidget(self.menu_scroll_area)

        # sidebar menu items
        self.construct_menu(self.menu, presenter.combo_binding, presenter.toolbox_binding)

        # quick slicers
        self.construct_slicers(self.menu, presenter.slicer_binding, presenter.clear_slicer_binding, 
                               presenter.slicer_settings_binding)

        # -------------------------------------- page --------------------------------------

        # main page container
        self.main_page = FrameWidget(universal_style.hidden, VerticalBox(), parent=self.page_splitter)
        self.page_splitter.addWidget(self.main_page)

        # toolbar 
        self.construct_toolbar(self.main_page, presenter.save_binding, presenter.import_binding, presenter.export_binding)

        # page container
        self.page = FrameWidget(universal_style.hidden, VerticalBox(content_margins=[30,40,30,30], spacing=10), parent=self.main_page)
        self.page_scroll_area = ScrollWidget(universal_style.hidden,widget=self.page, parent=self.main_page)
        self.main_page.layout().addWidget(self.page_scroll_area)

        # user login
        self.construct_login(self.page, presenter.login_binding, presenter.register_binding, presenter.forgot_binding)
        self.construct_register(self.page, presenter.cancel_registration_binding, presenter.complete_registration_binding)
        
        # landing page
        self.construct_landing_page(self.page)

        # page header
        self.header = LabelWidget(label_style.header, parent=self.page)
        self.page.layout().addWidget(self.header)

        # spacer to separate sub header from filters
        self.page.layout().addSpacing(15)

        # sub header and spacer to header from sub header 
        self.construct_sub_header(self.page, presenter.refresh_binding)

        # filters
        self.construct_filters(self.page, presenter.filter_toggle_binding, presenter.clear_filter_binding)

        # data table
        self.table = TableWidget(table_style.table, scroll_bar_style.table_vertical, scroll_bar_style.table_horizontal, visible=False)
        self.page.layout().addWidget(self.table)

        # hidden table container for loading/mid page purposes
        self.construct_page_placeholder(self.page)

        # status bar 
        self.construct_status_bar(self.main_page)

        # ----------------------------- splitter default position -----------------------------

        # paget contents take horizontal priority over sidebar
        self.page_splitter.setStretchFactor(0, 0)
        self.page_splitter.setStretchFactor(1, 1)


    # ------------------------------ ui cunstructor functions ------------------------------
    def construct_sidebar_collapser(self, parent: object, binding: callable) -> None:

        # collapse button widget and bind to presenter operation
        self.sidebar_collapser_button = ButtonWidget(button_style.discrete,icon=QIcon("app_view/icons/double-chevron-left.svg"), parent=parent)
        self.sidebar_collapser_button.clicked.connect(binding)

        # create custom layout to push button to right of sidebar and add to parent layout
        sidebar_collapser_layout = HorizontalBox(content_margins=[5,5,5,5], alignment=Qt.AlignmentFlag.AlignRight)
        sidebar_collapser_layout.addWidget(self.sidebar_collapser_button)
        parent.layout().addLayout(sidebar_collapser_layout)

        # create spacer
        parent.layout().addSpacing(20)


    def construct_navigation(self, parent: object, binding: callable) -> None:

        # sidebar navigation container
        self.navigation = FrameWidget(universal_style.hidden,VerticalBox(content_margins=[10,10,10,10],spacing=5), minimum_width=10, parent=parent)
        self.navi_scroll_area = ScrollWidget(universal_style.hidden,widget=self.navigation,maximum_height=len(self.navi_map)*40+21, parent=parent)
        parent.addWidget(self.navi_scroll_area)

        # create a button widget for each navigation option, bind, and add to parent layout
        for navi in self.navi_map:
            navi_button = ButtonWidget(
                button_style.toggle_inactive, 
                icon=self.navi_map[navi]["icon"], 
                icon_size=[20,20], 
                text=self.navi_map[navi]["text"], object_name=navi, 
                parent=parent
            )
            navi_button.clicked.connect(binding)
            self.navigation.layout().addWidget(navi_button)
    
    
    def construct_menu(self, parent: object, combo_binding: callable, toobox_binding: callable) -> None:

        # sidebar combo container
        self.menu_container = FrameWidget(universal_style.hidden, vertical_size_policy=QSizePolicy.Policy.Fixed,visible=False,
                                          layout=VerticalBox(content_margins=[0,20,0,10], spacing=5), minimum_width=10, parent=parent)
        parent.layout().addWidget(self.menu_container)

        # combo label
        self.combo_label = LabelWidget(label_style.combo, parent=self.menu_container)
        self.menu_container.layout().addWidget(self.combo_label)

        # disabled button to hold collapsed combo icon
        self.combo_icon = ButtonWidget(button_style.combo, visible=False, icon_size=[20,20], fixed_width=36, parent=self.menu_container)
        self.menu_container.layout().addWidget(self.combo_icon)
        self.menu_container.layout().addSpacing(5)

        # combo dropdowns
        self.combo_box = ComboBoxWidget(combo_box_style.inactive, "--Select Data--", parent=self.menu_container)
        self.combo_box.currentIndexChanged.connect(combo_binding)
        self.menu_container.layout().addWidget(self.combo_box)

        # toolbox button 
        self.toolbox_button = ButtonWidget(button_style.toggle_inactive, "Toolbox", icon=QIcon("app_view/icons/toolbox.svg"), icon_size=[20,20], parent=self.menu_container)
        self.toolbox_button.clicked.connect(toobox_binding)
        self.menu_container.layout().addWidget(self.toolbox_button)

        # toolbox container
        self.toolbox_container = FrameWidget(universal_style.generic_border_pane, VerticalBox(content_margins=[5,5,5,5],spacing=5), visible=False, parent=self.menu_container)
        self.menu_container.layout().addWidget(self.toolbox_container)

        # dividing line
        self.menu_container.layout().addSpacing(10)
        self.dividing_line = FrameWidget(universal_style.bright_gray, fixed_height=1, parent=self.menu_container)
        self.menu_container.layout().addWidget(self.dividing_line)


    def construct_slicers(self, parent: object, slicer_binding: callable, clear_binding: callable, 
                          settings_binding: callable, count=5) -> None:

        # slicer container
        self.slicer_container = FrameWidget(universal_style.hidden, VerticalBox(spacing=5), 
                                            visible=False, vertical_size_policy=QSizePolicy.Policy.Maximum, parent=parent)
        parent.layout().addWidget(self.slicer_container)

        # layout to hold label and clear slicer button
        slicer_layout = HorizontalBox()

        # slicer label and stretch separator
        slicer_label = LabelWidget(label_style.slicer, "Quick Slicers", parent=self.slicer_container)
        slicer_layout.addWidget(slicer_label)
        slicer_layout.addStretch()

        # clear slicer button
        self.clear_slicer_button = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/clear-filter.svg"), visible=False, parent=self.slicer_container)
        self.clear_slicer_button.clicked.connect(clear_binding)
        slicer_layout.addWidget(self.clear_slicer_button)

        # add slicer layout to container layout
        self.slicer_container.layout().addLayout(slicer_layout)

        # create a slicer widgets, bind, and add to parent layout
        for _ in range(count):
            slicer = LineEditWidget(line_edit_style.input_box, parent=self.slicer_container)
            slicer.textChanged.connect(slicer_binding)
            self.slicer_container.layout().addWidget(slicer)

        # slicer settings button
        slicer_settings = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/settings.svg"),
                                       fixed_width=26, tool_tip="Slicer Settings", parent=self.slicer_container)
        slicer_settings.clicked.connect(settings_binding)
        self.slicer_container.layout().addWidget(slicer_settings)

    
    def construct_toolbar(self, parent: object, save_binding: callable, import_binding: callable, export_binding: callable) -> None:

        # create toolbar container
        toolbar = FrameWidget(frame_style.toolbar, HorizontalBox(), fixed_height=26, parent=parent)
        parent.layout().addWidget(toolbar)

        # toolbar container to toggle visibility of buttons
        self.toolbar_container = FrameWidget(universal_style.hidden, HorizontalBox(content_margins=[5,2,5,2], spacing=2,alignment=Qt.AlignmentFlag.AlignLeft), visible=False, parent=toolbar)
        toolbar.layout().addWidget(self.toolbar_container)

        # save button
        self.save_button = ButtonWidget(button_style.toolbar, text="Save", enabled=False, parent=self.toolbar_container)
        self.save_button.clicked.connect(save_binding)
        self.toolbar_container.layout().addWidget(self.save_button)

         # export button
        self.export_button = ButtonWidget(button_style.toolbar, text="Check Out", enabled=False, parent=self.toolbar_container)
        self.export_button.clicked.connect(export_binding)
        self.toolbar_container.layout().addWidget(self.export_button)

        # import button
        self.import_button = ButtonWidget(button_style.toolbar, text="Check In", parent=self.toolbar_container)
        self.import_button.clicked.connect(import_binding)
        self.toolbar_container.layout().addWidget(self.import_button)


    def construct_login(self, parent: object, login_binding: callable, register_binding: callable, forgot_binding: callable) -> None:

        # login page container
        self.login_page = FrameWidget(universal_style.hidden, VerticalBox(alignment=Qt.AlignmentFlag.AlignCenter), parent=parent)
        parent.layout().addWidget(self.login_page)
        
        # login container
        container = FrameWidget(universal_style.generic_border_pane, layout=VerticalBox(content_margins=[20,20,20,20], spacing=10),
                                horizontal_size_policy=QSizePolicy.Policy.Maximum, vertical_size_policy=QSizePolicy.Policy.Maximum, parent=self.login_page)
        self.login_page.layout().addWidget(container)

        # login page header and sub header
        login_header = LabelWidget(label_style.header, "Sign In", parent=container)
        container.layout().addWidget(login_header)
        login_sub_header = LabelWidget(label_style.sub_header, "Commercial Services Hive", parent=container)
        container.layout().addWidget(login_sub_header)

        # dividing line
        dividing_line = FrameWidget(universal_style.bright_gray, fixed_height=1, parent=container)
        container.layout().addWidget(dividing_line)
        container.layout().addSpacing(10)

        # email inputbox 
        email = LineEditWidget(line_edit_style.form_input_box, "Email", parent=container)
        container.layout().addWidget(email)

        # password inputbox
        password = LineEditWidget(line_edit_style.form_input_box, "Password", echo_mode=LineEditWidget.EchoMode.Password, parent=container)
        container.layout().addWidget(password)

        # add spacer
        container.layout().addSpacing(10)

        # login button
        login_button = ButtonWidget(button_style.dialog_primary, text="Login", parent=container)
        login_button.clicked.connect(lambda: login_binding(email.text(), password.text()))
        container.layout().addWidget(login_button)

        # add layout for register and forgot password buttons
        button_layout = HorizontalBox(alignment=Qt.AlignmentFlag.AlignCenter)
        container.layout().addLayout(button_layout)

        # register button
        register_button = ButtonWidget(button_style.toggle_discrete_blue, text="Register", parent=container)
        register_button.clicked.connect(register_binding)
        button_layout.addWidget(register_button)

        # spacer to separate register and forgot password buttons
        button_layout.addStretch()

        # forgot password button
        self.forgot_button = ButtonWidget(button_style.toggle_discrete_blue, text="Forgot Password", parent=container)
        self.forgot_button.clicked.connect(lambda: forgot_binding(email.text()))
        button_layout.addWidget(self.forgot_button)


    def construct_register(self, parent: object, cancel_binding: callable, register_binding: callable) -> None:

        # register page
        self.register_page = FrameWidget(universal_style.hidden, VerticalBox(alignment=Qt.AlignmentFlag.AlignCenter), visible=False, parent=parent)
        parent.layout().addWidget(self.register_page)


        # form container
        container = FrameWidget(universal_style.generic_border_pane,
                                        layout=VerticalBox(content_margins=[20,20,20,20], spacing=10),
                                        horizontal_size_policy=QSizePolicy.Policy.Maximum, 
                                        vertical_size_policy=QSizePolicy.Policy.Maximum, 
                                        parent=self.register_page)
        self.register_page.layout().addWidget(container)

        # register page label
        register_header = LabelWidget(label_style.header, "Sign Up", parent=container)
        container.layout().addWidget(register_header)
        register_sub_header = LabelWidget(label_style.sub_header, "Join the Commercial Services Hive", parent=container)
        container.layout().addWidget(register_sub_header)

        # dividing line
        dividing_line = FrameWidget(universal_style.bright_gray, fixed_height=1, parent=container)
        container.layout().addWidget(dividing_line)
        container.layout().addSpacing(10)

        # combo for team selection
        teams = [navi['text'] for navi in self.navi_map.values()]
        team_combo = ComboBoxWidget(combo_box_style.active, "--Select Team--", parent=container)
        team_combo.addItems(teams)
        container.layout().addWidget(team_combo)

        # register form fields
        row = HorizontalBox(spacing=10, alignment=Qt.AlignmentFlag.AlignCenter)
        container.layout().addLayout(row)
        first_name = LineEditWidget(line_edit_style.form_input_box, "First Name", parent=container)
        row.addWidget(first_name)
        last_name = LineEditWidget(line_edit_style.form_input_box, "Last Name", parent=container)
        row.addWidget(last_name)
        email = LineEditWidget(line_edit_style.form_input_box, "Email", parent=container)
        container.layout().addWidget(email)
        row = HorizontalBox(spacing=10, alignment=Qt.AlignmentFlag.AlignCenter)
        container.layout().addLayout(row)
        network_id = LineEditWidget(line_edit_style.form_input_box, "Network ID", parent=container)
        row.addWidget(network_id)
        sus_id = LineEditWidget(line_edit_style.form_input_box, "SUS ID", parent=container)
        row.addWidget(sus_id)
        password = LineEditWidget(line_edit_style.form_input_box, "Password", echo_mode=LineEditWidget.EchoMode.Password, parent=container)
        container.layout().addWidget(password)
        confirm_password = LineEditWidget(line_edit_style.form_input_box, "Confirm Password", echo_mode=LineEditWidget.EchoMode.Password, parent=container)
        container.layout().addWidget(confirm_password)

        # add spacer 
        container.layout().addSpacing(10)

        # register and cancel buttons
        row = HorizontalBox(spacing=10, alignment=Qt.AlignmentFlag.AlignCenter)
        container.layout().addLayout(row)
        cancel_button = ButtonWidget(button_style.dialog_secondary, text="Cancel", fixed_width=140, parent=container)
        cancel_button.clicked.connect(cancel_binding)
        row.addWidget(cancel_button)
        register_button = ButtonWidget(button_style.dialog_primary, text="Register", fixed_width=140, parent=container)
        register_button.clicked.connect(lambda: register_binding(team_combo.currentText(), first_name.text(), last_name.text(), email.text(), network_id.text(), sus_id.text(), password.text(), confirm_password.text()))
        row.addWidget(register_button)
        

    def construct_landing_page(self, parent: object) -> None:

        # landing page container
        self.landing_page = FrameWidget(universal_style.hidden, VerticalBox(), visible=False, parent=parent)
        parent.layout().addWidget(self.landing_page)

        # landing page header
        self.landing_page_header = LabelWidget(label_style.header, "", parent=self.landing_page)
        self.landing_page.layout().addWidget(self.landing_page_header)

        # spacer
        self.landing_page.layout().addSpacing(10)

        # landing page sub header
        self.landing_page_sub_header = LabelWidget(label_style.sub_header, "", parent=self.landing_page)
        self.landing_page.layout().addWidget(self.landing_page_sub_header)

        # logo layout
        logo_container = FrameWidget(universal_style.hidden, VerticalBox(alignment=Qt.AlignmentFlag.AlignCenter), parent=self.landing_page)
        self.landing_page.layout().addWidget(logo_container)

        # spacer 
        logo_container.layout().addSpacing(20)

        # frame to hold icon
        container = FrameWidget(universal_style.generic_border_pane_round, VerticalBox(content_margins=[50,50,50,50],spacing=10, alignment=Qt.AlignmentFlag.AlignCenter),
                            vertical_size_policy=QSizePolicy.Policy.Fixed, horizontal_size_policy=QSizePolicy.Policy.Fixed, parent=logo_container)
        logo_container.layout().addWidget(container)

        # create hive image parameters
        max_width = 280
        width = 160
        over_the_hump = False

        # loop to create 6 segments
        for _ in range(6):

            # create frame object and add to layout
            layout = HorizontalBox(alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(FrameWidget(universal_style.hive_segments, fixed_height=40, fixed_width=width, parent=container))
            container.layout().addLayout(layout)

            # increment/decrement width
            width = width - 40 if over_the_hump else width + 40
            if width == max_width: over_the_hump = True

        
    def construct_filters(self, parent: object, fitler_toggle_binding: callable, clear_filter_binding: callable) -> None:
        
        # filter frame 
        self.filter_container = FrameWidget(frame_style.filter, VerticalBox(), vertical_size_policy=QSizePolicy.Policy.Minimum, visible=False, parent=parent)
        parent.layout().addWidget(self.filter_container)

        # header layout 
        header_layout = HorizontalBox(spacing=10)
        self.filter_container.layout().addLayout(header_layout)

        # expand filter button
        self.filter_toggle = ButtonWidget(button_style.filter, text="Filters", icon=QIcon("app_view/icons/chevron-down.svg"), parent=self.filter_container)
        self.filter_toggle.clicked.connect(fitler_toggle_binding)
        header_layout.addWidget(self.filter_toggle)

        # clear filter button 
        self.clear_filter = ButtonWidget(button_style.clear_filter, text="Clear Filters", 
                                         icon=QIcon("app_view/icons/clear-filter.svg"), 
                                         visible=False, fixed_width=120, parent=self.filter_container)        
        self.clear_filter.clicked.connect(clear_filter_binding)
        header_layout.addWidget(self.clear_filter)


    def construct_sub_header(self, parent: object, refresh_binding: callable) -> None:

        # sub header layout
        self.sub_header_container = FrameWidget(universal_style.hidden, HorizontalBox(), visible=False, 
                                                vertical_size_policy=QSizePolicy.Policy.Maximum, parent=parent)
        parent.layout().addWidget(self.sub_header_container)

        # sub header label 
        self.sub_header = LabelWidget(label_style.sub_header, parent=self.sub_header_container)
        self.sub_header_container.layout().addWidget(self.sub_header)

        # add strech to separate label from 
        self.sub_header_container.layout().addStretch()

        # refresh timestamp 
        self.refresh = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/refresh.svg"), tool_tip="Refresh", parent=self.sub_header_container)
        self.refresh.clicked.connect(refresh_binding)
        self.sub_header_container.layout().addWidget(self.refresh)


    def construct_page_placeholder(self, parent: object) -> None:

        # loading container
        self.page_placeholder = FrameWidget(universal_style.hidden, VerticalBox(spacing=10, alignment=Qt.AlignmentFlag.AlignCenter), visible=False, parent=parent)
        parent.layout().addWidget(self.page_placeholder)

        # add spacer
        self.page_placeholder.layout().addSpacing(6)

        # sub header 
        ph_sub_header_layout = HorizontalBox()
        ph_sub_header_label = FrameWidget(frame_style.loader_bright, fixed_height=20, maximum_width=400, parent=self.page_placeholder)
        ph_sub_header_layout.addWidget(ph_sub_header_label)
        ph_sub_header_layout.addStretch()
        ph_sub_header_button = FrameWidget(frame_style.loader_bright, fixed_height=20, maximum_width=160, parent=self.page_placeholder)
        ph_sub_header_layout.addWidget(ph_sub_header_button)
        self.page_placeholder.layout().addLayout(ph_sub_header_layout)

        # filters
        ph_filters = FrameWidget(frame_style.loader_light, VerticalBox([10,0,10,0], alignment=Qt.AlignmentFlag.AlignCenter), fixed_height=38, parent=self.page_placeholder)
        self.page_placeholder.layout().addWidget(ph_filters)
        ph_filters_layout = HorizontalBox()
        ph_filter_label = FrameWidget(frame_style.loader_bright, fixed_height=20, maximum_width=300, parent=self.page_placeholder)
        ph_filters_layout.addWidget(ph_filter_label)
        ph_filters_layout.addStretch()
        ph_filter_button = FrameWidget(frame_style.loader_bright, fixed_height=20, maximum_width=220, parent=self.page_placeholder)
        ph_filters_layout.addWidget(ph_filter_button)
        ph_filters.layout().addLayout(ph_filters_layout)

        # table
        ph_table = FrameWidget(universal_style.hidden, VerticalBox([20,20,20,20], spacing=20, alignment=Qt.AlignmentFlag.AlignTop), parent=self.page_placeholder)
        ph_table_scroll = NoScrollWidget(universal_style.generic_border_pane, widget=ph_table, minimum_height=100, parent=self.page_placeholder)
        self.page_placeholder.layout().addWidget(ph_table_scroll)

        # table contents
        padding = True
        rows = self.height() // 40
        for _ in range(rows):
            if padding:
                row_layout = HorizontalBox(alignment=Qt.AlignmentFlag.AlignLeft)
                row_layout.addSpacing(40)
                ph_row = FrameWidget(frame_style.loader_bright, fixed_height=20, parent=self.page_placeholder)
                row_layout.addWidget(ph_row)
                row_layout.addSpacing(40)
                ph_table.layout().addLayout(row_layout)
                padding = False
            else:
                ph_row = FrameWidget(frame_style.loader_bright, fixed_height=20, parent=self.page_placeholder)
                ph_table.layout().addWidget(ph_row)
                padding = True
    

    def construct_status_bar(self, parent: object) -> None:

        # status bar container
        status_container = FrameWidget(frame_style.status_bar, HorizontalBox(), fixed_height=25, parent=parent)
        parent.layout().addWidget(status_container)

        # status bar
        self.status_bar = FrameWidget(universal_style.hidden, visible=False,
            layout=HorizontalBox(content_margins=[20,2,20,2], spacing=10, alignment=Qt.AlignmentFlag.AlignRight), parent=status_container)
        status_container.layout().addWidget(self.status_bar)

        # status message
        self.status_indicator = LabelWidget(label_style.indicator_neutral, fixed_width=14, fixed_height=14, parent=self.status_bar)
        self.status_bar.layout().addWidget(self.status_indicator)
        self.save_status = LabelWidget(label_style.status, "No Changes", parent=self.status_bar)
        self.status_bar.layout().addWidget(self.save_status)

        # add stretch to center status message 
        self.status_bar.layout().addStretch()

        # table info
        self.table_status = LabelWidget(label_style.status, parent=self.status_bar)
        self.status_bar.layout().addWidget(self.table_status)

        # add divinding line to separate table status from refresh state
        dividing_line = FrameWidget(universal_style.bright_gray, fixed_width=1, parent=self.status_bar)
        self.status_bar.layout().addWidget(dividing_line)
 
         # refresh state
        self.refresh_state = LabelWidget(label_style.status, parent=self.status_bar)
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
            navi_button.setText(self.navi_map[navi_button.objectName()]["text"])

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
        self.table.setItemDelegate(CustomDelegate())


    def populate_toolbox(self, tools: dict=None) -> None:
        if tools is None: 
            self.toolbox_container.layout().addWidget(LabelWidget(label_style.slicer, "No tools added yet!", parent=self.toolbox_container))

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
            filter = LineEditWidget(line_edit_style.input_box, field, value, parent=self.filter_container)
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
            self.status_indicator.setStyleSheet(label_style.indicator_red)
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

    
    def toggle_export(self, enabled: bool) -> None:
        self.export_button.setEnabled(enabled)

    
    def toggle_login_visibility(self, visible: bool) -> None:
        self.login_page.setVisible(visible)


    def toggle_register_visibility(self, visible: bool) -> None:
        self.register_page.setVisible(visible)

        # clear form
        for field in self.register_page.findChildren(LineEditWidget):
            field.clear()

        # reset combo
        self.register_page.findChild(ComboBoxWidget).setCurrentIndex(-1)


    def toggle_landing_page_visibility(self, visible: bool, user: str="") -> None:
        self.landing_page.setVisible(visible)
        self.sidebar.setVisible(visible)

        # populate landing page header and sub header if user is provided
        if user != "":
            self.landing_page_header.setText(f"Hi {user}!")
            self.landing_page_sub_header.setText("Welcome to the Commercial Services Hive")


    def toggle_toolbar_visibility(self, visible: bool) -> None:
        self.toolbar_container.setVisible(visible)