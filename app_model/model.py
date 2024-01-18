from PyQt6 import QtCore
from PyQt6.QtCore import Qt
import os
import pandas as pd
import json
import shutil
from typing import Union
from datetime import datetime
from argon2 import PasswordHasher


# TEMPORARY
import getpass


class Model:

    def __init__(self):
        super().__init__()
        self.table_data = pd.DataFrame()
        self.table_changes = {}
        self.table = ""
        self.user = getpass.getuser()
        self.ph = PasswordHasher()

    def get_user_options(self):

        # create user profile if it doesn't exist
        if not os.path.exists(f"app_model/custom_options/{self.user}"): self.create_user_profile(self.user)

        # get user defined table options
        with open(f"app_model/custom_options/{self.user}/{self.table}.json", "r") as file:
            options = json.load(file)

        return options
    

    def update_user_options(self, option: str, options: list[str]) -> None:

        # get user defined table options
        with open(f"app_model/custom_options/{self.user}/{self.table}.json", "r") as file:
            table_options = json.load(file)

        # update options
        table_options[option] = options

        # save options
        with open(f"app_model/custom_options/{self.user}/{self.table}.json", "w") as file:
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
        with open(f"app_model/custom_options/{user}/{self.table}.json", "w") as file:
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
        df = pd.read_csv(f"app_model/session_data/{table}.csv", keep_default_na=False)
        self.model = TableModel(df, df, self.table_changes)

        # connect change listener and assign table data
        self.model.dataChanged.connect(self.handle_changes)
        self.table_data = self.model.get_table_data().astype(str)
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


    def export_table_data(self, directory: str) -> None:
        for file in os.listdir(f"app_model/session_data/exports/"):
            if self.table in file: os.remove(f"app_model/session_data/exports/{file}")

        id = str(hash(f"{self.user}{datetime.now()}"))[-6:]
        self.table_data.to_csv(f"app_model/session_data/exports/{self.table}%{id}.csv", index=False)
        self.table_data.to_csv(f"{directory}/{self.table}%{id}.csv", index=False)


    def import_update(self, import_table: pd.DataFrame, export_table: pd.DataFrame) -> int:
        import_table = import_table[import_table.index.isin(export_table.index)] 
        export_table = export_table[export_table.index.isin(import_table.index)]
        updates = export_table.compare(import_table, keep_equal=False)
        if len(updates) > 0: 
            updates = updates.xs('other', axis=1, level=1)

            # to be replaced by server actions
            with open (f"app_model/session_data/{self.table}.csv", "r") as file:
                table_data = pd.read_csv(file, index_col="PRIMARY_KEY")

            for primary_key, row in updates.iterrows():
                for column in row.index:
                    if pd.notna(row[column]): table_data.loc[primary_key, column] = row[column]

            table_data.to_csv(f"app_model/session_data/{self.table}.csv", index=True)

        return len(updates)


    def import_insert(self, import_table: pd.DataFrame) -> int:
        import_table = import_table[import_table.index == ""]
        if len(import_table) > 0:

            with open (f"app_model/session_data/{self.table}.csv", "r") as file:
                table_data = pd.read_csv(file, index_col="PRIMARY_KEY")   

            # insert row in table_data for each row in import_table
            for row in import_table.index:
                table_data.loc[row] = import_table.loc[row]

            table_data.to_csv(f"app_model/session_data/{self.table}.csv", index=True)
            
        return len(import_table)


    def import_delete(self, import_table: pd.DataFrame, export_table: pd.DataFrame) -> int:
        export_table = export_table[export_table.index.isin(import_table.index) == False]
        if len(export_table) > 0:

            primary_keys = export_table.index.tolist()
            with open (f"app_model/session_data/{self.table}.csv", "r") as file:
                table_data = pd.read_csv(file, index_col="PRIMARY_KEY")

            for row in export_table.index:
                table_data.drop(row, inplace=True)

            table_data.to_csv(f"app_model/session_data/{self.table}.csv", index=True)
            
        return len(export_table)

    
    def import_table_data(self, file: str) -> str:

        # ensure import table matches current table
        import_table = file.split("/")[-1].split("%")[0]
        if import_table != self.table: 
            return f"Error: Import table '{import_table}' does not match current table '{self.table}'"

        # check if import data exists in export directory
        import_file = file.split('/')[-1]
        if os.path.exists(f"app_model/session_data/exports/{import_file}"): 
            import_data = pd.read_csv(file, index_col="PRIMARY_KEY")
            export_data = pd.read_csv(f"app_model/session_data/exports/{import_file}", index_col="PRIMARY_KEY")

            ############# update database (this is a temporary mesaure - perminent will be to perform CRUD operations on database) #############
            updates = self.import_update(import_data, export_data)
            print(updates)
            inserts = self.import_insert(import_data)
            print(inserts)
            deletes = self.import_delete(import_data, export_data)
            print(deletes)

            # kill export file
            os.remove(f"app_model/session_data/exports/{import_file}")
            os.remove(file)

        else: 
            return f"Error: '{self.table}' has not been checked out. {import_file}"
        

    def register_user(self, team: str, first_name: str, last_name: str, email: str, network_id: str, sus_id: str, password: str) -> None:

        # user dictionary
        user = {
            "team": team,
            "first_name": first_name.capitalize().replace(" ", ""),
            "last_name": last_name.capitalize().replace(" ", ""),
            "email": email.lower().replace(" ", ""),
            "network_id": network_id.replace(" ", ""),
            "sus_id": sus_id.upper().replace(" ", ""),
            "password": self.ph.hash(password)
        }
       
        # ideally this is a one to one relationship with a database. File for now, but will be replaced by database
        with open(f"app_model/user_profile/users.json", "w") as file:
            json.dump({network_id: user}, file, indent=4)

        # write file to users directory with network_id as file name for auto-login
        with open(f"app_model/user_profile/{network_id}.json", "w") as file:
            json.dump(user, file, indent=4)


    def validate_user(self, email: str, password: str) -> dict:
            
        # ideally this is a one to one relationship with a database. File for now, but will be replaced by database
        try:
            with open(f"app_model/user_profile/users.json", "r") as file:
                users = json.load(file)
        except:
            return {"success": False, "message": "No users found"}

        # check if user exists
        if self.user in users:
            user = users[self.user]

            if user["email"] != email.lower():
                return {"success": False, "message": f"Email not found"}
            try:
                self.ph.verify(user["password"], password)

                # write file to users directory with network_id as file name for auto-login
                with open(f"app_model/user_profile/{self.user}.json", "w") as file:
                    json.dump(user, file, indent=4)

                return {"success": True, "user": user['first_name']}
            except: 
                return {"success": False, "message": f"Incorrect password"}
        else:
            return {"success": False, "message": "User does not exist"}
        

    def get_user_id(self) -> str:
        return self.user
        

    def auto_login(self) -> dict:

        # replace with pull from sql server
        try:
            with open(f"app_model/user_profile/users.json", "r") as file:
                users = json.load(file)
        except:
            return {"success": False}

        # check if user exists in server
        if self.user in users:

            # try to get current user profile
            try:
                with open(f"app_model/user_profile/{self.user}.json", "r") as file:
                    user = json.load(file)
            except:
                return {"success": False}

            # validate user
            if user['password'] == users[self.user]['password']:
                return {"success": True, "user": user['first_name']}
            else:
                return {"success": False}
        else:
            return {"success": False}


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
    
############################## in construction ############################### 
# --------------------------- department classes ---------------------------
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
