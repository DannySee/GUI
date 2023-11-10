from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout


class VerticalBox(QVBoxLayout):
    def __init__(self, content_margins=[0,0,0,0], spacing=0, spacer_item=None, alignment=None):
        super().__init__()
        self.setContentsMargins(*content_margins)
        self.setSpacing(spacing)

        if alignment is not None: self.setAlignment(alignment)
        if spacer_item is not None: self.addSpacerItem(spacer_item)

class HorizontalBox(QHBoxLayout):
    def __init__(self, content_margins=[0,0,0,0], spacing=0, spacer_item=None, alignment=None):
        super().__init__()
        self.setContentsMargins(*content_margins)
        self.setSpacing(spacing)

        if alignment is not None: self.setAlignment(alignment)
        if spacer_item is not None: self.addSpacerItem(spacer_item)
