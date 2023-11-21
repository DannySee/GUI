import app_view.style_sheets.color_palette as color

hidden = "background-color: transparent; border: none;"
bright_gray = f"background-color: {color.background_bright}; border: none;"
light_gray_1 = f"background-color: {color.background_light_1}; border: none;"
light_gray_2 = f"background-color: {color.background_light_2}; border: none;"
dark_gray = f"background-color: {color.background_dark}; border: none;"
darkest_gray = f"background-color: {color.background_darkest}; border: none;"

generic_border_pane = f"""
    background-color:{color.background_light_1};
    border:1px solid {color.background_bright};
    border-radius:10px;
"""

generic_border_pane_transparent = f"""
    background-color:{color.background_light_1};
    border:1px solid {color.background_bright};
    border-radius:50px;
"""

hive_segments = f"""
    background-color:{color.hive_orange};
    border:1px solid {color.background_bright};
    border-radius:20px;
"""