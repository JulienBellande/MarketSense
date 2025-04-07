import pandas as pd
import numpy as np
from google.cloud import bigquery
import pandas as pd
import os
from dotenv import load_dotenv
from google.cloud import storage
from io import StringIO
import streamlit as st

class PipeWalletData():

    def __init__(self):
        load_dotenv()
        creds_json = st.secrets["gcp_credentials"]["credential_json"]
        _, self.temp_cred_path = tempfile.mkstemp(suffix=".json")
        with open(self.temp_cred_path, "w") as f:
            json.dump(json.loads(creds_json), f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.temp_cred_path
        self.project_id = json.loads(creds_json)["project_id"]
        self.client = bigquery.Client(project=self.project_id)
        self.storage_client = storage.Client()
        self.bucket_name = 'walletbucket'
        self.file_name = 'Wallet.CSV'

    def extract(self, path):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        blob = bucket.blob(self.file_name)
        csv_data = blob.download_as_text()
        data = pd.read_csv(StringIO(csv_data))
        return data

    def transform(self, data):
        wallet_data = data.groupby('Ticker').apply(lambda x:
            pd.Series({'Avg_Price': round((x['price_USD'] * x['Number']).sum() / x['Number'].sum(), 2),
                    'Total_Invested': (x['price_USD'] * x['Number']).sum(),
                    'Total_Quantity': x['Number'].sum()
                    })).reset_index()
        total_capital = wallet_data["Total_Invested"].sum()
        wallet_data["Capital %"] = round((wallet_data["Total_Invested"] / total_capital * 100), 2)
        for index, row in wallet_data.iterrows():
            ticker = row["Ticker"]
            query = f"""
                SELECT Close
                FROM `{self.project_id}.Database.{ticker}`
                ORDER BY Datetime DESC
                LIMIT 1
            """
            price = self.client.query(query).to_dataframe().loc[0, "Close"]
            wallet_data.at[index, "Return"] = round(((price - row["Avg_Price"]) / row["Avg_Price"]) * 100, 2)
        return wallet_data
