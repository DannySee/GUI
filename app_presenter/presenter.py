from __future__ import annotations
from typing import Protocol
from app_view.ui_map import combo_map, navi_map
from app_view.widgets.popup_widget import SlicerSettingsPopup   


class Model(Protocol):
    def get_user_options(self, table: str) -> dict:
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
    def populate_combo(self, label: str, options: list[str]) -> None:
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


class Presenter:
    def __init__(self, model: Model, view: View) -> None:
        super().__init__()

        # model and view references
        self.model = model
        self.view = view

        # ui state trackers
        self.navi_selection = None
        self.navi_map = {}
        self.collapsed = False
        self.combo_selection = None
        self.slicer_map = {}

    
    def collapser_binding(self):

        # toggle sidebar visibility vased on current state
        if self.collapsed:
            self.view.expand_sidebar()
            self.collapsed = False
        else:
            self.view.collapse_sidebar()
            self.collapsed = True


    def navigation_binding(self):

        # do not proceed if selection is already active
        if self.view.sender() is not self.navi_selection:
            
            self.navi_selection = self.view.sender()
            self.navi_map = navi_map[self.view.sender().objectName()]

            # --------------------- update sidebar ---------------------

            # update navigation selection, populate combo box, and toggle visibility
            self.view.toggle_navi_selection(self.view.sender())
            self.view.toggle_combo_focus(False)
            self.view.populate_combo(self.navi_map["text"], self.navi_map["options"])
            self.view.toggle_slicer_visibility(False)

            # ----------------------- update page -----------------------

            # update page label and hid sub label
            self.view.update_header(self.navi_map["page_header"])
            self.view.toggle_page_visibility(False)


    def slicer_binding(self):

        # log slicer input
        slicer = self.view.sender()
        self.slicer_map[slicer.placeholderText()] = slicer.text()
        
        # loop through and apply slicer map
        slices = 0
        for slice in self.slicer_map:
            if self.slicer_map[slice] != "":
                slices += 1
            else:
                pass

        # update clear slicer button visibility
        visible = True if slices > 0 else False
        self.view.toggle_clear_slicer_visibility(visible)


    def clear_slicer_binding(self):

        # clear slicer map and update slicer container visibility
        self.slicer_map = {}
        self.view.clear_slicers()


    def combo_binding(self):

        # do not proceed if there is no selected index
        if self.view.sender().currentIndex() != -1:
            self.combo_selection = self.view.sender().currentText()

            # ---------------------- update sidebar ----------------------

            # get slicer options from model
            table = combo_map[self.combo_selection]["table"]
            slicers = self.model.get_user_options(table)["slicers"]

            # update combo box style
            self.view.toggle_combo_focus(True)

            # populate slicers options and hide clear button
            self.view.populate_slicers(slicers)
            self.view.toggle_clear_slicer_visibility(False)

            # ----------------------- update page -----------------------

            # update page sub header label and visibility
            self.view.update_sub_header(combo_map[self.combo_selection]["sub_header"])
            self.view.toggle_page_visibility(True)
       

    def slicer_settings_binding(self):
        
        popup = SlicerSettingsPopup([1,2,3,4,5],[2,4,5])

        if popup.exec() == SlicerSettingsPopup.StandardButton.Apply:
            print("apply")
        else:   
            print("cancel")

    
    def expand_filter_binding(self) -> None:
        pass


    def filter_binding(self) -> None:
        pass
   

    def run(self):
        self.view.init_ui(self)
        self.view.show()