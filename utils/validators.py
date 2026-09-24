import re

def validar_documento(doc):
    """Verifica que el documento o CUIT contenga solo dígitos y tenga longitud válida."""
    doc_str = str(doc).strip()
    return doc_str.isdigit() and 7 <= len(doc_str) <= 11

def validar_email(email):
    """Validación básica de formato de correo electrónico."""
    if not email or not str(email).strip():
        return True
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(patron, str(email).strip()))

def validar_patente(patente):
    """Valida formato de patentes argentinas (ABC123 o AB123CD)."""
    if not patente:
        return False
    texto = str(patente).strip().upper()
    patron = r"^[A-Z]{3}\d{3}$|^[A-Z]{2}\d{3}[A-Z]{2}$"
    return bool(re.match(patron, texto))

def validar_monto(valor):
    """Valida que un importe o cantidad sea numérico y no negativo."""
    if valor is None:
        return False
    try:
        monto = float(str(valor).replace(",", "."))
        return monto >= 0
    except ValueError:
        return False