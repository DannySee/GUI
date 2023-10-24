import pandas as pd
import os

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


def get_cal_programs(table):

    df = pd.read_csv(f"session_data/{table}.csv")
    return df.astype(str)

def save_changes(table, changes):

    df = pd.read_csv(f"session_data/{table}.csv")
    
    for row in changes:
        for col in changes[row]:
            df.loc[row, col] = changes[row][col]
            
    df.to_csv(f"session_data/{table}.csv", index=False)



