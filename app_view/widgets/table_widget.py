from PyQt6.QtWidgets import QTableView, QSizePolicy, QStyledItemDelegate, QLineEdit
from PyQt6.QtCore import Qt


class TableWidget(QTableView):
    def __init__(self, style_sheet, vertical_scroll_style=None, horizontal_scroll_style=None, visible=True,
                 vertical_policy=QSizePolicy.Policy.Expanding, horizontal_policy=QSizePolicy.Policy.Expanding, minimum_height=300):
        super().__init__()

        class CustomDelegate(QStyledItemDelegate):
            def __init__(self, style_sheet):
                super().__init__()
                self.style_sheet = style_sheet

            def createEditor(self, parent, option, index):
                editor = super().createEditor(parent, option, index)
                self.applyStyleSheetAndValueIfLineEdit(editor, index)
                return editor

            def setEditorData(self, editor, index):
                if not isinstance(editor, QLineEdit):
                    super().setEditorData(editor, index)

            def setModelData(self, editor, model, index):
                if isinstance(editor, QLineEdit):
                    model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)
                else:
                    super().setModelData(editor, model, index)

            def applyStyleSheetAndValueIfLineEdit(self, editor, index):
                if isinstance(editor, QLineEdit):
                    editor.setStyleSheet(self.style_sheet)
                    value = index.data(Qt.ItemDataRole.EditRole) or index.data(Qt.ItemDataRole.DisplayRole)
                    editor.setText(value)

        self.verticalHeader().setVisible(False) 
        self.setSizePolicy(horizontal_policy, vertical_policy)
        self.setMinimumHeight(minimum_height)
        self.setStyleSheet(style_sheet)
        self.setItemDelegate(CustomDelegate(style_sheet))
        self.setVisible(visible)

        if style_sheet is not None: self.setStyleSheet(style_sheet)
        if vertical_scroll_style is not None: self.verticalScrollBar().setStyleSheet(vertical_scroll_style)
        if horizontal_scroll_style is not None: self.horizontalScrollBar().setStyleSheet(horizontal_scroll_style)





