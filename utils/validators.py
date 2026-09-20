import re


def validar_documento(doc):
    """Verifica que el documento contenga solo dígitos y tenga longitud válida."""
    doc_str = str(doc).strip()
    return doc_str.isdigit() and 7 <= len(doc_str) <= 11


def validar_email(email):
    """Validación básica de estructura de correo electrónico."""
    if email is None:
        return False
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(patron, str(email).strip()))
