vertical_scrollbar = """
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
"""

horizontal_scrollbar = """
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
"""
table = """
    QTableView {
        background-color: #1f1f1f;
        color: #BABABA;
        gridline-color: #333333;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
    }
    
    QTableView::item {
        background-color: #1f1f1f;
        color: #BABABA;
        border: none;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
    }

    QHeaderView::section {
        background-color: #1f1f1f;
        color: #BABABA;
        border: 1px solid #333333;
        border-left: none;
        border-top: none;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
        text-align: left;
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
    QTableView QLineEdit {  
        background-color: #1f1f1f;
        color: #BABABA;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
    }
"""

ui_button = """
    QPushButton {
        background-color: transparent;
        padding: 8px;
        border: none;
    }
    QPushButton:hover {
        background-color: #3c3c3c;
        border-radius: 4px;                           
    }
"""

visible_splitter = """
    QSplitter::handle {
        background-color: #3c3c3c; 
        border: 12px transparent;
    } 
    QSplitter {
        background-color: transparent;
        border: none;
    }
"""

hidden_splitter = """
    QSplitter::handle {
        background-color: transparent; 
        border: none; 
    }
"""

hidden = """
        background-color: transparent; 
        border: none; 
"""

menu_label = """
    QLabel {
        font-family: "Microsoft Sans Serif";
        font-size: 18px;
        padding: 20px 0px 0px 0px;
        color: #EEEEEE;
        background-color: transparent;
    }
"""

quick_filter_label = """
    QLabel {
        font-family: "Microsoft Sans Serif";
        font-size: 16px;
        font-style: italic;
        padding: 20px 0px 0px 0px;
        color: #EEEEEE;
        background-color: transparent;
    }
"""

page_label = """
    QLabel {
        color: #EEEEEE;
        background-color: transparent;
        padding: 0px 0px 0px 30px;
        font-family: "Microsoft Sans Serif";
        font-size: 22px;
    }
"""

combobox = """
    QComboBox {
        background-color: #181818;
        border: none;
        border-radius: 4px;
        padding: 8px;
        min-width: 6em;
        color: #BDBDBD;
        font-family: "Microsoft Sans Serif";
        font-size: 14px;
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
        padding:  0px 8px 0px 8px ;
        border: 1px solid #333333;
        border-radius: 4px;
    }
    QComboBox QAbstractItemView::item {
        color: #BDBDBD;
        padding: 6px;
        font-family: "Microsoft Sans Serif";
        font-size: 14px;
    }
"""

base_button = """
    QPushButton {{
        text-align: {alignment};
        border: none;
        padding: 8px;
        border-radius: 4px;
        color: {color};
        background-color: {bg_color};
        font-family: "Microsoft Sans Serif";
        font-size: 14px;
    }}
    QPushButton:hover {{
        background-color: {hover_bg_color};
        color: #FFFFFF;
    }}
"""

icon_button_active = base_button.format(alignment="center", color="#EEEEEE", bg_color="#2F2F2F", hover_bg_color="#3F3F3F")
icon_button_inactive = base_button.format(alignment="center", color="#BDBDBD", bg_color="transparent", hover_bg_color="#2F2F2F")
text_button_active = base_button.format(alignment="left", color="#EEEEEE", bg_color="#2F2F2F", hover_bg_color="#3F3F3F")
text_button_inactive = base_button.format(alignment="left", color="#BDBDBD", bg_color="transparent", hover_bg_color="#2F2F2F")

dividing_line = "background-color: #3c3c3c; border: none; padding: 10px;"

light_gray_frame = "background-color: #1f1f1f; border: none;"

dark_gray_frame = "background-color: #181818; border: none;"

