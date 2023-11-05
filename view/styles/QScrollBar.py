
import color_palette as color
from string import Template

vertical_scrollbar = Template(
    """
    QScrollBar:vertical {
        background: transparent;
        border: none;
        width: 8px;
    }
    QScrollBar::handle:vertical {
        background: $light_gray_2;
        border-radius: 4px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background: $light_gray_3;
    }
    QScrollBar::add-line:vertical {
        background: none;
        height: 0px;
    }
    QScrollBar::sub-line:vertical {
        background: none;
        height: 0px;
    }
    QScrollBar::add-page:vertical {
        background: transparent; 
    }
    QScrollBar::sub-page:vertical {
        background: transparent; 
    }
    """
).substitute(light_gray_2=color.light_gray_2, light_gray_3=color.light_gray_3)

horizontal_scrollbar =  Template(
    """
    QScrollBar:horizontal {
        background: transparent;
        height: 8px;
        border: none;
    }
    QScrollBar::handle:horizontal {
        background: light_gray_2;
        border-radius: 4px;
        min-width: 20px;
    }
    QScrollBar::handle:horizontal:hover {
        background: light_gray_3;
    }
    QScrollBar::add-line:horizontal {
        background: none;
        width: 0;
    }
    QScrollBar::sub-line:horizontal {
        background: none;
        width: 0;
    }
    QScrollBar::add-page:horizontal {
        background: transparent; /* Customize the background color of the track */
    }
    QScrollBar::sub-page:horizontal {
        background: transparent; /* Customize the background color of the track */
    }
    """
).substitute(light_gray_2=color.light_gray_2, light_gray_3=color.light_gray_3)