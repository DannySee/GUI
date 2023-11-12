import app_view.style_sheets.color_palette as color
from string import Template


button_template = Template(
    """
    QPushButton {
        background-color: $background_color;
        padding: $padding; 
        border: none;
        border-radius: $border_radius;
        color: $text_color;
        font-family: "Microsoft Sans Serif";
        font-size: 14px;
        text-align: $align;   
        outline: 0;
        qproperty-layoutDirection: $layout_direction;
    }
    QPushButton:hover {
        background-color: $background_color_hover;
        color: $text_color_hover;
    }
    """
)

filter = button_template.substitute(
    background_color="transparent",
    padding="10px",
    text_color=color.text_dark,
    align="left",
    border_radius="10px",
    layout_direction="RightToLeft",
    background_color_hover=color.background_light_2,
    text_color_hover=color.text_light
)

discrete = button_template.substitute(
    background_color="transparent", 
    padding="5px 4px 5px 5px", 
    text_color=color.text_dark,
    border_radius="5px",
    layout_direction="LeftToRight",
    background_color_hover=color.background_light_2, 
    align="center",
    text_color_hover=color.text_light
)

toggle_inactive = button_template.substitute(
    background_color=color.background_light_1,
    padding="8px",
    text_color=color.text_dark,
    border_radius="5px",
    layout_direction="LeftToRight",
    background_color_hover=color.background_light_2,
    align="left",
    text_color_hover=color.text_light
)

toggle_active = button_template.substitute(
    background_color=color.background_light_2,
    padding="8px",
    text_color=color.text_light,
    border_radius="5px",
    layout_direction="LeftToRight",
    background_color_hover=color.background_light_3,
    align="left",
    text_color_hover=color.text_bright
)


