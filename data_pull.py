import data_centers as db
import pandas as pd


def get_cal_programss():

    with db.sql_server.begin() as connection:
        df = pd.read_sql(f"SELECT * FROM CAL_Programs ORDER BY PRIMARY_KEY DESC", connection)
        df.fillna("", inplace=True)


    return df



def get_cal_programs():

    df = pd.read_csv("data.csv")


    return df



