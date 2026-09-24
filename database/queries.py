from database.connection import get_connection
from mysql.connector import Error as DBError

# --- CLIENTES ---
def obtener_clientes():
    try:
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Documento, Nombre, Apellido, Telefono, Email FROM Cliente")
        registros = cursor.fetchall()
        cursor.close()
        conn.close()
        return registros
    except Exception as e:
        print(f"Error al obtener clientes: {e}")
        return []

def insertar_cliente(documento, nombre, apellido, telefono, email):
    try:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        sql = "INSERT INTO Cliente (Documento, Nombre, Apellido, Telefono, Email) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (documento, nombre, apellido, telefono, email))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al insertar cliente: {e}")
        return False

# --- VEHÍCULOS ---
def obtener_vehiculos():
    try:
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT v.Patente, v.Marca, v.Modelo, v.Anio, v.Documento_Cliente,
                   CONCAT(c.Nombre, ' ', c.Apellido) AS Dueno
            FROM Vehiculo v
            LEFT JOIN Cliente c ON v.Documento_Cliente = c.Documento
        """
        cursor.execute(sql)
        registros = cursor.fetchall()
        cursor.close()
        conn.close()
        return registros
    except Exception as e:
        print(f"Error al obtener vehículos: {e}")
        return []

def insertar_vehiculo(patente, marca, modelo, anio, doc_cliente):
    try:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        sql = "INSERT INTO Vehiculo (Patente, Marca, Modelo, Anio, Documento_Cliente) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (patente.upper(), marca, modelo, anio, doc_cliente))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al insertar vehículo: {e}")
        return False

# MECANICO

def obtener_mecanicos():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT Id_Mecanico, Nombre, Apellido, Especialidad, Telefono
            FROM Mecanico
        """)
        return cursor.fetchall()

    except Exception as e:
        print(f"Error al obtener mecánicos: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insertar_mecanico(nombre, apellido, especialidad, telefono):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        if not conn:
            return False

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Mecanico
            (Nombre, Apellido, Especialidad, Telefono)
            VALUES (%s, %s, %s, %s)
        """, (nombre, apellido, especialidad, telefono))

        conn.commit()
        return True

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error al insertar mecánico: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# --- REPUESTOS ---
def obtener_repuestos():
    try:
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Codigo_Repuesto, Nombre_Repuesto, Precio, Stock FROM Repuesto")
        registros = cursor.fetchall()
        cursor.close()
        conn.close()
        return registros
    except Exception as e:
        print(f"Error al obtener repuestos: {e}")
        return []

def insertar_repuesto(codigo, nombre, precio, stock):
    try:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        sql = "INSERT INTO Repuesto (Codigo_Repuesto, Nombre_Repuesto, Precio, Stock) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (codigo, nombre, precio, stock))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al insertar repuesto: {e}")
        return False

# --- ÓRDENES DE TRABAJO ---
def crear_orden_trabajo(fecha, observacion, descripcion, mano_obra, patente, id_mecanico, repuestos_usados):
    try:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        sql_orden = """
            INSERT INTO Orden_de_Trabajo
            (Fecha, Observacion, Descripcion_Servicio, Costo_Mano_Obra, Estado, Patente_Vehiculo, Id_Mecanico)
            VALUES (%s, %s, %s, %s, 'En Reparación', %s, %s)
        """
        cursor.execute(sql_orden, (fecha, observacion, descripcion, mano_obra, patente, id_mecanico))
        id_orden = cursor.lastrowid

        sql_detalle = """
            INSERT INTO Orden_Utiliza_Repuesto (Id_Orden, Codigo_Repuesto, Cantidad, Precio_Aplicado)
            VALUES (%s, %s, %s, %s)
        """
        sql_stock = "UPDATE Repuesto SET Stock = Stock - %s WHERE Codigo_Repuesto = %s"

        for r in repuestos_usados:
            cursor.execute(sql_detalle, (id_orden, r["codigo"], r["cantidad"], r.get("precio_aplicado", 0.0)))
            cursor.execute(sql_stock, (r["cantidad"], r["codigo"]))

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al registrar orden de trabajo: {e}")
        return False

# --- MÉTRICAS DASHBOARD ---
def obtener_metricas_dashboard():
    metrics = {"activas": 0, "en_reparacion": 0, "vehiculos": 0, "stock_critico": 0}
    try:
        conn = get_connection()
        if not conn:
            return metrics
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Orden_de_Trabajo WHERE Estado != 'Finalizada'")
        metrics["activas"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Orden_de_Trabajo WHERE Estado = 'En Reparación'")
        metrics["en_reparacion"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT Patente_Vehiculo) FROM Orden_de_Trabajo WHERE Estado != 'Finalizada'")
        metrics["vehiculos"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Repuesto WHERE Stock <= 5")
        metrics["stock_critico"] = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return metrics
    except Exception as e:
        print(f"Error al obtener métricas del dashboard: {e}")
        return metrics