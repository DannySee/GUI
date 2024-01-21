import app_view.style_sheets.color_palette as color
from string import Template


button_template = Template(
    """
    QPushButton {
        background-color: $background_color;
        padding: $padding; 
        border: $border;
        border-radius: $border_radius;
        color: $text_color;
        font-family: "Microsoft Sans Serif";
        font-size: $text_size;
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

toggle_discrete_blue = button_template.substitute(
    background_color="transparent",
    padding="8px",
    border="none",
    text_color=color.light_blue,
    align="center",
    border_radius="8px",
    text_size="14px",
    layout_direction="LeftToRight",
    background_color_hover="transparent",
    text_color_hover=color.lightest_blue
)

dialog_inactive = button_template.substitute(
    background_color=color.background_light_1,
    padding="8px",
    border="1px solid " + color.background_bright,
    text_color=color.text_dark,
    align="center",
    border_radius="8px",
    text_size="14px",
    layout_direction="LeftToRight",
    background_color_hover=color.background_light_1,
    text_color_hover=color.text_dark
)

dialog_tertiary = button_template.substitute(
    background_color=color.light_gray_1_5,
    padding="8px",
    border="1px solid transparent",
    text_color=color.text_dark,
    align="center",
    border_radius="8px",
    text_size="14px",
    layout_direction="LeftToRight",
    background_color_hover=color.light_gray_2,
    text_color_hover=color.text_light
)

dialog_secondary = button_template.substitute(
    background_color=color.light_gray_1_5,
    padding="8px",
    border="1px solid transparent",
    text_color=color.text_light,
    align="center",
    border_radius="8px",
    text_size="14px",
    layout_direction="LeftToRight",
    background_color_hover=color.light_gray_2,
    text_color_hover=color.text_bright
)

dialog_primary = button_template.substitute(
    background_color=color.blue,
    padding="8px",
    border="1px solid transparent",
    text_color=color.text_bright,
    align="center",
    border_radius="8px",
    text_size="14px",
    layout_direction="LeftToRight",
    background_color_hover=color.light_blue,
    text_color_hover=color.text_bright
)

filter = button_template.substitute(
    background_color="transparent",
    padding="10px",
    border="none",
    text_color=color.text_dark,
    align="left",
    border_radius="10px",
    text_size="14px",
    layout_direction="RightToLeft",
    background_color_hover=color.background_light_2,
    text_color_hover=color.text_light
)

filter_highlight = button_template.substitute(
    background_color="transparent",
    padding="10px",
    border="none",
    text_color=color.text_light,
    align="left",
    border_radius="10px",
    text_size="14px",
    layout_direction="RightToLeft",
    background_color_hover=color.background_light_2,
    text_color_hover=color.text_light
)

clear_filter = button_template.substitute(
    background_color=color.background_light_2,
    padding="10px",
    border="none",
    text_color=color.text_light,
    align="left",
    border_radius="10px",
    text_size="14px",
    layout_direction="RightToLeft",
    background_color_hover=color.background_light_3,
    text_color_hover=color.text_bright
)

discrete = button_template.substitute(
    background_color="transparent", 
    padding="5px 4px 5px 5px", 
    border="none",
    text_color=color.text_dark,
    border_radius="5px",
    text_size="14px",
    layout_direction="LeftToRight",
    background_color_hover=color.background_light_2, 
    align="center",
    text_color_hover=color.text_light
)

toggle_inactive = button_template.substitute(
    background_color=color.background_light_1,
    padding="8px",
    border="none",
    text_color=color.text_dark,
    border_radius="5px",
    text_size="14px",
    layout_direction="LeftToRight",
    background_color_hover=color.background_light_2,
    align="left",
    text_color_hover=color.text_light
)

toggle_active = button_template.substitute(
    background_color=color.background_light_2,
    padding="8px",
    border="none",
    text_color=color.text_light,
    border_radius="5px",
    text_size="14px",
    layout_direction="LeftToRight",
    background_color_hover=color.background_light_3,
    align="left",
    text_color_hover=color.text_bright
)

toolbar = button_template.substitute(
    background_color="transparent", 
    padding="4px 6px 4px 6px", 
    border="none",
    text_color=color.text_dark,
    border_radius="5px",
    text_size="12px",
    layout_direction="LeftToRight",
    background_color_hover=color.background_light_2, 
    align="center",
    text_color_hover=color.text_light
)

combo = button_template.substitute(
    background_color="transparent",
    padding="0px",
    border="none",
    text_color=color.text_dark,
    border_radius="5px",
    text_size="14px",
    layout_direction="LeftToRight",
    background_color_hover="transparent",
    align="center",
    text_color_hover=color.text_light
)

titlebar_generic = button_template.substitute(
    background_color="transparent",
    padding="6px",
    border="none",
    text_color=color.text_dark,
    border_radius="0px",
    text_size="14px",
    layout_direction="LeftToRight",
    background_color_hover=color.background_light_2,
    align="center",
    text_color_hover=color.text_light
)

titlebar_close = button_template.substitute(
    background_color="transparent",
    padding="6px",
    border="none",
    text_color=color.text_dark,
    border_radius="0px",
    text_size="14px",
    layout_direction="LeftToRight",
    background_color_hover=color.close_red,
    align="center",
    text_color_hover=color.text_light
)










