from database.connection import get_connection
def obtener_clientes():
    """Retorna todos los clientes registrados."""
    conn = get_connection()
    if not conn:
        return []
 
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Documento, Nombre, Apellido, Telefono, Email FROM Cliente")
    registros = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return registros

def insertar_cliente(documento, nombre, apellido, telefono, email):
    """Inserta un nuevo cliente en la base de datos."""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO Cliente (Documento, Nombre, Apellido, Telefono, Email) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (documento, nombre, apellido, telefono, email))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al guardar cliente: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
—--------------------------------------------------------------------------------------------------------- 
utils/validators.py 
import re

def validar_documento(doc):
    """Verifica que el documento contenga solo dígitos y tenga longitud válida."""
    doc_str = str(doc).strip()
    return doc_str.isdigit() and 7 <= len(doc_str) <= 11

def validar_email(email):
    """Validación básica de estructura de correo electrónico."""
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(patron, email.strip()))
