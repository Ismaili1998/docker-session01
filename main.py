from postgres_loader import PostgreSQLDataLoader


print("this is my python app running inside a docker container:")



# Example usage
if __name__ == "__main__":
    loader = PostgreSQLDataLoader(
        host='localhost',
        port=5432,
        database='postgres',
        user='postgres',
        password='postgres',
        table_name='users'
    )

    loader.store_data('./data/data.csv')
    loader.get_table_info()
    loader.close()