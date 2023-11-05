import color_palette as color
from string import Template


button_template = Template(
    """
    QPushButton {
        background-color: $background_color;
        padding: $padding;
        border: none;
        border-radius: 5px;
        color: $text_color;
        font-family: "Microsoft Sans Serif";
        font-size: 14px;
        outline: 0;
    }
    QPushButton:hover {
        background-color: $background_color_hover;
        color: $text_color_hover;
    }
    """
)

discrete_small = button_template.substitute(
    background_color="transparent", 
    padding="2px", 
    text_color=color.text_dark,
    background_color_hover=color.background_light_2, 
    hover_text_color=color.text_light
)

discrete_standard = button_template.substitute(
    background_color="transparent", 
    padding="8px", 
    text_color=color.text_dark,
    background_color_hover=color.background_light_2, 
    text_color_hover=color.text_light
)

toggle_inactive = button_template.substitute(
    background_color=color.background_light_1,
    padding="8px",
    text_color=color.text_dark,
    background_color_hover=color.background_light_2,
    text_color_hover=color.text_light
)

toggle_active = button_template.substitute(
    background_color=color.background_light_2,
    padding="8px",
    text_color=color.text_light,
    background_color_hover=color.background_light_3,
    text_color_hover=color.text_bright
)


