from __future__ import annotations
from typing import Protocol
from app_view.ui_map import combo_map, navi_map
from app_view.widgets.dialog_widget import SlicerSettingsDialog, UnsavedChangesDialog, QIcon
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QTimer
import pandas as pd  


class Model(Protocol):
    def get_user_options(self) -> dict:
        ...
    def get_table_model(self, table: str) -> object:
        ...
    def update_table_model(self, df: pd.DataFrame) -> object:
        ...
    def update_user_options(self, option: str, options: list[str]) -> None:
        ...
    def reset_user_profile(self, option: str) -> None:
        ...
    def save_changes(self) -> None:
        ...
    def clear_changes(self) -> None:
        ...
    def get_table_changes(self) -> dict:
        ...
    def get_table_data(self) -> pd.DataFrame:
        ...


class View(Protocol):
    def init_ui(self, presenter: Presenter) -> None:
        ...
    def collapse_sidebar(self) -> None:
        ...
    def expand_sidebar(self) -> None:
        ...
    def update_navigation(self) -> None:
        ...
    def toggle_navi_selection(self, selection: object) -> None:
        ...
    def populate_combo(self, label: str, icon: QIcon, options: list[str]) -> None:
        ...
    def toggle_combo_focus(self, active: bool) -> None:
        ...
    def populate_slicers(self, slicers: list[str]) -> None:
        ...
    def toggle_clear_slicer_visibility(self, visible: bool) -> None:
        ...
    def clear_slicers(self) -> None:
        ...
    def toggle_slicer_visibility(self, visible: bool) -> None:
        ...
    def update_header(self, text: str) -> None:
        ...
    def update_sub_header(self, text: str) -> None:
        ...
    def toggle_page_visibility(self, visible: bool) -> None:
        ...
    def populate_table(self, model: object) -> None:
        ...
    def expand_filters(self, fields: list[str], filter_map: dict, binding: callable) -> None:
        ...
    def collapse_filters(self) -> None:
        ...
    def toggle_clear_filter_visibility(self, visible: bool) -> None:
        ...
    def clear_filters(self) -> None:
        ...
    def set_save_status(self, message: str, indicator: ['red','yellow','green']) -> None:
        ...
    def reset_save_status(self) -> None:
        ...
    def set_table_status(self, message: str) -> None:
        ...
    def set_refresh_state(self, message: str) -> None:
        ...
    def toggle_status_bar_visibility(self, visible: bool) -> None:
        ...
    def toggle_save(self, enabled: bool) -> None:
        ...
    def populate_toolbox(self, tools: dict=None) -> None:
        ...
    def collapse_toolbox(self) -> None:
        ...


class Presenter:
    def __init__(self, model: Model, view: View) -> None:
        super().__init__()

        # model and view references
        self.model = model
        self.view = view

        # -------------------- ui state trackers --------------------

        # navigation
        self.navi_selection = None
        self.navi_map = {}

        # filters
        self.filtered_data = None
        self.filter_map = {}

        # slicers
        self.sliced_data = None
        self.slicer_map = {}

        # menu
        self.combo_map = {}
        self.toolbox_collapsed = True

        # active states
        self.filters_collapsed = True
        self.sidebar_collapsed = False
        self.binding_callable = True


    # ------------------------ helper functions ------------------------
    def free_filters(self) -> None: 
        self.filtered_data = None
        self.filter_map = {}


    def free_slicers(self) -> None: 
        self.sliced_data = None
        self.slicer_map = {}


    def handle_unsaved_changes(self) -> None:
        if self.model.get_table_changes() != {}: 

            # save or discard changes
            if UnsavedChangesDialog().exec() == 1: 
                self.save_table()
            else:
                self.show_slicers_hide_filters()
                self.view.reset_save_status()
                self.model.clear_changes()
                self.view.toggle_save(False)


    def set_table_data(self, df: pd.DataFrame=None) -> None:

        # get table model and set binding 
        table_model = self.model.get_table_model(self.combo_map["table"]) if df is None else self.model.update_table_model(df)
        table_model.dataChanged.connect(self.changes_made)

        # update table
        self.view.populate_table(table_model)

        # update status bar with row count
        self.view.set_table_status(f"Rows: {table_model.rowCount(0)}   Columns: {table_model.columnCount(0)}")


    def save_table(self) -> None:

        # set status message
        QTimer.singleShot(0, lambda: self.view.set_save_status("Saving changes...", "yellow"))

        # synch table changes to server
        self.model.save_changes()

        # update status message with successful save message and then clear the status
        QTimer.singleShot(500, lambda: self.view.set_save_status("Changes saved!", "green"))
        QTimer.singleShot(2000, self.view.reset_save_status)

        # disable save button 
        self.view.toggle_save(False)


    def reset_page_input(self) -> None:

        # reset slicer ui state tracker and visibility
        if self.slicer_map != {}:
            self.free_slicers()
            self.view.toggle_clear_slicer_visibility(False)
            self.view.clear_slicers()

        # reset filter ui state tracker and visibility
        if self.filtered_data is not None:
            self.free_filters()
            self.view.toggle_clear_filter_visibility(False)
        if not self.filters_collapsed:
            self.show_slicers_hide_filters()

    
    def show_slicers_hide_filters(self) -> None:
        if not self.filters_collapsed:
            if not self.sidebar_collapsed: self.view.toggle_slicer_visibility(True)
            self.view.collapse_filters()
            self.filters_collapsed = True


    # ------------------------ model listeners ------------------------
    def changes_made(self) -> None:
        self.view.set_save_status("Unsaved changes", "yellow")
        self.view.toggle_save(True)


    # ------------------------ view bindings ------------------------
    def collapser_binding(self):
        if self.binding_callable:
            self.binding_callable = False

            # toggle sidebar visibility vased on current state
            if self.sidebar_collapsed:
                self.view.expand_sidebar()
                if self.filters_collapsed and self.combo_map != {}: self.view.toggle_slicer_visibility(True)
                self.sidebar_collapsed = False
            else:
                self.view.collapse_sidebar()
                self.sidebar_collapsed = True
                if not self.toolbox_collapsed:
                    self.view.collapse_toolbox()
                    self.toolbox_collapsed = True

            self.binding_callable = True


    def navigation_binding(self):
        if self.binding_callable:
            self.binding_callable = False
                
            # do not proceed if selection is already active
            if self.view.sender() is not self.navi_selection:
                self.navi_selection = self.view.sender()
                self.navi_map = navi_map[self.view.sender().objectName()]
                self.combo_map = {}

                # --------------------- handle unsaved changes ---------------------
                self.handle_unsaved_changes()

                # --------------------- update sidebar ---------------------

                # navigation
                self.view.toggle_navi_selection(self.view.sender())

                # combo box
                self.view.toggle_combo_focus(False)
                self.view.populate_combo(self.navi_map["text"], QIcon(self.navi_map["icon"]), self.navi_map["options"])

                # reset toolbox
                if not self.toolbox_collapsed:
                    self.view.collapse_toolbox()
                    self.toolbox_collapsed = True

                #slicers
                self.view.toggle_slicer_visibility(False)

                # ----------------------- update page -----------------------

                # update page label and hide sub label
                self.view.update_header(self.navi_map["page_header"])
                self.view.toggle_page_visibility(False)

                # -------------------- update status bar ---------------------
                self.view.toggle_status_bar_visibility(False)

            self.binding_callable = True


    def combo_binding(self):
        if self.binding_callable:
            self.binding_callable = False

            # --------------------- save table changes ---------------------
            self.handle_unsaved_changes()

            # --------------------- update ui state ---------------------
            self.combo_map = combo_map[self.view.sender().currentText()]

            # ----------------------- update page -----------------------

            # update page sub header label and visibility
            self.view.update_sub_header(self.combo_map["sub_header"])
            self.view.toggle_page_visibility(True)

            # update table data
            self.set_table_data()

            # ---------------------- update sidebar ----------------------

            # update combo box style
            self.view.toggle_combo_focus(True)

            # populate slicers options and hide clear button
            slicers = self.model.get_user_options()["slicers"]
            self.view.populate_slicers(slicers)
            if not self.sidebar_collapsed: self.view.toggle_slicer_visibility(True)

            # ----------------------- update status bar -----------------------
            self.view.set_refresh_state(f"Last Refresh: {pd.Timestamp.now().day_name()} {pd.Timestamp.now().strftime('%I:%M %p')}")
            self.view.toggle_status_bar_visibility(True)

            # -------------- reset all page input (filter/slicer) --------------
            self.reset_page_input()

            self.binding_callable = True


    def slicer_binding(self):
        if self.binding_callable:
            self.binding_callable = False

            # get slicer field and value
            slicer = self.view.sender()
            field = slicer.placeholderText()
            value = slicer.text()

            # update slicer map
            if value == "": 
                self.slicer_map.pop(field)
            else:
                self.slicer_map[field] = value

            # update filtered table dataframe and clear slicer visibility
            df = self.filtered_data if self.filtered_data is not None else self.model.get_table_data()
            if len(self.slicer_map) > 0:

                # show clear slicer button and create sliced dataframe
                self.view.toggle_clear_slicer_visibility(True)
                for field, value in self.slicer_map.items():
                    df = df[df[field].str.contains(value, case=False)]
            else:

                # hide clear slicer button and reset filtered dataframe
                self.view.toggle_clear_slicer_visibility(False)

            # update ui state tracker
            self.sliced_data = df

            # refresh model and update table
            self.set_table_data(df)

            self.binding_callable = True


    def clear_slicer_binding(self):
        if self.binding_callable:
            self.binding_callable = False

            # update ui state tracker
            self.free_slicers()

            # clear all slicer fields
            self.view.clear_slicers()

            # refresh model and update table
            df = self.filtered_data if self.filtered_data is not None else self.model.get_table_data()
            self.set_table_data(df)

            self.binding_callable = True


    def slicer_settings_binding(self):
        if self.binding_callable:
            self.binding_callable = False

            # get slicer fields and all fields from active table
            slicers = self.model.get_user_options()["slicers"]
            all_fields = self.model.get_table_data().columns.tolist()
        
            # create popup dialog
            popup = SlicerSettingsDialog(all_fields, slicers)

            # update model based on new user selections
            if popup.exec() == 1:

                # get updated user selections
                fields = popup.get_slicers_options()

                # udpdate user options as designated by user
                if fields is not None:

                    # save user options
                    self.model.update_user_options("slicers", fields)
                else:
                    
                    # reset user options
                    fields = self.model.reset_user_profile("slicers")

                # update ui with selected slicers
                self.view.populate_slicers(fields)

            self.binding_callable = True


    def save_binding(self) -> None:
        if self.binding_callable:
            self.binding_callable = False
            self.save_table()
            self.binding_callable = True


    def import_binding(self) -> None:
        pass


    def export_binding(self) -> None:
        pass


    def filter_toggle_binding(self) -> None:
        if self.binding_callable:
            self.binding_callable = False

            # expand or collapse filter pane depending on current state. 
            if self.filters_collapsed:

                # transfer slicer values to filter map
                if self.slicer_map != {}:
                    self.filtered_data = self.sliced_data
                    for field, value in self.slicer_map.items():
                        if field not in self.filter_map: self.filter_map[field] = value

                    # update ui state tracker
                    self.free_slicers()

                    # show clear filter button and clear slicers
                    self.view.toggle_clear_filter_visibility(True)
                    self.view.clear_slicers()

                # hide slicers
                self.view.toggle_slicer_visibility(False)

                # expand filters and populate filter fields
                fields = self.model.get_table_data().columns.tolist()
                self.view.expand_filters(fields, self.filter_map, self.filter_binding)

                # update ui state tracker
                self.filters_collapsed = False
            else:
                # collapse filters and show slicers
                self.show_slicers_hide_filters()
                

            self.binding_callable = True


    def filter_binding(self) -> None:
        if self.binding_callable:
            self.binding_callable = False

            # get filter filed and value
            filter = self.view.sender()
            field = filter.placeholderText()
            value = filter.text()

            # update filter map 
            if value == "":
                self.filter_map.pop(field)
            else:
                self.filter_map[field] = value
                
            # update filtered table dataframe and clear filter visibility
            df = self.model.get_table_data()
            if len(self.filter_map) > 0:

                # show clear filter button and create filtered dataframe
                self.view.toggle_clear_filter_visibility(True)
                for field, value in self.filter_map.items():
                    df = df[df[field].str.contains(value, case=False)]
            else:

                # hide clear filter button and reset filtered dataframe
                self.view.toggle_clear_filter_visibility(False)

            # update ui state tracker
            self.filtered_data = df

            # refresh model and update table
            self.set_table_data(df)

            self.binding_callable = True


    def clear_filter_binding(self) -> None:
        if self.binding_callable:
            self.binding_callable = False

            # update ui state tracker
            self.free_filters()
        
            # reset ui widgets (clear filters and hid clear button)
            self.view.toggle_clear_filter_visibility(False)
            self.view.clear_filters()

            # get clean dataframe
            df = self.model.get_table_data()
            if self.slicer_map != {}:
                for field, value in self.slicer_map.items():
                    df = df[df[field].str.contains(value, case=False)]

            # refresh model and update table
            self.set_table_data(df)

            self.binding_callable = True


    def refresh_binding(self) -> None:
        if self.binding_callable:
            self.binding_callable = False

            # handle unsaved changes
            self.handle_unsaved_changes()

            # reset page input (filter/slicer)
            self.reset_page_input()

            # refresh model and update timestamp
            self.set_table_data()
            self.view.set_refresh_state(f"Last Refresh: {pd.Timestamp.now().day_name()} {pd.Timestamp.now().strftime('%I:%M %p')}")

            self.binding_callable = True


    def toolbox_binding(self) -> None:
        if self.binding_callable:
            self.binding_callable = False

            if self.toolbox_collapsed:
                self.view.populate_toolbox()
                self.toolbox_collapsed = False

                if self.sidebar_collapsed:
                    self.view.expand_sidebar()
                    self.sidebar_collapsed = False
            else:
                self.view.collapse_toolbox()
                self.toolbox_collapsed = True

            self.binding_callable = True

   
    # ------------------------ initiate view ------------------------
    def run(self):
        if self.binding_callable:
            self.binding_callable = False

            self.view.init_ui(self)
            self.view.show()

            self.binding_callable = True


   