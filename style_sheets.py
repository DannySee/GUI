vertical_scrollbar = """
    QScrollBar:vertical {
        background: transparent;
        border: none;
        width: 8px;
    }
    QScrollBar::handle:vertical {
        background: #555555;
        border-radius: 4px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background: #777777;
    }
    QScrollBar::add-line:vertical {
        background: none;
        height: 0px;
    }
    QScrollBar::sub-line:vertical {
        background: none;
        height: 0px;
    }
    QScrollBar::add-page:vertical {
        background: transparent; /* Customize the background color of the track */

    }
    QScrollBar::sub-page:vertical {
        background: transparent; /* Customize the background color of the track */

    }
"""

horizontal_scrollbar =  """
   QScrollBar:horizontal {
       background: transparent;
       height: 8px;
       border: none;
   }
   QScrollBar::handle:horizontal {
       background: #555555;
       border-radius: 4px;
       min-width: 20px;
   }
   QScrollBar::handle:horizontal:hover {
       background: #777777;
   }
   QScrollBar::add-line:horizontal {
       background: none;
       width: 0;
   }
   QScrollBar::sub-line:horizontal {
       background: none;
       width: 0;
   }
   QScrollBar::add-page:horizontal {
        background: transparent; /* Customize the background color of the track */
   }
   QScrollBar::sub-page:horizontal {
       background: transparent; /* Customize the background color of the track */
   }
"""

table = """
    QTableView {
        background-color: #1f1f1f;
        border:1px solid #3c3c3c;
        border-radius: 10px;
        color: #BDBDBD;
        gridline-color: #333333;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
        outline: 0;
    }
    QTableView::item {
        background-color: #1f1f1f;
        border: none;
        color: #EEEEEE;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
    }
    QTableView::item:selected {
        background-color: #181818;
        font-weight: bold;
        border: 1px solid #3c3c3c;
    }
    QHeaderView {
        background-color: #2f2f2f;
        border-top-left-radius: 10px;
    }
    QHeaderView::section {
        background: #2f2f2f;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
        color: #BDBDBD;
        border-top-left-radius: 10px;
        border-bottom: 1px solid #3c3c3c;
        border-right: 1px solid #3c3c3c;
    }
    QTableView QLineEdit {  
        background-color: #181818;
        color: #EEEEEE;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
        border: 1px solid #3c3c3c;
    }
    QTableView::corner {
        border-bottom-right-radius: 10px;
    }    
"""

ui_button = """
    QPushButton {
        background-color: transparent;
        padding: 8px;
        border: none;
        outline: 0;
    }
    QPushButton:hover {
        background-color: #3c3c3c;
        border-radius: 4px;                           
    }
"""

control_button = """
    QPushButton {
        background-color: transparent;
        padding: 20px 0px 10px 0px;
        border: none;
        outline: 0;
    }
"""

quick_filter = """
    QLineEdit {
        background-color: #181818;
        border: none;
        border-radius: 4px;
        padding: 8px;
        color: #EEEEEE;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
    }
    QLineEdit::placeholder {
        background-color: #181818;
        border: none;
        border-radius: 4px;
        padding: 8px;
        color: #BDBDBD;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
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

sidebar_label = """
    QLabel {
        font-family: "Microsoft Sans Serif";
        font-size: 16px;
        padding: 20px 0px 10px 0px;
        color: #EEEEEE;
        background-color: transparent;
    }
"""

page_label = """
    QLabel {
        color: #EEEEEE;
        font-weight: bold;
        background-color: transparent;
        font-family: "Microsoft Sans Serif";
        font-size: 34px;
    }
"""

combobox = """
    QComboBox {{
        background-color: #181818;
        border: none;
        border-radius: 4px;
        padding: 8px;
        min-width: 6em;
        color: {color};
        font-family: "Microsoft Sans Serif";
        font-size: 14px;
        outline: 0;
    }}
    QComboBox::drop-down {{
        width: 30px;
        border-left: none;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
    }}
    QComboBox::down-arrow {{
        image: url(icons/menu-down.svg);
    }}
    QComboBox:editable {{
        background: #181818;    
    }}
    QComboBox QAbstractItemView {{
        padding:  0px 8px 0px 8px ;
        border: 1px solid #333333;
        border-radius: 4px;
    }}
    QComboBox QAbstractItemView::item {{
        color: #EEEEEE;
        padding: 6px;
        font-family: "Microsoft Sans Serif";
        font-size: 14px;
    }}
"""

default_combobox = combobox.format(color="#BDBDBD")
active_combobox = combobox.format(color="#EEEEEE")

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
        outline: 0;
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

