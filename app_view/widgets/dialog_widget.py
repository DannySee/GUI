from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QIcon
from PyQt6.QtCore import QItemSelectionModel
from app_view.style_sheets import universal_style, label_style, list_style, button_style
from app_view.widgets.button_widget import ButtonWidget
from app_view.widgets.frame_widget import FrameWidget
from app_view.widgets.list_widget import ListWidget
from app_view.widgets.label_widget import LabelWidget
from app_view.widgets.layout_widget import VerticalBox, HorizontalBox


class SlicerSettingsDialog(QDialog):
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
                    self.apply_button.setEnabled(True)
                    self.apply_button.setStyleSheet(button_style.dialog_primary)
                    self.add_button.setEnabled(False)
                

        def remove_button_binding():
            selected = self.selected_field_list.selectedIndexes()

            if selected != []:
                self.apply_button.setEnabled(False)
                self.apply_button.setStyleSheet(button_style.dialog_inactive)
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
            self.apply_button.setEnabled(False)
            self.apply_button.setStyleSheet(button_style.dialog_inactive)


        # ------------------------------------ popup contents ------------------------------------

        # popup configuration
        self.setWindowTitle("Modify Quick Slicers")
        self.setStyleSheet(universal_style.light_gray_2)
        self.setLayout(VerticalBox(content_margins=[20,20,20,20], spacing=20))

        # popup header and spacer
        popup_label = LabelWidget(label_style.text_bright, "Select (5) Quick Slicer fields to display in the sidebar.")
        self.layout().addWidget(popup_label)

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
        self.add_button = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/chevron-right.svg"), enabled=False)
        self.add_button.clicked.connect(add_button_binding)
        selection_layout.addWidget(self.add_button)
        self.remove_button = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/chevron-left.svg"))
        self.remove_button.clicked.connect(remove_button_binding)
        selection_layout.addWidget(self.remove_button)
        self.remove_all_button = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/double-chevron-left.svg"))
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
        position_top_button = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/double-chevron-up.svg"))
        position_top_button.clicked.connect(position_top_binding)
        position_layout.addWidget(position_top_button)
        position_up_button = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/chevron-up.svg"))
        position_up_button.clicked.connect(position_up_binding)
        position_layout.addWidget(position_up_button)
        position_down_button = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/chevron-down.svg"))
        position_down_button.clicked.connect(position_down_binding)
        position_layout.addWidget(position_down_button)
        position_bottom_button = ButtonWidget(button_style.discrete, icon=QIcon("app_view/icons/double-chevron-down.svg"))
        position_bottom_button.clicked.connect(position_bottom_binding)
        position_layout.addWidget(position_bottom_button)
        position_layout.addStretch()

        # create layout for buttons
        button_layout = HorizontalBox(spacing=10)
        self.layout().addLayout(button_layout)

        # reset defaults button
        self.reset_button = ButtonWidget(button_style.dialog_tertiary, "Reset Defaults", fixed_width=120)
        self.reset_button.clicked.connect(self.reset_defaults)
        button_layout.addWidget(self.reset_button)

        # add stretch spacer to push remaining buttons to right
        button_layout.addStretch()

        # apply and cancel buttons
        self.apply_button = ButtonWidget(button_style.dialog_inactive, "Apply", fixed_width=80, enabled=False)
        self.apply_button.clicked.connect(self.accepted)
        button_layout.addWidget(self.apply_button)
        self.cancel_button = ButtonWidget(button_style.dialog_secondary, "Cancel", fixed_width=80)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)


    # ------------------------------------ helper methods ------------------------------------
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
    

    def accepted(self) -> None:
        self.slicer_options = [self.slicer_fields.item(row).text() for row in range(self.slicer_fields.rowCount())]
        self.accept()


    def reset_defaults(self) -> None:
        self.slicer_options = None
        self.accept()


    def get_slicers_options(self):
        return self.slicer_options
    

class UnsavedChangesDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.status = None
    

    def init_ui(self):

        # popup configuration
        self.setWindowTitle("Unsaved Changes")
        self.setStyleSheet(universal_style.light_gray_2)
        self.setLayout(VerticalBox(content_margins=[20,20,20,20], spacing=20))

        # popup header
        popup_label = LabelWidget(label_style.text_bright, "You have unsaved changes. Would you like to save them?")
        self.layout().addWidget(popup_label)

        # create layout for buttons
        button_layout = HorizontalBox(spacing=10)
        self.layout().addLayout(button_layout)

        # add stretch spacer to push remaining buttons to right
        button_layout.addStretch()

        # save, discard buttons
        self.save_button = ButtonWidget(button_style.dialog_primary, "Save", fixed_width=80)
        self.save_button.clicked.connect(self.accept)
        button_layout.addWidget(self.save_button)
        self.discard_button = ButtonWidget(button_style.dialog_secondary, "Discard", fixed_width=80)
        self.discard_button.clicked.connect(self.reject)
        button_layout.addWidget(self.discard_button)

        # add stretch to center buttons
        button_layout.addStretch()


