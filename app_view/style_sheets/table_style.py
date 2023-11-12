import app_view.style_sheets.color_palette as color
from string import Template


table = Template(
    """
    QTableView {
        background-color: $background_light_1;
        border:1px solid $background_bright;
        border-radius: 10px;
        color: $text_dark;
        gridline-color: $light_gray_1;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
        outline: 0;
    }
    QTableView::item {
        background-color: $background_light_1;
        border: none;
        color: $text_light;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
    }
    QTableView::item:selected {
        background-color: $background_dark;
        font-weight: bold;
        border: 1px solid $background_bright;
    }
    QHeaderView {
        background-color: $background_light_2;
        border-top-left-radius: 10px;
    }
    QHeaderView::section {
        background: $background_light_2;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
        color: $text_dark;
        border-top-left-radius: 10px;
        border-bottom: 1px solid $background_bright;
        border-right: 1px solid $background_bright;
    }
    QTableView QLineEdit {  
        background-color: $background_dark;
        color: $text_light;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
        border: 1px solid $background_bright;
    }
    QTableView::corner {
        border-bottom-right-radius: 10px;
    }   
    """
).substitute(background_light_1=color.background_light_1, 
             background_bright=color.background_bright, 
             background_dark=color.background_dark, 
             background_light_2=color.background_light_2, 
             text_dark=color.text_dark, 
             text_light=color.text_light, 
             light_gray_1=color.light_gray_1)

