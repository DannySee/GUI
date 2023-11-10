import os
import pandas as pd
import json
import shutil

# TEMPORARY
import getpass


"""
def pull_records(table):

    if os.path.exists(f"session_data/{table}.csv"):
        df = pd.read_csv(f"session_data/{table}.csv")

    else:
        with db.sql_server.begin() as connection:
            df = pd.read_sql(f"SELECT * FROM {table} ORDER BY PRIMARY_KEY DESC", connection)
            df.fillna("", inplace=True)

        df.to_csv(f"session_data/{table}.csv", index=False)


    return df
"""

class Model:

    def __init__(self):
        super().__init__()

    def get_user_options(self, table):

        # get user
        user = getpass.getuser()

        # create user profile if it doesn't exist
        if not os.path.exists(f"app_model/custom_options/{user}"): self.create_user_profile(user)

        # get user defined table options
        with open(f"app_model/custom_options/{user}/{table}.json", "r") as file:
            options = json.load(file)

        return options

    def create_user_profile(self, user):

        # copy directory
        os.mkdir(f"app_model/custom_options/{user}")

        # copy all files from default directory to new directory
        for file in os.listdir(f"app_model/custom_options/default/"):
            shutil.copy(f"app_model/custom_options/default/{file}", f"app_model/custom_options/{user}/{file}")

    def get_cal_programs(self, table):
        df = pd.read_csv(f"session_data/{table}.csv")
        return df.astype(str)

    def save_changes(self, table, changes):
        df = pd.read_csv(f"session_data/{table}.csv")
        
        for row in changes:
            for col in changes[row]:
                df.loc[row, col] = changes[row][col]
                
        df.to_csv(f"session_data/{table}.csv", index=False)