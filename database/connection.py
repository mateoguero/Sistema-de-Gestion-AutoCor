import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
def get_connection():
    """Establece y retorna la conexión a la base de datos."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
