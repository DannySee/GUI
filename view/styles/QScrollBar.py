import color_palette as color
from string import Template


scrollbar_template = Template(
    """
    QScrollBar:$orientation {
        background: transparent;
        border: none;
        width: 8px;
    }
    QScrollBar::handle:$orientation {
        background: $light_gray_2;
        border-radius: 4px;
        min-height: 20px;
    }
    QScrollBar::handle:$orientation:hover {
        background: $light_gray_3;
    }
    QScrollBar::add-line:$orientation {
        background: none;
        height: 0px;
    }
    QScrollBar::sub-line:$orientation {
        background: none;
        height: 0px;
    }
    QScrollBar::add-page:$orientation {
        background: transparent; 
    }
    QScrollBar::sub-page:$orientation {
        background: transparent; 
    }
    """
)

vertical = scrollbar_template.substitute(
    orientation="vertical", 
    light_gray_2=color.light_gray_2, 
    light_gray_3=color.light_gray_3
)

horizontal = scrollbar_template.substitute(
    orientation="horizontal", 
    light_gray_2=color.light_gray_2, 
    light_gray_3=color.light_gray_3
)
