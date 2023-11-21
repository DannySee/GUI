from PyQt6 import QtCore
from PyQt6.QtCore import Qt
import os
import pandas as pd
import json
import shutil

# TEMPORARY
import getpass


class Model:

    def __init__(self):
        super().__init__()
        self.table_data = pd.DataFrame()
        self.table_changes = {}
        self.table = ""

    def get_user_options(self):

        # get user
        user = getpass.getuser()

        # create user profile if it doesn't exist
        if not os.path.exists(f"app_model/custom_options/{user}"): self.create_user_profile(user)

        # get user defined table options
        with open(f"app_model/custom_options/{user}/{self.table}.json", "r") as file:
            options = json.load(file)

        return options
    

    def update_user_options(self, option: str, options: list[str]) -> None:

        # get user
        user = getpass.getuser()

        # get user defined table options
        with open(f"app_model/custom_options/{user}/{self.table}.json", "r") as file:
            table_options = json.load(file)

        # update options
        table_options[option] = options

        # save options
        with open(f"app_model/custom_options/{user}/{self.table}.json", "w") as file:
            json.dump(table_options, file, indent=4)


    def reset_user_profile(self, option: str) -> None:

        # get default defined table options
        with open(f"app_model/custom_options/default/{self.table}.json", "r") as file:
            table_options = json.load(file)
        
        # get default table options
        default_options = table_options[option]

        # get user
        user = getpass.getuser()

        # get user defined table options
        with open(f"app_model/custom_options/{user}/{self.table}.json", "r") as file:
            user_options = json.load(file)

        # update options
        user_options[option] = default_options

        # save user options
        with open(f"app_model/custom_options/{user}/{table}.json", "w") as file:
            json.dump(table_options, file, indent=4)

        return default_options


    def create_user_profile(self, user):

        # copy directory
        os.mkdir(f"app_model/custom_options/{user}")

        # copy all files from default directory to new directory
        for file in os.listdir(f"app_model/custom_options/default/"):
            shutil.copy(f"app_model/custom_options/default/{file}", f"app_model/custom_options/{user}/{file}")


    def handle_changes(self):
        self.table_changes = self.model.get_table_changes()


    def get_table_model(self, table: str) -> object:

        # pull data and create model
        df = pd.read_csv(f"app_model/session_data/{table}.csv").astype(str)
        self.model = TableModel(df, df, self.table_changes)

        # connect change listener and assign table data
        self.model.dataChanged.connect(self.handle_changes)
        self.table_data = self.model.get_table_data()
        self.table = table

        return self.model
    

    def update_table_model(self, df: pd.DataFrame) -> object:

        # update model and assign listener
        self.model = TableModel(df, self.table_data, self.table_changes)
        self.model.dataChanged.connect(self.handle_changes)

        return self.model
    

    def save_changes(self) -> None:

        # this is all temporary - to be replaced by server acctions
        df = pd.read_csv(f"app_model/session_data/{self.table}.csv")

        for row in self.table_changes:
            for col in self.table_changes[row]:
                df.loc[row, col] = self.table_changes[row][col]
                
        df.to_csv(f"app_model/session_data/{self.table}.csv", index=False)

        # This is perminent
        self.clear_changes()


    def get_table_changes(self) -> dict:
        return self.table_changes
    

    def get_table_data(self) -> pd.DataFrame:
        return self.table_data


    def clear_changes(self) -> None:
        self.table_changes = {}


# --------------------------- table model ---------------------------
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, visible_data, table_data, table_changes):
        super().__init__()
        self._data = visible_data
        self.table_data = table_data
        self.table_changes = table_changes

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]
    
    def flags(self, index):
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable
    
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if index.isValid() and role == Qt.ItemDataRole.EditRole:
            row, col = index.row(), index.column()

            # Update data structure if value has changed
            if value != self._data.iat[row, col]:
                self._data.iat[row, col] = value  # Update the pandas DataFrame
                self.dataChanged.emit(index, index)  # Notify listeners that data has been changed

                actual_row = self._data.iloc[row].name
                self.table_data.iat[actual_row, col] = value
                self.handleChanges(actual_row, col, value)
            
                return True
        
        return False
    
    def handleChanges(self, row, col, value):
        if row not in self.table_changes: 
            self.table_changes[row] = {} 

        column_name = self._data.columns[col]  
        self.table_changes[row][column_name] = value  
        print(self.table_changes)


    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

    def get_table_data(self):
        return self.table_data


    def get_table_changes(self):
        return self.table_changes
    
############################## in construction ############################### --------------------------- department classes ---------------------------
class QualityAssuranceToolbox():
    def __init__(self):
        super().__init__()
        self.table = "quality_assurance"
        self.model = Model()
        self.table_model = self.model.get_table_model(self.table)
        self.table_data = self.model.get_table_data()
        self.table_changes = self.model.get_table_changes()
        self.options = self.model.get_user_options()
        self.options = self.options["quality_assurance"]

    def get_table_model(self) -> object:
        return self.table_model
    

    def get_table_data(self) -> pd.DataFrame:
        return self.table_data
    

    def get_table_changes(self) -> dict:
        return self.table_changes
    

    def get_options(self) -> dict:
        return self.options
    

    def update_table_model(self, df: pd.DataFrame) -> object:
        self.table_model = self.model.update_table_model(df)
        return self.table_model
    

    def save_changes(self) -> None:
        self.model.save_changes()
    

    def clear_changes(self) -> None:
        self.model.clear_changes()
    

    def update_user_options(self, option: str, options: list[str]) -> None:
        self.model.update_user_options(option, options)
    

    def reset_user_profile(self, option: str) -> None:
        self.options = self.model.reset_user_profile(option)
