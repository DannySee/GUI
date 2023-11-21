
import app_view.style_sheets.color_palette as color
from string import Template


combobox_template = Template(
    """
    QComboBox {
        background-color: $background_dark;
        border: none;
        border-radius: 5px;
        padding: 8px;
        color: $text_color;
        font-family: "Microsoft Sans Serif";
        font-size: 14px;
        outline: 0;
    }
    QComboBox::hover {
        background-color: $background_darkest;
    }
    QComboBox::drop-down {
        width: 30px;
        padding-right: 3px;
        border-left: none;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
    }
    QComboBox::down-arrow {
        image: url(app_view/icons/menu-down.svg);
    }
    QComboBox:editable {
        background: $background_dark;;    
    }
    QComboBox QAbstractItemView {
        padding:  0px 8px 0px 8px ;
        border: 1px solid $light_gray_1;
        border-radius: 5px;
    }
    QComboBox QAbstractItemView::item {
        color: $text_light;
        padding: 6px;
        font-family: "Microsoft Sans Serif";
        font-size: 14px;
    }
    """
)

inactive = combobox_template.substitute(
    background_dark=color.background_dark, 
    background_darkest=color.background_darkest,
    text_light=color.text_light, 
    light_gray_1=color.light_gray_1,
    text_color=color.text_dark
)

active = combobox_template.substitute(
    background_dark=color.background_dark, 
    background_darkest=color.background_darkest,
    text_light=color.text_light, 
    light_gray_1=color.light_gray_1,
    text_color=color.text_light
)

collapsed = combobox_template.substitute(
    background_dark=color.background_dark, 
    background_darkest=color.background_darkest,
    text_light=color.text_light, 
    light_gray_1=color.light_gray_1,
    text_color=color.text_light
)

