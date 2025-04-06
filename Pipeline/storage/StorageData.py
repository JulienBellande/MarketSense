from google.cloud import bigquery
from pandas_gbq import to_gbq
from dotenv import load_dotenv
import os


class StorageData():

    def __init__(self):
        load_dotenv()
        self.project_id = os.getenv("GCP_PROJECT_ID")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GCP_CREDENTIALS_PATH")

    def store(self, data, table_name, dataset_name="Database"):
        full_table_id = f"{dataset_name}.{table_name}"
        to_gbq(data, full_table_id, project_id=self.project_id, if_exists='replace')
