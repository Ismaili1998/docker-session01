import os

from postgres_loader import PostgreSQLDataLoader


print("this is my python app running inside a docker container:")



# Example usage
if __name__ == "__main__":
    loader = PostgreSQLDataLoader(
      host=os.environ.get('DB_HOST', 'localhost'),
      port=int(os.environ.get('DB_PORT', 5432)),
      database=os.environ.get('DB_NAME', 'db'),
      user=os.environ.get('DB_USER', 'postgres_user'),
      password=os.environ.get('DB_PASSWORD', 'root'),
    )

    loader.store_data('./data/data.csv')
    loader.get_table_info()
    loader.close()