import app_view.style_sheets.color_palette as color
from string import Template


list = Template(
    """
    QListView {
        background-color: $background_light_1;
        color: $text_light;
        border-radius: 10px;
        border:1px solid $background_bright;
        padding: 5px;                                   
    }
    """
).substitute(background_light_1=color.background_light_1, 
             text_light=color.text_light, 
             background_bright=color.background_bright)

