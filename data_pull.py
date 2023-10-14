import data_centers as db
import pandas as pd


def get_cal_programs():

    with db.sql_server.begin() as connection:
        df = pd.read_sql(f"SELECT * FROM CAL_Programs ORDER BY PRIMARY_KEY DESC", connection)
        df.fillna("", inplace=True)


    print(df)


get_cal_programs()
