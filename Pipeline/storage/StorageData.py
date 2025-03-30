import sqlite3


class StorageData():

    def store(self, data, table_name, db_name="Database/database.db"):
        with sqlite3.connect(db_name) as conn:
            data.to_sql(table_name, conn, if_exists='replace', index=True)
