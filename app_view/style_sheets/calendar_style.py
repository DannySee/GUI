from string import Template
from app_view.style_sheets import color_palette as color

dateedit_template = Template(
    """
    QDateEdit {
        background-color: $background_dark;
        border: none;
        border-radius: $radius;
        padding: 8px;
        color: $text_color;
        font-family: "Microsoft Sans Serif";
        font-size: $size;
        outline: 0;
    }
    QDateEdit::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 30px;
        border-left-width: 1px;
        border-left-color: $light_gray_1;
        border-left-style: solid;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
    }
    """
)

calendar_style = dateedit_template.substitute(
    background_dark=color.background_dark, 
    background_darkest=color.background_darkest,
    text_light=color.text_light, 
    light_gray_1=color.light_gray_1,
    text_color=color.text_light,
    size='12px',
    radius='0px'
)
