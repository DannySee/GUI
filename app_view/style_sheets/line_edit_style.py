import app_view.style_sheets.color_palette as color
from string import Template


input_box = Template(
    """
    QLineEdit {
        background-color: $background_dark;
        border: none;
        border-radius: 5px;
        padding: 8px;
        color: $text_light;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
    }
    QLineEdit::hover {
        background-color: #141414;
    }
    QLineEdit::focus {
        background-color: #141414;
    }
    QLineEdit::placeholder {
        background-color: $background_dark;
        border: none;
        border-radius: 5px;
        padding: 8px;
        color: $text_dark;
        font-family: "Microsoft Sans Serif";
        font-size: 12px;
    }
    """
).substitute(background_dark=color.background_dark, 
             text_light=color.text_light, 
             text_dark=color.text_dark)

