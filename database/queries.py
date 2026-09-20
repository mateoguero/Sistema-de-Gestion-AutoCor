from database.connection import get_connection


def _is_mysql_connection(conn):
    return conn is not None and conn.__class__.__module__.startswith("mysql")


def obtener_clientes():
    """Retorna todos los clientes registrados."""
    conn = get_connection()
    if not conn:
        return []

    try:
        if _is_mysql_connection(conn):
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT Documento, Nombre, Apellido, Telefono, Email FROM Cliente")
            return cursor.fetchall()

        cursor = conn.cursor()
        cursor.execute("SELECT Documento, Nombre, Apellido, Telefono, Email FROM Cliente")
        columnas = ["Documento", "Nombre", "Apellido", "Telefono", "Email"]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    finally:
        conn.close()


def insertar_cliente(documento, nombre, apellido, telefono, email):
    """Inserta un nuevo cliente en la base de datos."""
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        sql = "INSERT INTO Cliente (Documento, Nombre, Apellido, Telefono, Email) VALUES (?, ?, ?, ?, ?)"
        if _is_mysql_connection(conn):
            sql = sql.replace("?", "%s")
        cursor.execute(sql, (documento, nombre, apellido, telefono, email))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al guardar cliente: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
