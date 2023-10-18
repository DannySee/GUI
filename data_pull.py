import data_centers as db
import pandas as pd
import os


def pull_records(table):

    if os.path.exists(f"data_tables/{table}.csv"):
        df = pd.read_csv(f"data_tables/{table}.csv")

    else:
        with db.sql_server.begin() as connection:
            df = pd.read_sql(f"SELECT * FROM {table} ORDER BY PRIMARY_KEY DESC", connection)
            df.fillna("", inplace=True)

        df.to_csv(f"data_tables/{table}.csv", index=False)


    return df



def get_cal_programs():

    df = pd.read_csv("data.csv")


    return df



