import app_view.style_sheets.color_palette as color
from string import Template


frame_template = Template(
    """
    QFrame {
        background-color: $background_color;
        border-radius: $border_radius;
        border: $border_color;
        border-top: $top_border_color;
        border-bottom: $bottom_border_color;
    }      
    """
)

filter = frame_template.substitute(
    background_color=color.background_light_1, 
    border_color="1px solid " + color.background_bright,
    border_radius="10px",
    top_border_color="1px solid " + color.background_bright,
    bottom_border_color="1px solid " + color.background_bright,
)

toolbar = frame_template.substitute(
    background_color="transparent",
    border_color= "none",
    border_radius="0px",
    top_border_color="none",
    bottom_border_color="none",
)

titlebar = frame_template.substitute(
    background_color=color.background_darkest,
    border_color= "none",
    border_radius="0px",
    top_border_color="none",
    bottom_border_color="1px solid " + color.background_light_2,
)

status_bar = frame_template.substitute(
    background_color=color.background_darkest,
    border_color= "none",
    border_radius="0px",
    top_border_color="1px solid " + color.background_light_2,
    bottom_border_color="1px solid transparent",
)

loader_empty = frame_template.substitute(
    background_color="transparent", 
    border_color="1px solid " + color.background_bright,
    border_radius="10px",
    top_border_color="1px solid " + color.background_bright,
    bottom_border_color="1px solid " + color.background_bright,
)

loader_light = frame_template.substitute(
    background_color=color.background_light_1, 
    border_color="1px solid " + color.background_bright,
    border_radius="10px",
    top_border_color="1px solid " + color.background_bright,
    bottom_border_color="1px solid " + color.background_bright,
)

loader_bright = frame_template.substitute(
    background_color=color.background_light_2, 
    border_color="none",
    border_radius="10px",
    top_border_color="none",
    bottom_border_color="none",
)

