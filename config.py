import os
from pathlib import Path

from dotenv import load_dotenv

# Cargar variables desde el archivo .env ubicado junto a este módulo,
# independientemente del directorio desde el que se ejecute la aplicación.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Variables obligatorias: no se usan valores por defecto para credenciales.
_REQUERIDAS = ("DB_USER", "DB_PASSWORD")
_faltantes = [var for var in _REQUERIDAS if not os.getenv(var)]
if _faltantes:
    raise RuntimeError(
        "Faltan variables de entorno obligatorias: "
        + ", ".join(_faltantes)
        + ". Copie .env.example como .env y complete los datos de conexión."
    )

# Configuración de la Base de Datos MySQL
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'SistemaAutocor'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': int(os.getenv('DB_PORT', '3306'))
}

# Constantes de configuración de la interfaz
APP_TITLE = "AUTOCOR - Sistema de Gestión de Taller y Repuestera"
APP_GEOMETRY = "1100x650"