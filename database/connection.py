import sqlite3
from pathlib import Path

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
except ModuleNotFoundError:
    mysql = None
    MySQLError = Exception

from config import DB_CONFIG


def _sqlite_path():
    """Ruta de la base de datos local de respaldo."""
    base_dir = Path(__file__).resolve().parent.parent
    return str(base_dir / "autocor.db")


def _init_sqlite_schema(connection):
    """Crea las tablas mínimas si la base SQLite aún no existe."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS Cliente (
            Documento TEXT PRIMARY KEY,
            Nombre TEXT NOT NULL,
            Apellido TEXT NOT NULL,
            Telefono TEXT,
            Email TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS Mecanico (
            Id_Mecanico INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            Apellido TEXT NOT NULL,
            Especialidad TEXT,
            Telefono TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS Repuesto (
            Codigo_Repuesto TEXT PRIMARY KEY,
            Nombre_Repuesto TEXT NOT NULL,
            Precio REAL NOT NULL,
            Stock INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS Vehiculo (
            Patente TEXT PRIMARY KEY,
            Marca TEXT NOT NULL,
            Modelo TEXT NOT NULL,
            Anio INTEGER,
            Documento_Cliente TEXT,
            FOREIGN KEY (Documento_Cliente) REFERENCES Cliente(Documento)
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS Orden_de_Trabajo (
            Id_Orden INTEGER PRIMARY KEY AUTOINCREMENT,
            Fecha TEXT NOT NULL,
            Observacion TEXT,
            Descripcion_Servicio TEXT NOT NULL,
            Costo_Mano_Obra REAL NOT NULL,
            Estado TEXT NOT NULL DEFAULT 'Pendiente',
            Patente_Vehiculo TEXT,
            Id_Mecanico INTEGER,
            FOREIGN KEY (Patente_Vehiculo) REFERENCES Vehiculo(Patente),
            FOREIGN KEY (Id_Mecanico) REFERENCES Mecanico(Id_Mecanico)
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS Orden_Utiliza_Repuesto (
            Id_Orden INTEGER,
            Codigo_Repuesto TEXT,
            Cantidad INTEGER NOT NULL,
            PRIMARY KEY (Id_Orden, Codigo_Repuesto),
            FOREIGN KEY (Id_Orden) REFERENCES Orden_de_Trabajo(Id_Orden),
            FOREIGN KEY (Codigo_Repuesto) REFERENCES Repuesto(Codigo_Repuesto)
        )
        """
    )
    connection.commit()


def get_connection():
    """Establece y retorna una conexión a MySQL o a SQLite como respaldo."""
    if mysql is not None:
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            if connection.is_connected():
                return connection
        except MySQLError as e:
            print(f"Error al conectar a MySQL: {e}")

    try:
        connection = sqlite3.connect(_sqlite_path())
        connection.row_factory = sqlite3.Row
        _init_sqlite_schema(connection)
        return connection
    except sqlite3.Error as e:
        print(f"Error al conectar a SQLite: {e}")
        return None
