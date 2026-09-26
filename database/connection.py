import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def get_connection():
    """Establece y retorna una conexión exclusiva con la base de datos MySQL

    utilizando las credenciales importadas desde config.py.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            return connection

        return None

    except Error as error:
        print(f"Error de conexión con MySQL: {error}")
        return None