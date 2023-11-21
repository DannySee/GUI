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
        border-radius: $radius;
        border: none;
    }
    """
)

combo = label_template.substitute(
    background_color="transparent",
    text_size="16px",
    text_style="normal",
    padding="1px,0px,0px,0px",
    text_color=color.text_light,
    radius="0px",
)
                                       
slicer = label_template.substitute(
    background_color="transparent",
    text_size="14px",
    text_style="normal",
    padding="10px 0px 10px 0px",
    text_color=color.text_dark,
    radius="0px",
)

header = label_template.substitute(
    background_color="transparent",
    text_size="34px",
    text_style="normal",
    padding="0px",
    text_color=color.text_light,
    radius="0px",
)

sub_header = label_template.substitute(
    background_color="transparent",
    text_size="16px",
    text_style="normal",
    padding="0px",
    text_color=color.text_dark,
    radius="0px",
)

text_bright = label_template.substitute(
    background_color="transparent",
    text_size="14px",
    text_style="normal",
    padding="0px",
    text_color=color.text_bright,
    radius="0px",
)

status = label_template.substitute(
    background_color="transparent",
    text_size="12px",
    text_style="normal",
    padding="0px",
    text_color=color.text_dark,
    radius="8px",
)

indicator_green = label_template.substitute(
    background_color=color.success_green,
    text_size="12px",
    text_style="normal",
    padding="0px",
    text_color=color.text_dark,
    radius="7px",
)

indicator_yellow = label_template.substitute(
    background_color=color.warning_yellow,
    text_size="12px",
    text_style="normal",
    padding="0px",
    text_color=color.text_dark,
    radius="7px",
)

indicator_neutral = label_template.substitute(
    background_color=color.light_gray_1,
    text_size="12px",
    text_style="normal",
    padding="0px",
    text_color=color.text_dark,
    radius="7px",
)