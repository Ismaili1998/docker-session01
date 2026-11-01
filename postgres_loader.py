import pandas as pd
import psycopg2
from sqlalchemy import create_engine, inspect
from sqlalchemy.types import Integer, String, Float, DateTime
import os


class PostgreSQLDataLoader:


    def __init__(self, host='localhost', port=5432, database='postgres',
                 user='postgres', password='postgres', table_name='data_table'):

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.table_name = table_name
        self.engine = None
        self.df = None

    def connect(self):
        """Establish connection to PostgreSQL database."""
        try:
            connection_string = f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'
            self.engine = create_engine(connection_string)
            print(f" Connected to PostgreSQL at {self.host}:{self.port}/{self.database}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False

    def load_csv(self, csv_path='./data/data.csv'):

        try:
            if not os.path.exists(csv_path):
                print(f"CSV file not found: {csv_path}")
                return None

            self.df = pd.read_csv(csv_path)
            print(f" Loaded CSV: {csv_path} ({len(self.df)} rows, {len(self.df.columns)} columns)")
            print(f"  Columns: {', '.join(self.df.columns.tolist())}")
            return self.df
        except Exception as e:
            print(f"✗ Error loading CSV: {e}")
            return None

    def table_exists(self):
        try:
            inspector = inspect(self.engine)
            exists = self.table_name in inspector.get_table_names()
            if exists:
                print(f" Table '{self.table_name}' already exists")
            return exists
        except Exception as e:
            print(f"✗ Error checking table existence: {e}")
            return False

    def table_has_data(self):
        """Check if table already contains data."""
        try:
            query = f"SELECT COUNT(*) FROM {self.table_name}"
            with self.engine.connect() as conn:
                result = conn.execute(query)
                count = result.fetchone()[0]
                if count > 0:
                    print(f"Table '{self.table_name}' has {count} rows")
                    return True
                return False
        except Exception as e:
            print(f"✗ Error checking table data: {e}")
            return False

    def store_data(self, csv_path='./data/data.csv', if_exists='fail'):
        try:
            # Check connection
            if self.engine is None:
                if not self.connect():
                    return False

            # Load CSV
            if self.df is None:
                if self.load_csv(csv_path) is None:
                    return False

            # Check if table exists and has data
            if self.table_exists():
                if self.table_has_data():
                    print(f"Table '{self.table_name}' already contains data. Skipping insertion.")
                    return True
                else:
                    if_exists = 'append'
                    print(f"Table exists but is empty. Appending data...")
            else:
                if_exists = 'replace'
                print(f"Creating new table '{self.table_name}'...")

            # Store data in PostgreSQL
            self.df.to_sql(self.table_name, self.engine, if_exists=if_exists, index=False)
            print(f"Successfully stored {len(self.df)} rows in table '{self.table_name}'")
            return True

        except Exception as e:
            print(f"Error storing data: {e}")
            return False

    def get_table_info(self):
        """Retrieve and display table information."""
        try:
            query = f"SELECT * FROM {self.table_name} LIMIT 5"
            df = pd.read_sql(query, self.engine)
            print(f"\n Table '{self.table_name}' sample data:")
            print(df.to_string(index=False))
            return df
        except Exception as e:
            print(f" Error retrieving table info: {e}")
            return None

    def close(self):
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            print("Connection closed")



