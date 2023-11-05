
import color_palette as color
from string import Template


splitter_template = Template(
    """
    QSplitter::handle {
        background-color: $background; 
        border: $border;
    } 
    QSplitter {
        background-color: transparent;
        border: none;
    }
    """
)

visible = splitter_template.substitute(
    background=color.background_bright, 
    border="12px transparent"
)

hidden = splitter_template.substitute(
    background="transparent",
    border="none"
)
