import pandas as pd
import numpy as np
import sqlite3

class PipeWalletData():

    def extract(self, path):
        data = pd.read_csv(path)
        return data

    def transform(self, data):
        wallet_data = data.groupby('Ticker').apply(lambda x:
            pd.Series({'Avg_Price': round((x['price_USD'] * x['Number']).sum() / x['Number'].sum(), 2),
                    'Total_Invested': (x['price_USD'] * x['Number']).sum(),
                    'Total_Quantity': x['Number'].sum()
                    })).reset_index()
        total_capital = wallet_data["Total_Invested"].sum()
        wallet_data["Capital %"] = round((wallet_data["Total_Invested"] / total_capital * 100), 2)
        conn = sqlite3.connect("Database/database.db")
        cursor = conn.cursor()
        for index, row in wallet_data.iterrows():
            ticker = row["Ticker"]
            cursor.execute(f"SELECT Close FROM {ticker} ORDER BY Datetime DESC LIMIT 1")
            actual_price = cursor.fetchone()
            actual_price = actual_price[0]
            wallet_data.at[index, "Return"] = round(((actual_price - row["Avg_Price"]) / row["Avg_Price"]) * 100, 2)
        conn.close()
        return wallet_data
