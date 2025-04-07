from google.cloud import bigquery
from pandas_gbq import to_gbq
from dotenv import load_dotenv
import os
import streamlit as st

class StorageData():

    def __init__(self):
        load_dotenv()
        creds_json = st.secrets["gcp_credentials"]["credential_json"]
        _, self.temp_cred_path = tempfile.mkstemp(suffix=".json")
        with open(self.temp_cred_path, "w") as f:
            json.dump(json.loads(creds_json), f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.temp_cred_path
        self.project_id = json.loads(creds_json)["project_id"]

    def store(self, data, table_name, dataset_name="Database"):
        full_table_id = f"{dataset_name}.{table_name}"
        to_gbq(data, full_table_id, project_id=self.project_id, if_exists='replace')
