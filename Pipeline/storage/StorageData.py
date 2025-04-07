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
        self.credentials = service_account.Credentials.from_service_account_file("GCP_key.json")
        self.project_id = self.credentials.project_id
        self.client = bigquery.Client(
            credentials=self.credentials,
            project=self.project_id
        )

    def store(self, data, table_name, dataset_name="Database"):
        full_table_id = f"{dataset_name}.{table_name}"
        to_gbq(data, full_table_id, project_id=self.project_id, if_exists='replace', credentials=self.credentials)
