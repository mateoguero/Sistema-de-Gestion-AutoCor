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


def actualizar_cliente(documento_original, documento, nombre, apellido, telefono, email):
    """Actualiza los datos de un cliente identificado por su documento original."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        sql = """UPDATE Cliente
                 SET Documento = %s, Nombre = %s, Apellido = %s,
                     Telefono = %s, Email = %s
                 WHERE Documento = %s"""
        cursor.execute(sql, (documento, nombre, apellido, telefono, email, documento_original))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error al actualizar cliente: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# --- eliminar registros
def eliminar_cliente(documento):
    try:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        sql = "DELETE FROM Cliente WHERE Documento = %s"
        cursor.execute(sql, (documento,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al eliminar cliente: {e}")
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
def crear_orden_trabajo(fecha, observacion, descripcion, mano_obra, patente, mecanico, repuestos_usados, estado='En Reparación'):
    estados_validos = {"Pendiente", "En Reparación", "Finalizada", "Cancelada"}
    if estado not in estados_validos:
        return False
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()


        if isinstance(fecha, str) and "/" in fecha:
            partes = fecha.strip().split("/")
            if len(partes) == 3:
                fecha = f"{partes[2]}-{partes[1]}-{partes[0]}"


        sql_orden = """
            INSERT INTO Orden_de_Trabajo
            (Fecha, Observacion, Descripcion_Servicio, Costo_Mano_Obra, Estado, Patente_Vehiculo, Nombre_Mecanico)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_orden, (fecha, observacion, descripcion, mano_obra, estado, patente, mecanico))
        id_orden = cursor.lastrowid


        sql_detalle = """
            INSERT INTO Orden_Utiliza_Repuesto (Id_Orden, Codigo_Repuesto, Cantidad, Precio_aplicado)
            VALUES (%s, %s, %s, %s)
        """
        for r in repuestos_usados:
            cantidad = int(r["cantidad"])
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero")
            if estado != "Cancelada":
                cursor.execute("SELECT Stock FROM Repuesto WHERE Codigo_Repuesto = %s FOR UPDATE", (r["codigo"],))
                inventario = cursor.fetchone()
                if not inventario or inventario[0] < cantidad:
                    raise ValueError(f"Stock insuficiente para el repuesto {r['codigo']}")
                """cursor.execute("UPDATE Repuesto SET Stock = Stock - %s WHERE Codigo_Repuesto = %s", (cantidad, r["codigo"]))"""
            cursor.execute(sql_detalle, (id_orden, r["codigo"], r["cantidad"], r.get("precio_aplicado", 0.0)))

        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error al registrar orden de trabajo: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def actualizar_estado_orden(id_orden, nuevo_estado):
    estados_validos = {"Pendiente", "En Reparación", "Finalizada", "Cancelada"}
    if nuevo_estado not in estados_validos:
        return False
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("SELECT Estado FROM Orden_de_Trabajo WHERE Id_Orden = %s FOR UPDATE", (id_orden,))
        fila = cursor.fetchone()
        if not fila:
            return False
        estado_actual = fila[0]
        if estado_actual == nuevo_estado:
            return True
        cursor.execute("SELECT Codigo_Repuesto, Cantidad FROM Orden_Utiliza_Repuesto WHERE Id_Orden = %s", (id_orden,))
        repuestos = cursor.fetchall()
        if estado_actual != "Cancelada" and nuevo_estado == "Cancelada":
            for codigo, cantidad in repuestos:
                cursor.execute("UPDATE Repuesto SET Stock = Stock + %s WHERE Codigo_Repuesto = %s", (cantidad, codigo))
        elif estado_actual == "Cancelada" and nuevo_estado != "Cancelada":
            for codigo, cantidad in repuestos:
                cursor.execute("SELECT Stock FROM Repuesto WHERE Codigo_Repuesto = %s FOR UPDATE", (codigo,))
                stock = cursor.fetchone()
                if not stock or stock[0] < cantidad:
                    raise ValueError(f"Stock insuficiente para reactivar el repuesto {codigo}")
                cursor.execute("UPDATE Repuesto SET Stock = Stock - %s WHERE Codigo_Repuesto = %s", (cantidad, codigo))
        cursor.execute("UPDATE Orden_de_Trabajo SET Estado = %s WHERE Id_Orden = %s", (nuevo_estado, id_orden))
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error al actualizar estado de orden: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def actualizar_repuestos_orden(id_orden, repuestos_nuevos):
    """Reemplaza los repuestos de una orden y aplica al stock solo las diferencias."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("SELECT Estado FROM Orden_de_Trabajo WHERE Id_Orden = %s FOR UPDATE", (id_orden,))
        orden = cursor.fetchone()
        if not orden:
            return False
        cancelada = orden[0] == "Cancelada"
        cursor.execute("SELECT Codigo_Repuesto, Cantidad FROM Orden_Utiliza_Repuesto WHERE Id_Orden = %s", (id_orden,))
        anteriores = {str(codigo): int(cantidad) for codigo, cantidad in cursor.fetchall()}
        nuevos = {}
        datos_nuevos = {}
        for repuesto in repuestos_nuevos:
            codigo = str(repuesto["codigo"])
            cantidad = int(repuesto["cantidad"])
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero")
            nuevos[codigo] = nuevos.get(codigo, 0) + cantidad
            datos_nuevos[codigo] = repuesto
        if not cancelada:
            for codigo in set(anteriores) | set(nuevos):
                diferencia = nuevos.get(codigo, 0) - anteriores.get(codigo, 0)
                if diferencia > 0:
                    cursor.execute("SELECT Stock FROM Repuesto WHERE Codigo_Repuesto = %s FOR UPDATE", (codigo,))
                    stock = cursor.fetchone()
                    if not stock or stock[0] < diferencia:
                        raise ValueError(f"Stock insuficiente para el repuesto {codigo}")
                    cursor.execute("UPDATE Repuesto SET Stock = Stock - %s WHERE Codigo_Repuesto = %s", (diferencia, codigo))
                elif diferencia < 0:
                    cursor.execute("UPDATE Repuesto SET Stock = Stock + %s WHERE Codigo_Repuesto = %s", (-diferencia, codigo))
        cursor.execute("DELETE FROM Orden_Utiliza_Repuesto WHERE Id_Orden = %s", (id_orden,))
        for codigo, cantidad in nuevos.items():
            repuesto = datos_nuevos[codigo]
            cursor.execute(
                "INSERT INTO Orden_Utiliza_Repuesto (Id_Orden, Codigo_Repuesto, Cantidad, Precio_aplicado) VALUES (%s, %s, %s, %s)",
                (id_orden, codigo, cantidad, repuesto.get("precio_aplicado", 0.0))
            )
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error al actualizar repuestos de la orden: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def obtener_repuestos_orden(id_orden):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT d.Codigo_Repuesto, r.Nombre_Repuesto, d.Cantidad, d.Precio_aplicado
               FROM Orden_Utiliza_Repuesto d
               JOIN Repuesto r ON r.Codigo_Repuesto = d.Codigo_Repuesto
               WHERE d.Id_Orden = %s""", (id_orden,)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener repuestos de orden: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
# --- ELIMINAR ORDEN DE TRABAJO
def eliminar_orden_trabajo(id_orden):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("SELECT Estado FROM Orden_de_Trabajo WHERE Id_Orden = %s FOR UPDATE", (id_orden,))
        orden = cursor.fetchone()
        if not orden:
            return False
        if orden[0] != "Cancelada":
            cursor.execute("SELECT Codigo_Repuesto, Cantidad FROM Orden_Utiliza_Repuesto WHERE Id_Orden = %s", (id_orden,))
            for codigo, cantidad in cursor.fetchall():
                cursor.execute("UPDATE Repuesto SET Stock = Stock + %s WHERE Codigo_Repuesto = %s", (cantidad, codigo))
        cursor.execute("DELETE FROM Orden_Utiliza_Repuesto WHERE Id_Orden = %s", (id_orden,))
        cursor.execute("DELETE FROM Orden_de_Trabajo WHERE Id_Orden = %s", (id_orden,))
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error al eliminar orden de trabajo: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# También necesitamos una función para obtener las órdenes y mostrarlas en la tabla:
def obtener_ordenes_trabajo():
    try:
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT o.Id_Orden, o.Fecha, o.Patente_Vehiculo, o.Nombre_Mecanico,
                   o.Descripcion_Servicio, o.Costo_Mano_Obra, o.Estado
            FROM Orden_de_Trabajo o
        """
        cursor.execute(sql)
        registros = cursor.fetchall()
        cursor.close()
        conn.close()
        return registros
    except Exception as e:
        print(f"Error al obtener órdenes de trabajo: {e}")
        return []
# --- MÉTRICAS DASHBOARD ---
def obtener_metricas_dashboard():
    metrics = {"activas": 0, "en_reparacion": 0, "vehiculos": 0, "stock_critico": 0}
    try:
        conn = get_connection()
        if not conn:
            return metrics
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Orden_de_Trabajo WHERE Estado NOT IN ('Finalizada', 'Cancelada')")
        metrics["activas"] = cursor.fetchone()[0]


        cursor.execute("SELECT COUNT(*) FROM Orden_de_Trabajo WHERE Estado = 'En Reparación'")
        metrics["en_reparacion"] = cursor.fetchone()[0]


        cursor.execute("SELECT COUNT(DISTINCT Patente_Vehiculo) FROM Orden_de_Trabajo WHERE Estado NOT IN ('Finalizada', 'Cancelada')")
        metrics["vehiculos"] = cursor.fetchone()[0]


        cursor.execute("SELECT COUNT(*) FROM Repuesto WHERE Stock <= 5")
        metrics["stock_critico"] = cursor.fetchone()[0]


        cursor.close()
        conn.close()
        return metrics
    except Exception as e:
        print(f"Error al obtener métricas del dashboard: {e}")
        return metrics
