import os
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "SistemaAutocor"),
            charset="utf8mb4",
            connection_timeout=10,
            autocommit=False
        )

        if connection.is_connected():
            return connection

        return None

    except Error as error:
        print(f"Error de conexión con MySQL: {error}")
        return None