import app_view.style_sheets.color_palette as color
from string import Template


scrollbar_template = Template(
    """
    QScrollBar:$orientation {
        background: transparent;
        border: none;
        margin: $margin;
        $dimension
    }
    QScrollBar::handle:$orientation {
        background: $light_gray_2;
        border-radius: 4px;
        $min_size
    }
    QScrollBar::handle:$orientation:hover {
        background: $light_gray_3;
    }
    QScrollBar::add-line:$orientation {
        background: transparent;
        $size
    }
    QScrollBar::sub-line:$orientation {
        background: transparent;
        $size
    }
    QScrollBar::add-page:$orientation {
        background: $scroll_background; 
    }
    QScrollBar::sub-page:$orientation {
        background: $scroll_background; 
    }
    """
)

table_vertical = scrollbar_template.substitute(
    dimension="width: 8px;",
    orientation="vertical", 
    light_gray_2=color.light_gray_2, 
    light_gray_3=color.light_gray_3,
    scroll_background=color.background_light_1,
    size="height: 0px;",
    min_size="min-height: 25px;",
    margin="7px 0px 0px 0px;"
)

table_horizontal = scrollbar_template.substitute(
    dimension="height: 8px;",
    orientation="horizontal", 
    light_gray_2=color.light_gray_2, 
    light_gray_3=color.light_gray_3,
    scroll_background=color.background_light_1,
    size="width: 10px;",
    min_size= "min-width: 25px;",
    margin="0px 0px 0px 7px;"
)

list_vertical = scrollbar_template.substitute(
    dimension="width: 8px;",
    orientation="vertical", 
    light_gray_2=color.light_gray_2, 
    light_gray_3=color.light_gray_3,
    scroll_background=color.background_light_1,
    size="height: 0px;",
    min_size="min-height: 25px;",
    margin="0px 0px 0px 0px;"
)

