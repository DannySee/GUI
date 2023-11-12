import app_view.style_sheets.color_palette as color
from string import Template


filter = Template(
    """
    QFrame {
        background-color: $background_light_1;
        border-radius: 10px;
        border:1px solid $background_bright;
    }      
    """
).substitute(background_light_1=color.background_light_1, 
             background_bright=color.background_bright)

