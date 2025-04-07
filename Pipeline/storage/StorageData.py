from google.cloud import bigquery
from google.oauth2 import service_account
from pandas_gbq import to_gbq
from dotenv import load_dotenv
import os
import json
import tempfile
import streamlit as st

class StorageData():

    def __init__(self):
        creds_dict = st.secrets["gcp_credentials"]
        self.credentials = service_account.Credentials.from_service_account_info(creds_dict)
        self.project_id = creds_dict["project_id"]
        self.client = bigquery.Client(
            credentials=self.credentials,
            project=self.project_id
        )

    def store(self, data, table_name, dataset_name="Database"):
        full_table_id = f"{dataset_name}.{table_name}"
        to_gbq(data, full_table_id, project_id=self.project_id, if_exists='replace')
