import app_view.style_sheets.color_palette as color
from string import Template


label_template = Template(
    """
    QLabel {
        background-color: $background_color;
        font-family: "Microsoft Sans Serif";
        font-size: $text_size;
        font-style: $text_style;
        padding: $padding;
        color: $text_color;
    }
    """
)

combo = label_template.substitute(
    background_color="transparent",
    text_size="16px",
    text_style="normal",
    padding="20px 0px 10px 0px",
    text_color=color.text_light
)
                                       
slicer = label_template.substitute(
    background_color="transparent",
    text_size="14px",
    text_style="normal",
    padding="10px 0px 10px 0px",
    text_color=color.text_dark
)

header = label_template.substitute(
    background_color="transparent",
    text_size="34px",
    text_style="normal",
    padding="0px",
    text_color=color.text_light
)

sub_header = label_template.substitute(
    background_color="transparent",
    text_size="16px",
    text_style="italic",
    padding="0px 0px 5px 0px",
    text_color=color.text_dark
)

text_bright = label_template.substitute(
    background_color="transparent",
    text_size="14px",
    text_style="normal",
    padding="0px",
    text_color=color.text_bright
)