from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import QItemSelectionModel
from app_view.style_sheets import universal_style, label_style, list_style, button_style
from app_view.widgets.button_widget import ButtonWidget
from app_view.widgets.frame_widget import FrameWidget
from app_view.widgets.list_widget import ListWidget
from app_view.widgets.label_widget import LabelWidget
from app_view.widgets.layout_widget import VerticalBox, HorizontalBox


class SlicerSettingsPopup(QMessageBox): 
    def __init__(self, all_fields, slicer_fields):
        super().__init__()
        self.all_fields, self.slicer_fields = self.get_model(all_fields, slicer_fields)
        self.init_ui()

    def init_ui(self):


        # ------------------------------------ positional button bindings ------------------------------------
        def position_top_binding():
            selected = self.selected_field_list.selectionModel().selectedRows()
            if selected:
                selected_row = selected[0].row()

                if selected_row > 0:
                    item = self.slicer_fields.takeItem(selected_row)  # Remove the item from the source position
                    self.slicer_fields.insertRow(0, item)  # Insert the item at the destination
                    self.slicer_fields.removeRow(selected_row + 1)
                    index = self.slicer_fields.indexFromItem(item)
                    self.selected_field_list.selectionModel().select(index, QItemSelectionModel.SelectionFlag.Select)


        def position_up_binding():
            selected = self.selected_field_list.selectionModel().selectedRows()
            if selected:
                selected_row = selected[0].row()

                if selected_row > 0:
                    item = self.slicer_fields.takeItem(selected_row)  # Remove the item from the source position
                    self.slicer_fields.insertRow(selected_row - 1, item)  # Insert the item at the destination
                    self.slicer_fields.removeRow(selected_row + 1)
                    index = self.slicer_fields.indexFromItem(item)
                    self.selected_field_list.selectionModel().select(index, QItemSelectionModel.SelectionFlag.Select)


        def position_down_binding():
            selected = self.selected_field_list.selectionModel().selectedRows()
            if selected:
                selected_row = selected[0].row()

                if selected_row + 1 < self.slicer_fields.rowCount():
                    item = self.slicer_fields.takeItem(selected_row)  # Remove the item from the source position
                    self.slicer_fields.insertRow(selected_row + 2, item)  # Insert the item at the destination
                    self.slicer_fields.removeRow(selected_row)
                    index = self.slicer_fields.indexFromItem(item)
                    self.selected_field_list.selectionModel().select(index, QItemSelectionModel.SelectionFlag.Select)


        def position_bottom_binding():
            selected = self.selected_field_list.selectionModel().selectedRows()
            if selected:
                selected_row = selected[0].row()

                if selected_row < self.slicer_fields.rowCount():
                    item = self.slicer_fields.takeItem(selected_row)  # Remove the item from the source position
                    self.slicer_fields.appendRow(item)  # Insert the item at the destination
                    self.slicer_fields.removeRow(selected_row)
                    index = self.slicer_fields.indexFromItem(item)
                    self.selected_field_list.selectionModel().select(index, QItemSelectionModel.SelectionFlag.Select)


        # ------------------------------------ selection button bindings ------------------------------------
        def add_button_binding():
            selected = self.all_field_list.selectedIndexes()

            if selected != []:
                self.slicer_fields.appendRow(QStandardItem(selected[0].data()))
                self.all_fields.removeRow(self.all_field_list.selectionModel().selectedRows()[0].row())
                self.remove_button.setEnabled(True)
                self.remove_all_button.setEnabled(True)

                if self.slicer_fields.rowCount() == 5:
                    self.add_button.setEnabled(False)
                

        def remove_button_binding():
            selected = self.selected_field_list.selectedIndexes()

            if selected != []:
                self.all_fields.appendRow(QStandardItem(selected[0].data()))
                self.slicer_fields.removeRow(self.selected_field_list.selectionModel().selectedRows()[0].row())
                self.add_button.setEnabled(True)

                if self.slicer_fields.rowCount() == 0:
                    self.remove_button.setEnabled(False)
                    self.remove_all_button.setEnabled(False)


        def remove_all_button_binding():
            row_count = self.slicer_fields.rowCount()
            for _ in range(row_count):
                item = self.slicer_fields.item(0)  # Always get the first item since the list will reduce in size with each iteration
                self.all_fields.appendRow(QStandardItem(item.text()))
                self.slicer_fields.removeRow(0)  

            self.add_button.setEnabled(True)
            self.remove_button.setEnabled(False)
            self.remove_all_button.setEnabled(False)


        # ------------------------------------ popup contents ------------------------------------

        # popup configuration
        self.setWindowTitle("Modify Quick Slicers")
        self.setStandardButtons(QMessageBox.StandardButton.Apply | QMessageBox.StandardButton.Cancel)
        self.setDefaultButton(QMessageBox.StandardButton.Cancel)
        self.setStyleSheet(universal_style.light_gray_2)
        self.setLayout(VerticalBox())

        # popup header and spacer
        popup_label = LabelWidget(label_style.text_bright, "Select (5) Quick Slicer fields to display in the sidebar.")
        self.layout().addWidget(popup_label)
        self.layout().addSpacing(10)

        # layout to hold widgets
        main_layout = HorizontalBox(spacing=5)
        self.layout().addLayout(main_layout)

        # list view to display all available fields
        self.all_field_list = ListWidget(list_style.list, self.all_fields, fixed_width=200, fixed_height=300)
        main_layout.addWidget(self.all_field_list)
        
        # layout to hold selection buttons
        selection_layout = VerticalBox(spacing=5)
        main_layout.addLayout(selection_layout)

        # selection buttons and stretch spacers to center buttons 
        selection_layout.addStretch()
        self.add_button = ButtonWidget(button_style.discrete, icon="ui_elements/icons/chevron-right.svg", enabeld=False)
        self.add_button.clicked.connect(add_button_binding)
        selection_layout.addWidget(self.add_button)
        self.remove_button = ButtonWidget(button_style.discrete, icon="ui_elements/icons/chevron-left.svg")
        self.remove_button.clicked.connect(remove_button_binding)
        selection_layout.addWidget(self.remove_button)
        self.remove_all_button = ButtonWidget(button_style.discrete, icon="ui_elements/icons/double-chevron-left.svg")
        self.remove_all_button.clicked.connect(remove_all_button_binding)
        selection_layout.addWidget(self.remove_all_button)
        selection_layout.addStretch()

        # list view to display selected slicer fields
        self.selected_field_list = ListWidget(list_style.list, self.slicer_fields, fixed_width=200, fixed_height=300)
        main_layout.addWidget(self.selected_field_list)

        # layout to hold positional buttons
        position_layout = VerticalBox(spacing=5)
        main_layout.addLayout(position_layout)

        # positional buttons and stretch spacers to center buttons
        position_layout.addStretch()
        position_top_button = ButtonWidget(button_style.discrete, icon="ui_elements/icons/double-chevron-up.svg")
        position_top_button.clicked.connect(position_top_binding)
        position_layout.addWidget(position_top_button)
        position_up_button = ButtonWidget(button_style.discrete, icon="ui_elements/icons/chevron-up.svg")
        position_up_button.clicked.connect(position_up_binding)
        position_layout.addWidget(position_up_button)
        position_down_button = ButtonWidget(button_style.discrete, icon="ui_elements/icons/chevron-down.svg")
        position_down_button.clicked.connect(position_down_binding)
        position_layout.addWidget(position_down_button)
        position_bottom_button = ButtonWidget(button_style.discrete, icon="ui_elements/icons/double-chevron-down.svg")
        position_bottom_button.clicked.connect(position_bottom_binding)
        position_layout.addWidget(position_bottom_button)
        position_layout.addStretch()


    def get_model(self, all_fields: list[str], slicer_fields: list[str]) -> QStandardItemModel:
        
        # create models
        all_field_model = QStandardItemModel()
        slicer_model = QStandardItemModel()

        # divide fields into appropriate models
        for field in all_fields:
            item = QStandardItem(field)
            if field in slicer_fields:
                slicer_model.appendRow(item)
            else:
                all_field_model.appendRow(item)

        return all_field_model, slicer_model