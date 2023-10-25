import pyodbc
from pyodbc import Error
from functools import lru_cache


@lru_cache
def create_server_connection(host_name, database, user_name, user_password):
    connection = None
    try:
        connection = pyodbc.connect(
            f'driver={{SQL Server}};server={host_name};database={database};uid={user_name};pwd={user_password}')
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection
