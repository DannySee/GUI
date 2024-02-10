from PyQt6.QtWidgets import QComboBox , QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import QSize


class ComboBoxWidget(QComboBox):
    def __init__(self, style_sheet, placeholder, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet(style_sheet)
        self.setPlaceholderText(placeholder)


    def showPopup(self):
        # Call the base class method to handle the popup
        super().showPopup()

        # Calculate the width required to display the longest item
        width = self.dropdownWidth()
        # Set the width of the dropdown list
        self.view().setMinimumWidth(width)

    def dropdownWidth(self):
        # Get the font metrics for the current font of the combobox
        font_metrics = self.fontMetrics()
        # Initialize the maximum width
        max_width = 0
        # Iterate over all items to find the maximum width
        for i in range(self.count()):
            # Calculate the width of the text of the current item
            option_width = font_metrics.horizontalAdvance(self.itemText(i))
            # Update the maximum width if the current item's width is larger
            max_width = max(max_width, option_width)
        # Add some extra space to ensure the text fits well
        extra_padding = 20
        return max_width + extra_padding